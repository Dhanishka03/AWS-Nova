"""
Challenge 2: Adding Tools to Your Agent
Give your agent a calculator, weather tool, and age calculator.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Needs AWS credentials configured (aws configure)
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

import requests
from datetime import date, datetime
from strands import Agent, tool
from strands_tools import calculator

MODEL = "us.amazon.nova-pro-v1:0"


# ============================================================
# TODO 1: Create a custom weather tool
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
        # Use the wttr.in JSON API for real weather data
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract relevant fields from the API response
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
        # Fallback to dummy data if the API is unreachable
        return f"Weather in {city}: Partly cloudy, 30°C (could not fetch live data: {e})"


# ============================================================
# TODO 2: Create a custom age calculator tool
# ============================================================
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
        # Subtract one year if the birthday hasn't occurred yet this year
        age = today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )
        return f"Age: {age} years old (born {birth_date})"
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD (e.g. 1995-08-20)."


# ============================================================
# TODO 3: Create an agent with all tools
# ============================================================
agent = Agent(
    model=MODEL,
    tools=[calculator, weather, age_calculator],
    system_prompt=(
        "You are a helpful assistant with access to three tools:\n"
        "1. calculator — for any math calculations\n"
        "2. weather    — to get current weather for a city\n"
        "3. age_calculator — to calculate someone's age from their birth date\n"
        "Always use the appropriate tool when the user asks a relevant question. "
        "Be concise and friendly."
    ),
)


# ============================================================
# TODO 4: Test the agent with different questions
# ============================================================

# Test math
print("🧮 Math test:")
response = agent("What is 42 * 17?")
print(response)

# Test weather
print("\n🌤️ Weather test:")
response = agent("What's the weather in Chennai?")
print(response)

# Test age
print("\n🎂 Age test:")
response = agent("How old is someone born on 2000-05-15?")
print(response)

# Bonus: question that uses multiple tools
print("\n🚀 Bonus — multi-tool test:")
response = agent(
    "What is 365 * 24, what's the weather in Mumbai, "
    "and how old is someone born on 1995-03-10?"
)
print(response)

print("\n✅ Challenge 2 complete!")
