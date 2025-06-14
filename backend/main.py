# Import necessary libraries
from dotenv import load_dotenv  # Loads environment variables from a .env file
from langchain_openai import ChatOpenAI  # Imports the ChatOpenAI model for language processing
from langchain.chains import ConversationChain  # Imports the ConversationChain for managing chat interactions
from langchain.memory import ConversationBufferMemory  # Imports memory management for conversation history
import os  # Imports the os module for environment variable access

# Load environment variables from the .env file
load_dotenv()

def create_chatbot():
    # Initialize the ChatOpenAI model with a temperature of 0.7 for controlled randomness
    llm = ChatOpenAI(
        temperature=0.7,
        model_name="gpt-3.5-turbo"  # Specifies the model to use
    )
    
    # Create a conversation chain with memory to maintain context
    conversation = ConversationChain(
        llm=llm,  # Passes the initialized model
        memory=ConversationBufferMemory(),  # Uses buffer memory to store conversation history
        verbose=True  # Enables verbose output for debugging
    )
    
    return conversation  # Returns the configured conversation chain

def main():
    # Create the chatbot using the create_chatbot function
    chatbot = create_chatbot()
    
    print("Welcome to the LangChain Chatbot! Type 'quit' to exit.")  # Displays a welcome message
    
    while True:
        # Get user input and strip any leading/trailing whitespace
        user_input = input("\nYou: ").strip()
        
        # Check if the user wants to quit the program
        if user_input.lower() == 'quit':
            print("Goodbye!")  # Displays a goodbye message
            break  # Exits the loop
        
        # Get a response from the chatbot using the user's input
        response = chatbot.predict(input=user_input)
        print(f"\nBot: {response}")  # Displays the bot's response

if __name__ == "__main__":
    main()  # Ensures the main function is called when the script is run directly