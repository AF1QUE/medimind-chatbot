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

# Load environment variables from the .env file
load_dotenv()

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
    
    # Create a conversation chain with memory
    conversation = ConversationChain(
        llm=llm,  # Passes the initialized model
        memory=ConversationBufferMemory(),  # Uses buffer memory to store conversation history
        verbose=True  # Enables verbose output for debugging
    )
    
    return conversation, vectorstore

def main():
    # Create the RAG chatbot
    chatbot, vectorstore = create_rag_chatbot()
    
    print("Welcome to the RAG-powered LangChain Chatbot! Type 'quit' to exit.")  # Displays a welcome message
    
    while True:
        # Get user input and strip any leading/trailing whitespace
        user_input = input("\nYou: ").strip()
        
        # Check if the user wants to quit the program
        if user_input.lower() == 'quit':
            print("Goodbye!")  # Displays a goodbye message
            # Persist the vector store before exiting
            vectorstore.persist()
            break  # Exits the loop
        
        # Retrieve relevant documents
        relevant_docs = vectorstore.similarity_search(user_input, k=3)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        # Combine user input with retrieved context
        augmented_input = f"Context: {context}\n\nUser question: {user_input}"
        
        # Get response from the chatbot
        response = chatbot.predict(input=augmented_input)
        print(f"\nBot: {response}")  # Displays the bot's response

if __name__ == "__main__":
    main()  # Ensures the main function is called when the script is run directly