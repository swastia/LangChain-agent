# Importing required packages

from dotenv import load_dotenv   # Loads environment variables from a .env file into the system environment
import os                        # Standard Python library for interacting with the operating system (not directly used here)
from langchain_core.prompts import PromptTemplate  # LangChain class for creating structured prompts with placeholders
from langchain.agents import create_agent  # LangChain functions for creating agents and specifying agent types
from langchain_core.tools import Tool, tool  # LangChain class for defining tools that agents can use to perform specific tasks
from langchain_core.messages import HumanMessage  # LangChain class for representing messages from a human user 
from langchain_openai import ChatOpenAI   # LangChain wrapper for OpenAI chat models (like GPT-4)
from openai import OpenAI                 # Official OpenAI Python SDK (imported but not used in this script)

from tavily import TavilyClient  # Importing the Tavily client

# Load environment variables (e.g., API keys) from the .env file
load_dotenv()

tavily = TavilyClient()  # Initialize the Tavily client

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
    return tavily.search(query)  # Use the Tavily client to perform the search and return results

llm = ChatOpenAI(model="gpt-5.4-nano")  # Initialize the language model (GPT-4) using LangChain's wrapper
tools = [search]  # Create a list of tools that the agent can use (currently only the search tool)
agent = create_agent(model=llm, tools=tools)  # Create an agent with the specified LLM, tools

# Define the main function that will run when the script is executed
def main():
    print("Hello from langchain-agent!")  # Simple greeting to confirm execution
    #result = agent.invoke({"messages": [HumanMessage(content="What is the weather is Pune, India?")]})  # Run the agent with a human message asking for the capital of France
    result = agent.invoke({"messages": [HumanMessage(content="search for 3 job postings for an ai engineer in Pune, India on naukari.com and list their details")]})  # Run the agent with a human message asking for the capital of France
    print(f"Agent response: {result}")  # Print the agent's response to the console

# Standard Python entry point
# Ensures main() runs only when the script is executed directly, not when imported
if __name__ == "__main__":
    main()



#sample output for a simple search query "What is the weather is Pune, India?" using tavily search tool and gpt-5.4-nano model:
#Right now in Pune, India, it’s Sunny.
#Temperature: 25.4°C (feels like 26.4°C)
#Humidity: 58%
#Wind: 5.4 kph from NW
#Cloud cover: 22%
#Precipitation: 0.0 mm
#Visibility: 10 km
#Last updated: 2026-04-01 07:15 (local time)

#####******* Replaced the query for linkedin to naukari.com because LLM was not able to extract the exact postings on linked in.
#Output for naukari.com is:
#***************************

#Here are 3 AI Engineer job postings in Pune, India found on Naukri.com (with the details available from the listing pages):
#AI Engineer - Pune - Infosys
#
#Company: Infosys Limited
#Location: Pune
#Experience: 7 to 8 years
#Naukri link: https://www.naukri.com/job-listings-ai-engineer-infosys-limited-pune-7-to-8-years-230326930232
#Key requirements (from listing snippet):
#6+ years strong experience in AI model development
#Expertise in deep learning and computer vision
#
#AI Engineer - Pune - Infinite
#
#Company: Infinite
#Location: Pune
#Experience: 4 to 6 years
#Naukri link: https://www.naukri.com/job-listings-ai-engineer-infinite-pune-4-to-6-years-230326006730
#Key requirements (from listing snippet):
#AI Engineer role in Pune (full description available on the page)
#
#Senior AI Engineer - Pune - Onit
#
#Company: Onit
#Location: Pune
#Experience: 2 to 6 years
#Naukri link: https://www.naukri.com/job-listings-senior-ai-engineer-onit-pune-2-to-6-years-300326500142
#Key requirements (from listing snippet):
#“AI Engineer - 3.5+ Years”
#CTC range shown: 5–15 Lacs (as visible in snippet)
#
#If you want, tell me your experience level (e.g., 1-3, 3-6, 6+ years) and I’ll narrow these to the best matches and list additional fields (education, skills, job type) from the pages.