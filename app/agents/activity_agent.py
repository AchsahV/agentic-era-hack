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

from datetime import date, timedelta
from google.adk.agents import Agent
from google.adk.tools import ToolContext

def log_activity(user_name: str, activity_type: str, details: str, tool_context: ToolContext) -> str:
    """Logs a user's activity in the session state."""
    if f"user:activities" not in tool_context.state:
        tool_context.state[f"user:activities"] = []
    tool_context.state[f"user:activities"].append(f"{activity_type}: {details}")
    return f"Logged '{details}' as a {activity_type} for {user_name}."

def get_past_activities(user_name: str, tool_context: ToolContext) -> str:
    """Gets a user's past activities from the session state."""
    activities = tool_context.state.get(f"user:activities", [])
    if activities:
        return f"Here are the recent activities for {user_name}:\n" + "\n".join(activities)
    else:
        return "- run: 5km"

activity_agent = Agent(
    name="activity_agent",
    model="gemini-2.5-flash",
    instruction="""You are an Activity Tracking Expert. Your goal is to help users log their daily activities and retrieve their past performance from the session state. Use the `log_activity` and `get_past_activities` tools to manage user activities.""",
    tools=[log_activity, get_past_activities],
)
