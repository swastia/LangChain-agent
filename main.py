from agents import langchain_smith_tool_example

def main():
    print("=== Agent Orchestrator ===")
    print("Choose an agent to run:")
    print("1. langchain_smith_tool_example")
    print("2. Search Agent")
    print("3. Audit Agent")

    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        langchain_smith_tool_example.main()
    elif choice == "2":
        print("Search Agent is not implemented yet.")
    elif choice == "3":
        print("Audit Agent is not implemented yet.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()