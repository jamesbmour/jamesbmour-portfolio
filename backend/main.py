import os
import requests
import json
import lancedb
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings  # , HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import LanceDB
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS


# from langchain import LangChain, ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Access the API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
RESUME_PDF = './James-Brendamour-Resume.pdf'
# Create a FastAPI instance
app = FastAPI()

# Configure CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # List the origins that should be allowed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ChatRequest(BaseModel):
    message: str

def load_pdf(query="What is this document about?"):
    loader = PyPDFLoader(RESUME_PDF)
    pages = loader.load_and_split()
    # print(pages[0])
    faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
    docs = faiss_index.similarity_search(query, k=2)
    for doc in docs:
        print(str(doc.metadata["page"]) + ":", doc.page_content[:300])


    return docs



def get_vector_store():
    # Create a FAISS vector store

    embeddings = OpenAIEmbeddings()

    db = lancedb.connect("/tmp/lancedb")
    table = db.create_table(
        "my_table",
        data=[
            {
                "vector": embeddings.embed_query("Hello World"),
                "text": "Hello World",
                "id": "1",
            }
        ],
        mode="overwrite",
    )
    # Load the document, split it into chunks, embed each chunk and load it into the vector store.
    raw_documents = TextLoader('./Resume.txt').load()
    text_splitter = CharacterTextSplitter(chunk_size=256, chunk_overlap=40)
    documents = text_splitter.split_documents(raw_documents)
    db = LanceDB.from_documents(documents, OpenAIEmbeddings())
    query = "What is the document about?"
    docs = db.similarity_search(query)
    # print(docs)
    return docs


@app.post("/chat/")
async def create_chat_message(chat_request: ChatRequest):
    chat = ChatOpenAI(
        openai_api_base= "https://openrouter.ai/api/v1",
        # api_key = OPENAI_API_KEY,
        api_key = OPENROUTER_API_KEY,
        # model = "gpt-3.5-turbo",
        model = "mistralai/mistral-7b-instruct:free",
        temperature = 0.3,
        max_tokens = 250
    )
    
    
    response = chat.invoke(
    [
        HumanMessage(
            content=chat_request.message
        )
    ]    
    )
    print(response.content)
    return {"response": response.content}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)