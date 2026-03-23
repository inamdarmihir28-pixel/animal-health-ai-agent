import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from agent_tools import tools


load_dotenv()

# Initialize chat model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Build Tool-Aware Agent (LangChain 1.x API)
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful assistant that uses tools when needed.",
    debug=False,
)


if __name__ == "__main__":
    prompts = [
        "What is 12 * (7+3)?",
        "Tell me a joke about robots.",
        "Where is Paris located?",
    ]

    for p in prompts:
        print("\nQ:", p)
        result = agent.invoke({"messages": [{"role": "user", "content": p}]})
        final_msg = result["messages"][-1].content
        print("A:", final_msg)
