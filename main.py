# Importing required packages

from dotenv import load_dotenv   # Loads environment variables from a .env file into the system environment
import os                        # Standard Python library for interacting with the operating system (not directly used here)
from langchain_core.prompts import PromptTemplate  # LangChain class for creating structured prompts with placeholders

from langchain_openai import ChatOpenAI   # LangChain wrapper for OpenAI chat models (like GPT-4)
from openai import OpenAI                 # Official OpenAI Python SDK (imported but not used in this script)

# Load environment variables (e.g., API keys) from the .env file
load_dotenv()

# Define the main function that will run when the script is executed
def main():
    print("Hello from langchain-agent!")  # Simple greeting to confirm execution

    # Multi-line string containing biographical information about Elon Musk
    information = """ Elon Reeve Musk (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a businessman and entrepreneur known for his leadership of Tesla, SpaceX, X, and xAI. Musk has been the wealthiest person in the world since 2025; as of February 2026, Forbes estimates his net worth to be around US$852 billion.
    ... (rest of biography text omitted for brevity) ...
    """

    # Template for summarizing the information in a structured format
    summary_template = """ given the information about a person I want you to summarize the information in a few sentences. The information is: {information}. Give respone in below format:
    1. Name: 
    2. Occupation:
    3. short summary:
    4. two interesting facts:
    """

    # Create a PromptTemplate object
    # - template: the text defined above
    # - input_variables: list of placeholders that will be replaced dynamically
    summary_prompt_template = PromptTemplate(
        template=summary_template,
        input_variables=["information"]
    )

    # Initialize the ChatOpenAI model
    # - model: specifies which OpenAI model to use
    # - temperature: controls randomness (0 = deterministic, consistent output)
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Create a chain by piping the prompt into the model
    # This means: input → prompt → LLM → output
    chain = summary_prompt_template | llm

    # Execute the chain with the biography text as input
    # - invoke runs the pipeline and returns the model’s response
    response = chain.invoke(input={"information": information})

    # Print the AI-generated summary to the console
    print(response.content)


# Standard Python entry point
# Ensures main() runs only when the script is executed directly, not when imported
if __name__ == "__main__":
    main()

## Output: with gpt-4 model
#Hello from langchain-agent!
#1. Name: Elon Reeve Musk
#2. Occupation: Businessman, Entrepreneur, CEO of Tesla and SpaceX
#3. Short Summary: Elon Musk, born in South Africa and holding Canadian and American citizenship, is a renowned businessman and entrepreneur. He is the CEO of Tesla and SpaceX, and has been the world's wealthiest person since 2025. Musk has co-founded several successful companies including Zip2, X.com (which later became PayPal), OpenAI, and Neuralink. He also founded the Boring Company and acquired Twitter in 2022, rebranding it as X. Despite his business success, Musk's political activities and controversial statements have made him a polarizing figure.4. Two Interesting Facts:
#   - Musk was the largest donor in the 2024 U.S. presidential election, supporting Donald Trump, and served as Senior Advisor to the President and the de facto head of the Department of Government Efficiency (DOGE) in 2025. 
#   - In November 2025, a Tesla pay package worth $1 trillion for Musk was approved, which he is to receive over 
#10 years if he meets specific goals.