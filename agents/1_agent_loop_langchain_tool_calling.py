from dotenv import load_dotenv   # Loads environment variables from a .env file into the system environment
load_dotenv()  # Load environment variables (e.g., API keys) from the .env file

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from langsmith import traceable

MAX_ITERATIONS = 10  # Maximum number of iterations for the agent loop
MODEL = "llama3.2:latest" # my locally installed ollama model

# ----- Tools (LangChain @tool decorated functions) -----

@tool
def get_product_price(product_name: str) -> float:
    """Tool to get the price of a product from the catalog."""
    # In a real implementation, this would query a database or API.
    # For this example, we'll return a placeholder price.
    print(f"Getting price for product: '{product_name}'")
    prices = {
        "laptop": 999.99,
        "mouse": 29.99,
        "keyboard": 79.99
    }
    return prices.get(product_name, 0)


@tool
def apply_discount(price: float, discount_tier: str) -> float:
    """Tool to apply a discount to a price.
    Available discount tiers: bronze, silver, gold"
    """
    print(f"Applying discount: '{discount_tier}' to price: {price}")
    discounts = {
        "bronze": 0.05,  # 5% discount
        "silver": 0.10,  # 10% discount
        "gold": 0.20     # 20% discount
    }
    discount_rate = discounts.get(discount_tier, 0)
    return round(price * (1 - discount_rate), 2)


# ----- Agent Loop -----
@traceable(name="Langchain Agent Loop")
def run_agent(question: str):
    """Runs the agent loop to answer the question using the defined tools."""
    pass

if __name__ == "__main__":
    # Example question for the agent to answer
    question = "What is the price of a laptop after applying a silver discount?"
    print(f"Question: {question}")
    result = run_agent(question)
    print(f"Final result: {result}")
