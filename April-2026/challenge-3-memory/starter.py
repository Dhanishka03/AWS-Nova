"""
Challenge 3: Agent with Persistent Memory
Give your agent memory that survives restarts using FAISS.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Store some facts, then quit and restart to verify persistence
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from strands import Agent

MODEL = "us.amazon.nova-pro-v1:0"


# ============================================================
# TODO 1: Import mem0_memory from strands_tools
# ============================================================
# mem0_memory uses FAISS under the hood to store facts as vectors
# on disk — so memories persist even after the program exits.
from strands_tools import mem0_memory


# ============================================================
# TODO 2: Create an agent with mem0_memory tool
# ============================================================
agent = Agent(
    model=MODEL,
    tools=[mem0_memory],
    system_prompt=(
        "You are a helpful personal assistant with persistent memory. "
        "When the user asks you to remember something, use the mem0_memory tool "
        "to store that information. "
        "When the user asks about something they told you before, use the "
        "mem0_memory tool to search and recall it. "
        "Always confirm when you have stored a memory with a friendly message like "
        "'✅ Got it, I'll remember that!'. "
        "Be warm, concise, and helpful."
    ),
)


# ============================================================
# TODO 3: Interactive loop — chat with the memory agent
# ============================================================

print("🧠 Memory Agent Ready!")
print("Try: 'Remember that my name is [your name] and I love [food]'")
print("Then: 'What's my name and what food do I like?'")
print("Quit and restart to verify memories persist across sessions.")
print("Type 'quit' to exit.\n")

while True:
    try:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye! 👋")
            break

        # Send user_input to the agent and print the response
        response = agent(user_input)
        print(f"Agent: {response}\n")

    except KeyboardInterrupt:
        print("\nBye! 👋")
        break

print("\n✅ Challenge 3 complete!")
