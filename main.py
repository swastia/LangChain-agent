from dotenv import load_dotenv
import os
load_dotenv()

def main():
    print("Hello from langchain-agent!")
    print("Your OPENAI_API_KEY is:", os.getenv("OPENAI_API_KEY"))


if __name__ == "__main__":
    main()
