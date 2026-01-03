import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "portfolio-chat")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY must be set in .env")

# Initialize FastAPI
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://jamesbmour.com",
        "https://www.jamesbmour.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Components
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=CHROMA_PERSIST_DIR,
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

# Prompt Template
system_prompt = (
    "You are a professional recruitment assistant for James Brendamour's portfolio website. "
    "Use the following pieces of retrieved context to answer questions about James's skills, "
    "experience, education, projects, and blog articles. "
    "If you don't know the answer, say that you don't have that information. "
    "Keep your answers professional, concise, and helpful to potential employers. "
    "When discussing projects, mention relevant technologies and skills used. "
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat/")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"Received query: {request.message[:100]}...")
    try:
        response = rag_chain.invoke({"input": request.message})
        logger.info("Response generated successfully")
        return {"response": response["answer"]}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
