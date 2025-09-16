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

import json
from pathlib import Path
from google.adk.agents import Agent
from google.adk.tools import ToolContext

ACTIVITIES_FILE = Path(__file__).parent.parent / "data" / "user_activities.json"

def _read_activities() -> dict:
    if not ACTIVITIES_FILE.exists():
        return {}
    with open(ACTIVITIES_FILE, "r") as f:
        return json.load(f)

def _write_activities(data: dict):
    with open(ACTIVITIES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_activity(user_name: str, activity_type: str, details: str, tool_context: ToolContext) -> str:
    """Logs a user's activity in a file."""
    activities = _read_activities()
    if user_name not in activities:
        activities[user_name] = []
    activities[user_name].append(f"{activity_type}: {details}")
    _write_activities(activities)
    return f"Logged '{details}' as a {activity_type} for {user_name}."

def get_past_activities(user_name: str, tool_context: ToolContext) -> str:
    """Gets a user's past activities from a file."""
    activities = _read_activities()
    user_activities = activities.get(user_name, [])
    if user_activities:
        return f"Here are the recent activities for {user_name}:\n" + "\n".join(user_activities)
    else:
        return f"No past activities found for {user_name}. Let's get started!"

activity_agent = Agent(
    name="activity_agent",
    model="gemini-2.5-flash",
    instruction="""You are an Encouraging Activity Tracking Expert. Your goal is to check if the user exists in the activity files,if exists retrieve their past performance from a file else log their activity details. Use the `log_activity` and `get_past_activities` tools to manage user activities.""",
    tools=[log_activity, get_past_activities],
)