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
# ---- Tool binding to llm objects is only supported by llms that support function calling ----
@traceable(name="Langchain Agent Loop")
def run_agent(question: str):
    tools = [get_product_price, apply_discount]  # List of available tools for the agent
    tools_dict = {tool.name: tool for tool in tools}  # Create a dictionary of tools for easy access
    llm = init_chat_model(f'ollama:{MODEL}', temperature=0)  # Initialize the language model (e.g., LLaMA 3.2)
    llm_with_tools = llm.bind_tools(tools)  # Wrap the language model with the tools
    print(f'Question: {question}')
    print("=" * 60)

    # ---- Brain of the LLM -----
    messages = [
        SystemMessage(
            content=(
                "You are a helpful shopping assistant. "
                "You have access to a product catalog tool and a discount application tool.\n\n"
                "STRICT RULES - you must follow these exacty:\n"
                "1. Never guess or assume any product price."
                "You must ALWAYS call get_product_price to get the price of a product before applying any discount. "
                "2. Only call apply_discount AFTER you have received "
                "the price from get_product_price. Pass the exact price returned by get_product_price - do NOT pass a made-up number.\n"
                "3. NEVER calculate discounts yourself using math. You MUST call the apply_discount tool to get the discounted price."
                "4. If the user does not specify a discount tier, ask them which tier to use - do NOT assume one."
                )
        ),
        HumanMessage(content=question)
    ]

    for iteration in range(MAX_ITERATIONS):
        print(f"\n Iteration {iteration  + 1} of {MAX_ITERATIONS}")

        ai_message = llm_with_tools.invoke(messages)  # Get the AI's response based on the current messages
        tool_calls = ai_message.tool_calls  # Extract any tool calls made by the AI in its response

        print(tool_calls)

        # If no tool calls were made, we assume the AI has provided a final answer and we can return it
        if not tool_calls:
            print("Final Answer:", ai_message.content)
            return ai_message.content

        # Process only the first tool call made by the AI for simplicity
        tool_call = tool_calls[0]
        tool_name = tool_call.get("name")  # Get the name of the tool being called
        tool_args = tool_call.get("args")  # Get the arguments for the tool call
        tools_call_id = tool_call.get("id")  # Get the unique ID for this tool call
        print(f"Tool call detected: {tool_name} with args {tool_args}")
        tool_to_call = tools_dict.get(tool_name)  # Retrieve the actual tool function based on the name
        if not tool_to_call:
            print(f"Error: Tool '{tool_name}' not found.")
            raise ValueError(f"Tool '{tool_name}' not found.")
            return f"Error: Tool '{tool_name}' not found."
        observation = tool_to_call.invoke(tool_args)  # Call the tool with the provided arguments and get the observation/result
        print(f"Observation from tool '{tool_name}': {observation}")

        # Add the AI's message, the tool call, and the observation to the messages for the next iteration
        messages.append(ai_message)  # Add the AI's message to the conversation history
        messages.append(
            ToolMessage(
                content = str(observation),  # Add the observation from the tool call as a ToolMessage
                tool_call_id = tools_call_id  # Associate this observation with the specific tool call ID
            )
        )

    # If we reach the maximum number of iterations without a final answer, return an error message
    print("Error: Maximum iterations reached without a final answer.")
    return None



if __name__ == "__main__":
    # Example question for the agent to answer
    question = "What is the price of a laptop after applying a gold discount?"
    print(f"Question: {question}")
    result = run_agent(question)
    print(f"Final result: {result}")



