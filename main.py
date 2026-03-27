# Importing required packages

from dotenv import load_dotenv   # Loads environment variables from a .env file into the system environment
import os                        # Standard Python library for interacting with the operating system (not directly used here)
from langchain_core.prompts import PromptTemplate  # LangChain class for creating structured prompts with placeholders
from langchain.agents import create_agent  # LangChain functions for creating agents and specifying agent types
from langchain_core.tools import Tool, tool  # LangChain class for defining tools that agents can use to perform specific tasks
from langchain_core.messages import HumanMessage  # LangChain class for representing messages from a human user 
from langchain_openai import ChatOpenAI   # LangChain wrapper for OpenAI chat models (like GPT-4)
from openai import OpenAI                 # Official OpenAI Python SDK (imported but not used in this script)

# Load environment variables (e.g., API keys) from the .env file
load_dotenv()

# define a tool that the agent can use to search the web for information
@tool
def search(query: str) -> str:
    # In a real implementation, this function would perform a web search and return results.
    # For this example, we'll return a placeholder string.
    """Tool that searches over internet for information.
    Args:
        query (str): The search query to look up information for.
    Returns:
        str: The search results."""
    
    print(f"Performing search for query: '{query}'")  # Log the search query for debugging
    return f"Search results for '{query}'"

llm = ChatOpenAI(model="gpt-4")  # Initialize the language model (GPT-4) using LangChain's wrapper
tools = [search]  # Create a list of tools that the agent can use (currently only the search tool)
agent = create_agent(model=llm, tools=tools)  # Create an agent with the specified LLM, tools

# Define the main function that will run when the script is executed
def main():
    print("Hello from langchain-agent!")  # Simple greeting to confirm execution
    result = agent.invoke({"messages": [HumanMessage(content="What is the weather is Pune, India?")]})  # Run the agent with a human message asking for the capital of France
    print(f"Agent response: {result}")  # Print the agent's response to the console

# Standard Python entry point
# Ensures main() runs only when the script is executed directly, not when imported
if __name__ == "__main__":
    main()