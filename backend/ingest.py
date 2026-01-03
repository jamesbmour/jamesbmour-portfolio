import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import time

load_dotenv()

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "portfolio-chat")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def ingest_data():
    if not PINECONE_API_KEY or not OPENAI_API_KEY:
        print("Error: PINECONE_API_KEY and OPENAI_API_KEY must be set in .env")
        return

    print("Initialize Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Create index if it doesn't exist
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Creating index {PINECONE_INDEX_NAME}...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
            time.sleep(1)

    print("Loading documents...")
    documents = []

    # Load Recume
    resume_path = "/Users/james/Library/CloudStorage/Dropbox/GitHub/jamesbmour-portfolio/backend/James-Brendamour-Resume.pdf"
    if os.path.exists(resume_path):
        print(f"Loading {resume_path}...")
        loader = PyPDFLoader(resume_path)
        documents.extend(loader.load())
    else:
        print(f"Warning: {resume_path} not found.")

    # Load Resume.txt if exists (as fallback or additional context)
    txt_path = "./Resume.txt"
    if os.path.exists(txt_path):
        print(f"Loading {txt_path}...")
        loader = TextLoader(txt_path)
        documents.extend(loader.load())

    if not documents:
        print("No documents found to ingest.")
        return

    print(f"Loaded {len(documents)} documents.")

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    print(f"Split into {len(splits)} chunks.")

    # Embed and store
    print("Embedding and storing in Pinecone...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    PineconeVectorStore.from_documents(
        documents=splits, embedding=embeddings, index_name=PINECONE_INDEX_NAME
    )

    print("Ingestion complete!")


if __name__ == "__main__":
    ingest_data()
