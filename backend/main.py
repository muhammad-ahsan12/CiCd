from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
import shutil
from typing import List
import uvicorn
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI()

# CORS configuration to allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:3000"],  # Streamlit default port + React (if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration

TMP_DIR = Path("data/tmp")
os.makedirs(TMP_DIR, exist_ok=True)

class QuestionRequest(BaseModel):
    prompt: str

# Global state for the conversational chain and memory
state = {"chain": None, "memory": None}

# Custom prompt template
CHAT_PROMPT = ChatPromptTemplate.from_template("""
You are a helpful assistant that answers questions based only on the provided PDF documents.
If the answer isn't in the documents, say "I don't have enough information to answer that."

Context: {context}

Chat History: {chat_history}

Question: {question}

Answer:
""")

# Helper Functions
def load_documents(files: List[UploadFile]):
    """Load PDF documents from uploaded files."""
    documents = []
    for uploaded_file in files:
        # Check if file is a PDF
        if not uploaded_file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail=f"File {uploaded_file.filename} is not a PDF.")
        
        temp_file_path = TMP_DIR / uploaded_file.filename
        with open(temp_file_path, "wb") as f:
            shutil.copyfileobj(uploaded_file.file, f)
        
        loader = PyPDFLoader(temp_file_path.as_posix())
        loaded_docs = loader.load()
        for doc in loaded_docs:
            doc.metadata["source"] = uploaded_file.filename
        documents.extend(loaded_docs)
    return documents

def create_vectorstore_and_chain(files: List[UploadFile]):
    """Create a vector store and conversational chain from uploaded PDF files."""
    # Load documents
    documents = load_documents(files)
    if not documents:
        raise HTTPException(status_code=400, detail="No valid PDF documents were loaded")
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Create retriever
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    
    # Create conversational chain
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer",
        input_key="question"
    )
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile", temperature=0.5)
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False,
        combine_docs_chain_kwargs={"prompt": CHAT_PROMPT}
    )
    
    # Update state
    state["chain"] = chain
    state["memory"] = memory

# API Endpoints
@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload PDF documents and prepare them for question-answering."""
    try:
        create_vectorstore_and_chain(files)
        return JSONResponse(content={"message": "PDF documents uploaded successfully and ready for questions"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF documents: {str(e)}")

from pydantic import BaseModel

class QuestionRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Answer questions based on the uploaded PDF documents."""
    if not state["chain"]:
        raise HTTPException(status_code=400, detail="No PDF documents uploaded yet. Please upload PDFs first.")
    
    try:
        response = state["chain"].invoke({"question": request.prompt})
        answer = response["answer"]
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
