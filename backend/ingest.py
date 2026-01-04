"""
Data ingestion pipeline for the RAG chatbot.
Loads data from multiple sources and ingests into Qdrant vector database.

Data Sources:
1. Resume PDF
2. Portfolio configuration (gitprofile.config.ts)
3. GitHub repositories
4. Dev.to blog articles

Extensible design allows easy addition of new data sources.
"""
import os
import re
import json
import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from config import config


# Abstract Base Class for Data Loaders
class DataLoader(ABC):
    """Abstract base class for data loaders"""

    @abstractmethod
    def load(self) -> List[Document]:
        """Load documents from data source"""
        pass


# Data Loader Implementations
class ResumePDFLoader(DataLoader):
    """Load resume PDF document"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def load(self) -> List[Document]:
        """Load resume PDF"""
        print(f"Loading resume PDF from: {self.pdf_path}")

        if not os.path.exists(self.pdf_path):
            print(f"Warning: Resume PDF not found at {self.pdf_path}")
            return []

        loader = PyPDFLoader(self.pdf_path)
        docs = loader.load()

        # Add metadata
        for doc in docs:
            doc.metadata["source"] = "resume"
            doc.metadata["type"] = "resume_pdf"
            doc.metadata["last_updated"] = datetime.now().isoformat()

        print(f"Loaded {len(docs)} pages from resume PDF")
        return docs


class PortfolioConfigLoader(DataLoader):
    """Load and parse gitprofile.config.ts"""

    def __init__(self, config_path: str):
        self.config_path = config_path

    def load(self) -> List[Document]:
        """Parse portfolio configuration and extract structured data"""
        print(f"Loading portfolio configuration from: {self.config_path}")

        if not os.path.exists(self.config_path):
            print(f"Warning: Config file not found at {self.config_path}")
            return []

        with open(self.config_path, "r") as f:
            content = f.read()

        docs = []

        # Extract skills
        skills_docs = self._extract_skills(content)
        docs.extend(skills_docs)

        # Extract experience
        experience_docs = self._extract_experience(content)
        docs.extend(experience_docs)

        # Extract education
        education_docs = self._extract_education(content)
        docs.extend(education_docs)

        # Extract external projects
        projects_docs = self._extract_external_projects(content)
        docs.extend(projects_docs)

        print(f"Extracted {len(docs)} documents from portfolio config")
        return docs

    def _extract_skills(self, content: str) -> List[Document]:
        """Extract skills array from config"""
        docs = []
        try:
            # Find skills array
            skills_match = re.search(r"skills:\s*\[(.*?)\]", content, re.DOTALL)
            if skills_match:
                skills_text = skills_match.group(1)
                # Extract individual skills (quoted strings)
                skills = re.findall(r"'([^']*)'", skills_text)

                if skills:
                    skills_content = f"Technical Skills: {', '.join(skills)}"
                    doc = Document(
                        page_content=skills_content,
                        metadata={
                            "source": "portfolio_config",
                            "type": "skills",
                            "last_updated": datetime.now().isoformat(),
                        }
                    )
                    docs.append(doc)
                    print(f"Extracted {len(skills)} skills")

        except Exception as e:
            print(f"Error extracting skills: {str(e)}")

        return docs

    def _extract_experience(self, content: str) -> List[Document]:
        """Extract work experience from config"""
        docs = []
        try:
            # Find experiences array
            exp_match = re.search(r"experiences:\s*\[(.*?)\],\s*certifications", content, re.DOTALL)
            if exp_match:
                experiences_text = exp_match.group(1)

                # Extract individual experience objects
                exp_objects = re.findall(r"\{(.*?)\}", experiences_text, re.DOTALL)

                for exp_obj in exp_objects:
                    # Extract fields
                    company_match = re.search(r"company:\s*'([^']*)'", exp_obj)
                    position_match = re.search(r"position:\s*'([^']*)'", exp_obj)
                    from_match = re.search(r"from:\s*'([^']*)'", exp_obj)
                    to_match = re.search(r"to:\s*'([^']*)'", exp_obj)
                    comp_url_match = re.search(r"companyLink:\s*'([^']*)'", exp_obj)

                    if company_match and position_match:
                        company = company_match.group(1)
                        position = position_match.group(1)
                        from_date = from_match.group(1) if from_match else "N/A"
                        to_date = to_match.group(1) if to_match else "Present"
                        comp_url = comp_url_match.group(1) if comp_url_match else ""

                        exp_content = f"Work Experience: {position} at {company} ({from_date} - {to_date})"

                        doc = Document(
                            page_content=exp_content,
                            metadata={
                                "source": "portfolio_config",
                                "type": "experience",
                                "company": company,
                                "position": position,
                                "from": from_date,
                                "to": to_date,
                                "company_url": comp_url,
                                "last_updated": datetime.now().isoformat(),
                            }
                        )
                        docs.append(doc)

                print(f"Extracted {len(docs)} work experiences")

        except Exception as e:
            print(f"Error extracting experience: {str(e)}")

        return docs

    def _extract_education(self, content: str) -> List[Document]:
        """Extract education from config"""
        docs = []
        try:
            # Find education array
            edu_match = re.search(r"education:\s*\[(.*?)\],\s*publications", content, re.DOTALL)
            if edu_match:
                education_text = edu_match.group(1)

                # Extract individual education objects
                edu_objects = re.findall(r"\{(.*?)\}", education_text, re.DOTALL)

                for edu_obj in edu_objects:
                    # Extract fields
                    institution_match = re.search(r"institution:\s*'([^']*)'", edu_obj)
                    degree_match = re.search(r"degree:\s*'([^']*)'", edu_obj)
                    from_match = re.search(r"from:\s*'([^']*)'", edu_obj)
                    to_match = re.search(r"to:\s*'([^']*)'", edu_obj)

                    if institution_match and degree_match:
                        institution = institution_match.group(1)
                        degree = degree_match.group(1)
                        from_date = from_match.group(1) if from_match else "N/A"
                        to_date = to_match.group(1) if to_match else "N/A"

                        edu_content = f"Education: {degree} from {institution} ({from_date} - {to_date})"

                        doc = Document(
                            page_content=edu_content,
                            metadata={
                                "source": "portfolio_config",
                                "type": "education",
                                "institution": institution,
                                "degree": degree,
                                "from": from_date,
                                "to": to_date,
                                "last_updated": datetime.now().isoformat(),
                            }
                        )
                        docs.append(doc)

                print(f"Extracted {len(docs)} education entries")

        except Exception as e:
            print(f"Error extracting education: {str(e)}")

        return docs

    def _extract_external_projects(self, content: str) -> List[Document]:
        """Extract external projects from config"""
        docs = []
        try:
            # Find external projects array
            proj_match = re.search(r"external:\s*\{.*?projects:\s*\[(.*?)\]", content, re.DOTALL)
            if proj_match:
                projects_text = proj_match.group(1)

                # Extract individual project objects
                proj_objects = re.findall(r"\{(.*?)\}", projects_text, re.DOTALL)

                for proj_obj in proj_objects:
                    # Extract fields
                    title_match = re.search(r"title:\s*'([^']*)'", proj_obj)
                    desc_match = re.search(r"description:\s*'([^']*)'", proj_obj)
                    link_match = re.search(r"link:\s*'([^']*)'", proj_obj)

                    if title_match and desc_match:
                        title = title_match.group(1)
                        description = desc_match.group(1)
                        link = link_match.group(1) if link_match else ""

                        proj_content = f"Project: {title}\n{description}"

                        doc = Document(
                            page_content=proj_content,
                            metadata={
                                "source": "portfolio_config",
                                "type": "external_project",
                                "title": title,
                                "link": link,
                                "last_updated": datetime.now().isoformat(),
                            }
                        )
                        docs.append(doc)

                print(f"Extracted {len(docs)} external projects")

        except Exception as e:
            print(f"Error extracting external projects: {str(e)}")

        return docs


class GitHubReposLoader(DataLoader):
    """Load GitHub repositories via API"""

    def __init__(self, username: str, max_repos: int = 4):
        self.username = username
        self.max_repos = max_repos

    def load(self) -> List[Document]:
        """Fetch GitHub repositories"""
        print(f"Loading GitHub repositories for: {self.username}")

        try:
            url = f"https://api.github.com/users/{self.username}/repos"
            response = requests.get(url, params={"sort": "updated", "per_page": 100})
            response.raise_for_status()

            repos = response.json()

            # Filter and sort
            repos = [r for r in repos if not r.get("fork", False)]
            repos = sorted(repos, key=lambda x: x.get("updated_at", ""), reverse=True)
            repos = repos[:self.max_repos]

            docs = []
            for repo in repos:
                name = repo.get("name", "Unknown")
                description = repo.get("description", "No description available")
                language = repo.get("language", "Unknown")
                stars = repo.get("stargazers_count", 0)
                url = repo.get("html_url", "")
                updated = repo.get("updated_at", "")

                content = f"GitHub Project: {name}\nDescription: {description}\nPrimary Language: {language}\nStars: {stars}"

                doc = Document(
                    page_content=content,
                    metadata={
                        "source": "github",
                        "type": "project",
                        "repo_name": name,
                        "repo_url": url,
                        "language": language,
                        "stars": stars,
                        "updated_at": updated,
                        "last_updated": datetime.now().isoformat(),
                    }
                )
                docs.append(doc)

            print(f"Loaded {len(docs)} GitHub repositories")
            return docs

        except Exception as e:
            print(f"Error loading GitHub repos: {str(e)}")
            return []


class DevToBlogLoader(DataLoader):
    """Load blog articles from dev.to"""

    def __init__(self, username: str, max_articles: int = 4):
        self.username = username
        self.max_articles = max_articles

    def load(self) -> List[Document]:
        """Fetch dev.to blog articles"""
        print(f"Loading dev.to articles for: {self.username}")

        try:
            url = f"https://dev.to/api/articles?username={self.username}&per_page={self.max_articles}"
            response = requests.get(url)
            response.raise_for_status()

            articles = response.json()

            docs = []
            for article in articles:
                title = article.get("title", "Unknown")
                description = article.get("description", "")
                tags = ", ".join(article.get("tag_list", []))
                url = article.get("url", "")
                published = article.get("published_at", "")
                reading_time = article.get("reading_time_minutes", 0)

                content = f"Blog Article: {title}\n{description}\nTags: {tags}\nReading Time: {reading_time} minutes"

                doc = Document(
                    page_content=content,
                    metadata={
                        "source": "blog",
                        "type": "article",
                        "title": title,
                        "url": url,
                        "tags": tags,
                        "published_at": published,
                        "reading_time": reading_time,
                        "last_updated": datetime.now().isoformat(),
                    }
                )
                docs.append(doc)

            print(f"Loaded {len(docs)} blog articles")
            return docs

        except Exception as e:
            print(f"Error loading blog articles: {str(e)}")
            return []


# Main Ingestion Class
class DataIngestion:
    """
    Main data ingestion pipeline.
    Coordinates loading from all sources and ingesting into Qdrant.
    """

    def __init__(self):
        """Initialize ingestion pipeline"""
        # Validate configuration
        config.validate()

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY,
        )

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
        )

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
        )

        # Data loaders registry
        self.loaders: Dict[str, DataLoader] = {}

    def register_loader(self, name: str, loader: DataLoader):
        """Register a new data loader"""
        self.loaders[name] = loader
        print(f"Registered loader: {name}")

    def load_all_sources(self) -> List[Document]:
        """Load documents from all registered sources"""
        all_docs = []

        for name, loader in self.loaders.items():
            try:
                print(f"\n{'='*60}")
                print(f"Loading data source: {name}")
                print(f"{'='*60}")

                docs = loader.load()
                all_docs.extend(docs)

                print(f"✓ Loaded {len(docs)} documents from {name}")

            except Exception as e:
                print(f"✗ Error loading {name}: {str(e)}")

        return all_docs

    def setup_collection(self):
        """Setup or recreate Qdrant collection"""
        collection_name = config.COLLECTION_NAME

        # Check if collection exists
        collections = self.qdrant_client.get_collections()
        collection_exists = any(col.name == collection_name for col in collections.collections)

        if collection_exists:
            print(f"Collection '{collection_name}' already exists. Deleting...")
            self.qdrant_client.delete_collection(collection_name)

        # Create collection
        print(f"Creating collection: {collection_name}")
        self.qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1536,  # OpenAI text-embedding-3-small dimension
                distance=Distance.COSINE,
            ),
        )
        print(f"✓ Collection '{collection_name}' created")

    def ingest(self, recreate_collection: bool = True):
        """
        Run full ingestion pipeline.

        Args:
            recreate_collection: Whether to recreate the collection (default: True)
        """
        print("\n" + "="*60)
        print("STARTING DATA INGESTION PIPELINE")
        print("="*60 + "\n")

        # Setup collection
        if recreate_collection:
            self.setup_collection()

        # Load all documents
        print("\n" + "="*60)
        print("LOADING DATA SOURCES")
        print("="*60)

        all_docs = self.load_all_sources()

        if not all_docs:
            print("\n✗ No documents loaded. Aborting ingestion.")
            return

        print(f"\n✓ Total documents loaded: {len(all_docs)}")

        # Split documents
        print("\n" + "="*60)
        print("SPLITTING DOCUMENTS")
        print("="*60)

        split_docs = self.text_splitter.split_documents(all_docs)
        print(f"✓ Split into {len(split_docs)} chunks")

        # Ingest into Qdrant
        print("\n" + "="*60)
        print("INGESTING INTO QDRANT")
        print("="*60)

        vector_store = QdrantVectorStore.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY,
            collection_name=config.COLLECTION_NAME,
        )

        print(f"✓ Ingested {len(split_docs)} chunks into Qdrant")

        # Display summary
        self.print_summary(all_docs, split_docs)

        print("\n" + "="*60)
        print("INGESTION COMPLETE!")
        print("="*60 + "\n")

    def print_summary(self, all_docs: List[Document], split_docs: List[Document]):
        """Print ingestion summary"""
        print("\n" + "="*60)
        print("INGESTION SUMMARY")
        print("="*60)

        # Count by source
        source_counts = {}
        for doc in all_docs:
            source = doc.metadata.get("source", "unknown")
            source_counts[source] = source_counts.get(source, 0) + 1

        print("\nDocuments by source:")
        for source, count in sorted(source_counts.items()):
            print(f"  - {source}: {count}")

        print(f"\nTotal documents: {len(all_docs)}")
        print(f"Total chunks: {len(split_docs)}")
        print(f"Collection: {config.COLLECTION_NAME}")


def main():
    """Main ingestion function"""
    # Initialize ingestion pipeline
    pipeline = DataIngestion()

    # Register data loaders
    pipeline.register_loader(
        "resume_pdf",
        ResumePDFLoader("../src/data/James-Brendamour-Resume.pdf")
    )

    pipeline.register_loader(
        "portfolio_config",
        PortfolioConfigLoader(config.PORTFOLIO_CONFIG_PATH)
    )

    pipeline.register_loader(
        "github_repos",
        GitHubReposLoader(config.GITHUB_USERNAME, max_repos=4)
    )

    pipeline.register_loader(
        "devto_blog",
        DevToBlogLoader(config.DEV_TO_USERNAME, max_articles=4)
    )

    # Run ingestion
    pipeline.ingest(recreate_collection=True)


if __name__ == "__main__":
    main()
