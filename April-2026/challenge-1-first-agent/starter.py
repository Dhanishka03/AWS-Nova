"""
Challenge 1: Your First AI Agent
Build a simple agent using Strands SDK + Ollama (runs locally!)

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Make sure 'ollama serve' is running in another terminal
"""

# TODO 1: Import Agent from strands
from strands import Agent

# TODO 2: Import OllamaModel from strands
from strands.models.ollama import OllamaModel


# TODO 3: Create an OllamaModel instance
# Connects to the locally running Ollama server using llama3.2:3b
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="gemma3:270m",
)


# TODO 4: Create an Agent with the ollama_model
# tools=[] because we are not adding any tools in this challenge
agent = Agent(
    model=ollama_model,
    tools=[],
    system_prompt=(
        "You are a helpful and friendly assistant. "
        "Keep your answers brief and easy to understand."
    ),
)


# TODO 5: Ask the agent a question and print the response
print("🤖 Agent: ", end="")
response = agent("Tell me a fun fact about Python programming")
print(response)

# Bonus: ask two more questions to explore the agent
print("\n🤖 Agent: ", end="")
response2 = agent("What is the difference between a list and a tuple in Python?")
print(response2)

print("\n🤖 Agent: ", end="")
response3 = agent("Give me one tip for writing clean Python code.")
print(response3)

print("\n✅ Challenge 1 complete!")
