from langgraph.checkpoint.sqlite import SqliteSaver

from src.agent import create_chat_agent


def get_ai_response(username, message):

    print("Entered get_ai_response")
    print("User:", username)
    print("Message:", message)

    with SqliteSaver.from_conn_string("/home/chat_memory.db") as checkpointer:

        print("Creating agent...")
        agent = create_chat_agent(checkpointer)

        print("Invoking agent...")
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
            },
            config={"configurable": {"thread_id": username}},
        )

        print("Agent finished")

        return result["messages"][-1].content


def start_chat():

    print("=" * 45)
    print("          AI AGENT PRO")
    print("=" * 45)

    username = ""

    while not username:
        username = input("Enter your username: ").strip().lower()

    print(f"\nHello {username.capitalize()}!")
    print("Your conversation has been loaded.")
    print("Type 'exit' to quit.\n")

    with SqliteSaver.from_conn_string("/home/chat_memory.db") as checkpointer:

        agent = create_chat_agent(checkpointer)

        while True:

            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:

                print("\nGoodbye!")

                break

            try:
                print("=" * 60)
                print("Invoking agent...")
                print("User:", username)
                print("Question:", user_input)
                print("=" * 60)

                result = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": user_input,
                            }
                        ]
                    },
                    config={"configurable": {"thread_id": username}},
                )

                print("\nAssistant:", result["messages"][-1].content)
                print()

            except Exception as e:

                print("\nERROR:", e)
