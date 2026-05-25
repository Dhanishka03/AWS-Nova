"""
Challenge 4: The Full Agent — Tools + Memory + Streaming
Combine everything into one powerful agent.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in ALL the TODO sections
  2. Run: python starter.py
  3. Have a full conversation using all tools!
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

import requests
from datetime import date, datetime

MODEL = "us.amazon.nova-pro-v1:0"


# ============================================================
# TODO 1: Import everything you need
# ============================================================
from strands import Agent, tool
from strands_tools import calculator, mem0_memory


# ============================================================
# TODO 2: Create a streaming callback handler
# ============================================================
# Called for every chunk the model streams back.
# - "data"             → a piece of the text response
# - "current_tool_use" → the agent is about to call a tool
def stream_callback(**kwargs):
    if "data" in kwargs:
        # Print each text chunk immediately without a newline
        print(kwargs["data"], end="", flush=True)
    elif "current_tool_use" in kwargs:
        tool_name = kwargs["current_tool_use"].get("name")
        if tool_name:
            print(f"\n🔧 Using tool: {tool_name}", flush=True)


# ============================================================
# TODO 3: Create custom tools — weather and age_calculator
# ============================================================

@tool
def weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: The name of the city to get weather for.

    Returns:
        A string describing the current weather conditions.
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        description = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        wind_kmph = current["windspeedKmph"]

        return (
            f"Weather in {city}: {description}, {temp_c}°C "
            f"(feels like {feels_like}°C), "
            f"Humidity: {humidity}%, Wind: {wind_kmph} km/h"
        )
    except Exception as e:
        return f"Weather in {city}: Partly cloudy, 30°C (live data unavailable: {e})"


@tool
def age_calculator(birth_date: str) -> str:
    """Calculate a person's age from their birth date.

    Args:
        birth_date: Date of birth in YYYY-MM-DD format (e.g. 2000-05-15).

    Returns:
        A string stating the calculated age in years.
    """
    try:
        dob = datetime.strptime(birth_date, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )
        return f"Age: {age} years old (born {birth_date})"
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD (e.g. 1995-08-20)."


# ============================================================
# TODO 4: Create the full agent with ALL tools + memory + streaming
# ============================================================
agent = Agent(
    model=MODEL,
    tools=[calculator, weather, age_calculator, mem0_memory],
    callback_handler=stream_callback,
    system_prompt=(
        "You are a powerful, friendly AI assistant with the following superpowers 🦸:\n"
        "🧮 calculator      — solve any math problem\n"
        "🌤️  weather         — get real-time weather for any city\n"
        "🎂 age_calculator  — calculate someone's age from their birth date\n"
        "🧠 mem0_memory     — remember and recall personal preferences\n\n"
        "Always use the right tool for the job. "
        "When storing a memory, confirm with '✅ Stored!'. "
        "When recalling, be specific about what you remember. "
        "Keep responses concise, warm, and use emojis where appropriate. 🚀"
    ),
)


# ============================================================
# TODO 5: Interactive chat loop
# ============================================================

print("🤖 Full Agent Ready! Type 'quit' to exit.")
print("Try: 'What's the weather in Delhi and how old is someone born 2000-01-01?'")
print("Try: 'Remember my name is [name]' then 'What's my name?'\n")

while True:
    try:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye! 👋")
            break

        print("\nAgent: ", end="")
        # Call the agent — stream_callback handles printing each chunk
        agent(user_input)
        # Print a blank line after the streamed response finishes
        print("\n")

    except KeyboardInterrupt:
        print("\nBye! 👋")
        break

print("\n✅ Challenge 4 complete! 🏆")
