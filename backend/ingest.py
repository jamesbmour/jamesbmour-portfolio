import os
import json
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from datetime import datetime
import requests

load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "portfolio-chat")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "jamesbmour")
DEV_TO_USERNAME = os.getenv("DEV_TO_USERNAME", "jamesbmour")
PORTFOLIO_CONFIG_PATH = os.getenv("PORTFOLIO_CONFIG_PATH", "../gitprofile.config.ts")


class PortfolioIngestion:
    """Handles ingestion of all portfolio content into ChromaDB"""

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        # self.embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        self.vectorstore = None
        self.documents = []

    def load_resume(self):
        """Load resume PDF and TXT files"""
        print("Loading resume documents...")
        resume_docs = []

        # Load PDF
        resume_path = "./James-Brendamour-Resume.pdf"
        if os.path.exists(resume_path):
            print(f"Loading {resume_path}...")
            loader = PyPDFLoader(resume_path)
            docs = loader.load()
            # Add metadata
            for doc in docs:
                doc.metadata["source"] = "resume"
                doc.metadata["type"] = "resume_pdf"
                doc.metadata["last_updated"] = datetime.now().isoformat()
            resume_docs.extend(docs)

        # Load TXT
        txt_path = "./Resume.txt"
        if os.path.exists(txt_path):
            print(f"Loading {txt_path}...")
            loader = TextLoader(txt_path)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = "resume"
                doc.metadata["type"] = "resume_txt"
                doc.metadata["last_updated"] = datetime.now().isoformat()
            resume_docs.extend(docs)

        print(f"Loaded {len(resume_docs)} resume document(s)")
        return resume_docs

    def load_portfolio_config(self):
        """Parse gitprofile.config.ts and extract structured data"""
        print("Loading portfolio configuration...")
        config_docs = []

        config_path = PORTFOLIO_CONFIG_PATH
        if not os.path.exists(config_path):
            print(f"Warning: {config_path} not found")
            return config_docs

        # Read the TypeScript config file
        with open(config_path, "r") as f:
            content = f.read()

        # Extract skills array
        try:
            skills_start = content.find("skills: [")
            if skills_start != -1:
                skills_end = content.find("],", skills_start)
                skills_text = content[skills_start:skills_end]
                # Extract skill names
                skills = [
                    line.strip().strip("'").strip('"').rstrip(",")
                    for line in skills_text.split("\n")
                    if line.strip().startswith("'") or line.strip().startswith('"')
                ]

                skills_doc = Document(
                    page_content=f"James's technical skills include: {', '.join(skills)}. "
                    f"He has expertise in {len(skills)} different technologies and tools.",
                    metadata={
                        "source": "portfolio_config",
                        "type": "skills",
                        "count": len(skills),
                        "last_updated": datetime.now().isoformat(),
                    },
                )
                config_docs.append(skills_doc)
                print(f"  - Extracted {len(skills)} skills")
        except Exception as e:
            print(f"Warning: Could not parse skills: {e}")

        # Extract experiences
        try:
            experiences_start = content.find("experiences: [")
            if experiences_start != -1:
                experiences_end = content.find("],", experiences_start)
                experiences_section = content[experiences_start:experiences_end]

                # Parse each experience
                current_exp = {}
                for line in experiences_section.split("\n"):
                    if "company:" in line and current_exp.get("position"):
                        # Save previous experience
                        exp_text = (
                            f"James worked at {current_exp.get('company', 'Unknown')} "
                            f"as {current_exp.get('position', 'Unknown')} "
                            f"from {current_exp.get('from', 'Unknown')} to {current_exp.get('to', 'Unknown')}."
                        )
                        config_docs.append(
                            Document(
                                page_content=exp_text,
                                metadata={
                                    "source": "portfolio_config",
                                    "type": "experience",
                                    "company": current_exp.get("company", "Unknown"),
                                    "last_updated": datetime.now().isoformat(),
                                },
                            )
                        )
                        current_exp = {}

                    if "company:" in line:
                        # Extract company between quotes
                        start_quote = line.find("'") if "'" in line else line.find('"')
                        if start_quote != -1:
                            end_quote = (
                                line.rfind("'") if "'" in line else line.rfind('"')
                            )
                            current_exp["company"] = line[start_quote + 1 : end_quote]
                    elif "position:" in line:
                        start_quote = line.find("'") if "'" in line else line.find('"')
                        if start_quote != -1:
                            end_quote = (
                                line.rfind("'") if "'" in line else line.rfind('"')
                            )
                            current_exp["position"] = line[start_quote + 1 : end_quote]
                    elif "from:" in line:
                        start_quote = line.find("'") if "'" in line else line.find('"')
                        if start_quote != -1:
                            end_quote = (
                                line.rfind("'") if "'" in line else line.rfind('"')
                            )
                            current_exp["from"] = line[start_quote + 1 : end_quote]
                    elif "to:" in line:
                        start_quote = line.find("'") if "'" in line else line.find('"')
                        if start_quote != -1:
                            end_quote = (
                                line.rfind("'") if "'" in line else line.rfind('"')
                            )
                            current_exp["to"] = line[start_quote + 1 : end_quote]

                # Don't forget last experience
                if current_exp.get("position"):
                    exp_text = (
                        f"James worked at {current_exp.get('company', 'Unknown')} "
                        f"as {current_exp.get('position', 'Unknown')} "
                        f"from {current_exp.get('from', 'Unknown')} to {current_exp.get('to', 'Unknown')}."
                    )
                    config_docs.append(
                        Document(
                            page_content=exp_text,
                            metadata={
                                "source": "portfolio_config",
                                "type": "experience",
                                "company": current_exp.get("company", "Unknown"),
                                "last_updated": datetime.now().isoformat(),
                            },
                        )
                    )

                print(f"  - Extracted experiences")
        except Exception as e:
            print(f"Warning: Could not parse experiences: {e}")

        # Extract education
        try:
            educations_start = content.find("educations: [")
            if educations_start != -1:
                educations_end = content.find("],", educations_start)
                educations_section = content[educations_start:educations_end]

                current_edu = {}
                for line in educations_section.split("\n"):
                    if "institution:" in line and current_edu.get("degree"):
                        # Save previous education
                        edu_text = (
                            f"James earned a {current_edu.get('degree', 'degree')} "
                            f"from {current_edu.get('institution', 'Unknown')} "
                            f"({current_edu.get('from', 'Unknown')}-{current_edu.get('to', 'Unknown')})."
                        )
                        if "minor" in current_edu:
                            edu_text += f" Minor: {current_edu['minor']}."
                        config_docs.append(
                            Document(
                                page_content=edu_text,
                                metadata={
                                    "source": "portfolio_config",
                                    "type": "education",
                                    "institution": current_edu.get(
                                        "institution", "Unknown"
                                    ),
                                    "last_updated": datetime.now().isoformat(),
                                },
                            )
                        )
                        current_edu = {}

                    if "institution:" in line:
                        start_quote = line.find("'") if "'" in line else line.find('"')
                        if start_quote != -1:
                            end_quote = (
                                line.rfind("'") if "'" in line else line.rfind('"')
                            )
                            current_edu["institution"] = line[
                                start_quote + 1 : end_quote
                            ]
                    elif "degree:" in line:
                        start_quote = line.find("'") if "'" in line else line.find('"')
                        if start_quote != -1:
                            end_quote = (
                                line.rfind("'") if "'" in line else line.rfind('"')
                            )
                            current_edu["degree"] = line[start_quote + 1 : end_quote]
                    elif "minor:" in line:
                        start_quote = line.find("'") if "'" in line else line.find('"')
                        if start_quote != -1:
                            end_quote = (
                                line.rfind("'") if "'" in line else line.rfind('"')
                            )
                            current_edu["minor"] = line[start_quote + 1 : end_quote]
                    elif "from:" in line:
                        start_quote = line.find("'") if "'" in line else line.find('"')
                        if start_quote != -1:
                            end_quote = (
                                line.rfind("'") if "'" in line else line.rfind('"')
                            )
                            current_edu["from"] = line[start_quote + 1 : end_quote]
                    elif "to:" in line:
                        start_quote = line.find("'") if "'" in line else line.find('"')
                        if start_quote != -1:
                            end_quote = (
                                line.rfind("'") if "'" in line else line.rfind('"')
                            )
                            current_edu["to"] = line[start_quote + 1 : end_quote]

                # Don't forget last education
                if current_edu.get("degree"):
                    edu_text = (
                        f"James earned a {current_edu.get('degree', 'degree')} "
                        f"from {current_edu.get('institution', 'Unknown')} "
                        f"({current_edu.get('from', 'Unknown')}-{current_edu.get('to', 'Unknown')})."
                    )
                    if "minor" in current_edu:
                        edu_text += f" Minor: {current_edu['minor']}."
                    config_docs.append(
                        Document(
                            page_content=edu_text,
                            metadata={
                                "source": "portfolio_config",
                                "type": "education",
                                "institution": current_edu.get(
                                    "institution", "Unknown"
                                ),
                                "last_updated": datetime.now().isoformat(),
                            },
                        )
                    )

                print(f"  - Extracted education entries")
        except Exception as e:
            print(f"Warning: Could not parse education: {e}")

        # Extract external projects
        try:
            # Find external projects section
            external_start = content.find("external:")
            if external_start != -1:
                projects_start = content.find("projects: [", external_start)
                if projects_start != -1:
                    # Find the closing bracket for external projects array
                    projects_end = content.find("],", projects_start)
                    projects_section = content[projects_start:projects_end]

                    # Parse each project
                    current_proj = {}
                    for line in projects_section.split("\n"):
                        if "title:" in line and current_proj.get("description"):
                            # Save previous project
                            proj_text = (
                                f"Research Project: {current_proj.get('title', 'Unknown')}. "
                                f"{current_proj.get('description', '')}"
                            )
                            config_docs.append(
                                Document(
                                    page_content=proj_text,
                                    metadata={
                                        "source": "portfolio_config",
                                        "type": "external_project",
                                        "title": current_proj.get("title", "Unknown"),
                                        "link": current_proj.get("link", ""),
                                        "last_updated": datetime.now().isoformat(),
                                    },
                                )
                            )
                            current_proj = {}

                        if "title:" in line:
                            # Extract title between quotes
                            start_quote = (
                                line.find("'") if "'" in line else line.find('"')
                            )
                            if start_quote != -1:
                                end_quote = (
                                    line.rfind("'") if "'" in line else line.rfind('"')
                                )
                                current_proj["title"] = line[
                                    start_quote + 1 : end_quote
                                ]
                        elif "description:" in line:
                            start_quote = (
                                line.find("'") if "'" in line else line.find('"')
                            )
                            if start_quote != -1:
                                end_quote = (
                                    line.rfind("'") if "'" in line else line.rfind('"')
                                )
                                current_proj["description"] = line[
                                    start_quote + 1 : end_quote
                                ]
                        elif "link:" in line:
                            start_quote = (
                                line.find("'") if "'" in line else line.find('"')
                            )
                            if start_quote != -1:
                                end_quote = (
                                    line.rfind("'") if "'" in line else line.rfind('"')
                                )
                                current_proj["link"] = line[start_quote + 1 : end_quote]

                    # Don't forget last project
                    if current_proj.get("description"):
                        proj_text = (
                            f"Research Project: {current_proj.get('title', 'Unknown')}. "
                            f"{current_proj.get('description', '')}"
                        )
                        config_docs.append(
                            Document(
                                page_content=proj_text,
                                metadata={
                                    "source": "portfolio_config",
                                    "type": "external_project",
                                    "title": current_proj.get("title", "Unknown"),
                                    "link": current_proj.get("link", ""),
                                    "last_updated": datetime.now().isoformat(),
                                },
                            )
                        )

                    print(f"  - Extracted external projects")
        except Exception as e:
            print(f"Warning: Could not parse external projects: {e}")

        print(f"Loaded {len(config_docs)} config document(s)")
        return config_docs

    def fetch_github_projects(self):
        """Fetch GitHub repository information via GitHub API"""
        print("Fetching GitHub projects...")
        github_docs = []

        try:
            # Fetch user's repositories
            url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
            params = {"sort": "updated", "per_page": 10, "type": "owner"}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            repos = response.json()

            for repo in repos:
                # Skip forks if desired
                if repo.get("fork", False):
                    continue

                # Create document from repo data
                repo_text = (
                    f"GitHub Project: {repo['name']}. "
                    f"Description: {repo.get('description', 'No description available')}. "
                    f"Primary language: {repo.get('language', 'Not specified')}. "
                    f"Stars: {repo.get('stargazers_count', 0)}, "
                    f"Forks: {repo.get('forks_count', 0)}. "
                    f"Last updated: {repo.get('updated_at', 'Unknown')}."
                )

                github_docs.append(
                    Document(
                        page_content=repo_text,
                        metadata={
                            "source": "github",
                            "type": "github_project",
                            "repo_name": repo["name"],
                            "repo_url": repo["html_url"],
                            "language": repo.get("language", "Unknown"),
                            "stars": repo.get("stargazers_count", 0),
                            "last_updated": datetime.now().isoformat(),
                            "repo_updated_at": repo.get("updated_at", "Unknown"),
                        },
                    )
                )

            print(f"Fetched {len(github_docs)} GitHub projects")
        except Exception as e:
            print(f"Warning: Could not fetch GitHub projects: {e}")

        return github_docs

    def fetch_blog_articles(self):
        """Fetch blog articles from Dev.to"""
        print("Fetching blog articles...")
        blog_docs = []

        try:
            url = f"https://dev.to/api/articles?username={DEV_TO_USERNAME}&per_page=10"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            articles = response.json()

            for article in articles:
                article_text = (
                    f"Blog Article: {article['title']}. "
                    f"{article.get('description', '')} "
                    f"Published on {article.get('published_at', 'Unknown')}. "
                    f"Tags: {', '.join(article.get('tag_list', []))}. "
                    f"Read time: {article.get('reading_time_minutes', 'Unknown')} minutes."
                )

                blog_docs.append(
                    Document(
                        page_content=article_text,
                        metadata={
                            "source": "blog",
                            "type": "blog_article",
                            "title": article["title"],
                            "url": article["url"],
                            "published_at": article.get("published_at", "Unknown"),
                            "tags": ", ".join(article.get("tag_list", [])),
                            "last_updated": datetime.now().isoformat(),
                        },
                    )
                )

            print(f"Fetched {len(blog_docs)} blog articles")
        except Exception as e:
            print(f"Warning: Could not fetch blog articles: {e}")

        return blog_docs

    def ingest_all(self, include_dynamic=True):
        """Main ingestion function - loads all content"""
        print("\n=== Starting Portfolio Ingestion ===\n")

        # Load static content
        self.documents.extend(self.load_resume())
        # self.documents.extend(self.load_portfolio_config())

        # Load dynamic content if requested
        # if include_dynamic:
        #     self.documents.extend(self.fetch_github_projects())
        #     self.documents.extend(self.fetch_blog_articles())

        if not self.documents:
            print("Error: No documents to ingest")
            return False

        print(f"\n=== Total: {len(self.documents)} documents loaded ===\n")

        # Split documents
        print("Splitting documents into chunks...")
        splits = self.text_splitter.split_documents(self.documents)
        print(f"Created {len(splits)} chunks")

        # Create or update vector store
        print("\nEmbedding and storing in ChromaDB...")

        # Clear existing database to prevent corruption errors during full ingestion
        if os.path.exists(CHROMA_PERSIST_DIR):
            print(f"Clearing existing persistence directory: {CHROMA_PERSIST_DIR}")
            shutil.rmtree(CHROMA_PERSIST_DIR)

        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            collection_name=COLLECTION_NAME,
            persist_directory=CHROMA_PERSIST_DIR,
        )

        print(f"\n=== Ingestion Complete! ===")
        print(f"Vector store persisted to: {CHROMA_PERSIST_DIR}")
        print(f"Collection name: {COLLECTION_NAME}")

        return True

    def update_dynamic_content(self):
        """Update only dynamic content (GitHub projects and blog articles)"""
        print("\n=== Updating Dynamic Content ===\n")

        # Fetch fresh dynamic content
        new_docs = []
        new_docs.extend(self.fetch_github_projects())
        new_docs.extend(self.fetch_blog_articles())

        if not new_docs:
            print("No dynamic content to update")
            return False

        # Split new documents
        splits = self.text_splitter.split_documents(new_docs)
        print(f"Created {len(splits)} new chunks")

        # Load existing vector store
        vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=CHROMA_PERSIST_DIR,
        )

        # Delete old dynamic content
        print("Removing old dynamic content...")
        try:
            # Get all documents with source="github" or source="blog"
            collection = vectorstore._collection
            github_ids = collection.get(where={"source": "github"})["ids"]
            blog_ids = collection.get(where={"source": "blog"})["ids"]

            if github_ids:
                collection.delete(ids=github_ids)
                print(f"  - Deleted {len(github_ids)} old GitHub entries")
            if blog_ids:
                collection.delete(ids=blog_ids)
                print(f"  - Deleted {len(blog_ids)} old blog entries")
        except Exception as e:
            print(f"Warning: Could not delete old dynamic content: {e}")

        # Add new content
        print("Adding new dynamic content...")
        vectorstore.add_documents(splits)

        print(f"\n=== Dynamic Content Update Complete! ===")
        return True


def main():
    """Main entry point"""
    import sys

    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY must be set in .env")
        sys.exit(1)

    ingestion = PortfolioIngestion()

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--update-dynamic":
        # Update only dynamic content
        success = ingestion.update_dynamic_content()
    else:
        # Full ingestion
        success = ingestion.ingest_all(include_dynamic=True)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
