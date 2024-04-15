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
    response = requests.request("POST", url, headers=headers, data=payload)

    # response = requests.post(url, json=payload, headers=headers)
    # check if the response is successful
    response.raise_for_status()
    response_data = response.json()
    print(response_data)
    chat_response = response_data.get('choices', [{}])[0].get('text', '').strip()
    print(chat_response)
    return {"response": chat_response}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)