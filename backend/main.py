# Import necessary libraries
from dotenv import load_dotenv  # Loads environment variables from a .env file
from langchain_openai import ChatOpenAI  # Imports the ChatOpenAI model for language processing
from langchain.chains import ConversationChain  # Imports the ConversationChain for managing chat interactions
from langchain.memory import ConversationBufferMemory  # Imports memory management for conversation history
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os  # Imports the os module for environment variable access
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Load environment variables from the .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request and response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

# Global variables to store conversation chains
conversation_chains = {}

def create_rag_chatbot():
    # Initialize the embedding model
    embeddings = OpenAIEmbeddings()
    
    # Initialize the ChatOpenAI model
    llm = ChatOpenAI(
        temperature=0.7,
        model_name="gpt-3.5-turbo"  # Specifies the model to use
    )
    
    # Load and process documents
    def load_documents(directory_path):
        # Check if vector store already exists
        persist_directory = "./chroma_db"
        
        if os.path.exists(persist_directory):
            print("Loading existing vector store...")
            vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=embeddings
            )
        else:
            print("Creating new vector store...")
            # Load documents
            loader = DirectoryLoader(directory_path, glob="**/*.txt", loader_cls=TextLoader)
            documents = loader.load()
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(documents)
            
            # Create and persist vector store
            vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=embeddings,
                persist_directory=persist_directory
            )
            # Explicitly persist the database
            vectorstore.persist()
        
        return vectorstore
    
    # Create vector store
    vectorstore = load_documents("documents")
    
    return vectorstore

# Initialize the vector store
vectorstore = create_rag_chatbot()

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Get or create conversation chain
        if request.conversation_id not in conversation_chains:
            conversation_chains[request.conversation_id] = ConversationChain(
                llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo"),
                memory=ConversationBufferMemory(),
                verbose=True
            )
        
        conversation = conversation_chains[request.conversation_id]
        
        # Retrieve relevant documents
        relevant_docs = vectorstore.similarity_search(request.message, k=3)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        # Create augmented input
        augmented_input = f"""You are a medical assistant. Use the following context to answer the user's question. 
If the context doesn't contain relevant information, say so.

Context:
{context}

User question: {request.message}

Answer:"""
        
        # Get response
        response = conversation.predict(input=augmented_input)
        
        return ChatResponse(
            response=response,
            conversation_id=request.conversation_id or "new_conversation"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000);