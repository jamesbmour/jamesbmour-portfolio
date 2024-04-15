from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings  # , HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from dotenv import load_dotenv
import os
import requests
import json

# from langchain import ChatOpenAI, LangChain
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage


# from langchain import LangChain, ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Access the API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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

@app.post("/chat/")
async def create_chat_message(chat_request: ChatRequest):
    url = "https://api.openai.com/v1/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = json.dumps({
    "model": "gpt-3.5-turbo-instruct",
    "prompt": chat_request.message,
    "max_tokens": 250,
    "temperature": 0.7
    })
    chat = ChatOpenAI(
        api_key = OPENAI_API_KEY,
        model = "gpt-3.5-turbo",
        temperature = 0.7,
        max_tokens = 250
    )
    
    response = chat.invoke(
    [
        HumanMessage(
            content=chat_request.message
        )
    ]    
    )
    print(response)
    return {"response": response.content}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)