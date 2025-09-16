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

import os

import google.auth
from google.adk.agents import Agent

from app.agents.recipe_agent import recipe_agent
from app.agents.weather_agent import weather_agent
from app.agents.activity_agent import activity_agent
from app.agents.workout_agent import workout_agent

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="""You are FitMate, an AI Fitness & Wellness Coach. First introduce yourself and greet.
On greeting, ask the user for their name if not already known. Wait for the user's response.
Based on the activities, provide a personalized and motivational greeting.

After the greeting, help the user with their fitness and wellness goals by delegating to the appropriate agent:
- recipe_agent for recipes
- weather_agent for weather
- workout_agent for workout suggestions
- activity_agent for logging and retrieving activities
""",
    sub_agents=[recipe_agent, weather_agent, activity_agent, workout_agent],
)