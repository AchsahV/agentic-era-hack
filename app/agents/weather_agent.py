# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import httpx
from google.adk.agents import Agent

API_KEY = "14c79042ed3ab4c760c79806fff8ff6b"

def get_weather(location: str) -> str:
    """Gets the weather for a given location using the OpenWeather API."""
    try:
        response = httpx.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric")
        response.raise_for_status()
        data = response.json()
        if "weather" in data and data["weather"]:
            description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"The weather in {location} is {description} with a temperature of {temp}°C."
        else:
            return f"Could not get weather for {location}."
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    instruction="""You are a Weather Expert. Your goal is to provide accurate weather forecasts to help users plan their outdoor activities. Use the `get_weather` tool to get the current weather.""",
    tools=[get_weather],
)
