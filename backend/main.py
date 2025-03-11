import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np

# Load API keys from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


# Load and embed documents for FAISS
def load_documents():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        text = f.read()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    documents = text_splitter.split_text(text)
    docs = [Document(page_content=doc) for doc in documents]
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)

    return db

vector_db = load_documents()

# Request model
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    query = request.message

    # Use the updated invoke method instead of get_relevant_documents
    retriever = vector_db.as_retriever()
    retrieved_docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in retrieved_docs[:3]])

    # Construct the final query with retrieved context
    final_query = f"Context: {context}\n\nUser Query: {query}"

    # Use the specific Gemini model recommended in the error message
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    
    try:
        response = model.generate_content(final_query)
        return {"response": response.text}
    except Exception as e:
        # If that model fails, try a fallback model
        try:
            fallback_model = genai.GenerativeModel("models/gemini-1.5-pro")
            fallback_response = fallback_model.generate_content(final_query)
            return {"response": fallback_response.text, "note": "Used fallback model"}
        except Exception as fallback_error:
            return {
                "error": f"Primary error: {str(e)}. Fallback error: {str(fallback_error)}",
                "suggestion": "Try using one of these models directly: models/gemini-1.5-flash or models/gemini-1.5-pro"
            }