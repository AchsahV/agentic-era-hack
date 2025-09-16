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

from google.adk.agents import Agent
from app.data.workouts import find_workouts, get_all_workouts

workout_agent = Agent(
    name="workout_agent",
    model="gemini-2.5-flash",
    instruction="""You are a friendly and encouraging personal trainer. Your goal is to help the user find the perfect workout for them today.

1.  Start by asking the user some questions to understand their needs. For example: \"How are you feeling today?\", \"How much time do you have for a workout?\", or \"Are you in the mood for something high-energy or something more relaxing?\", or \"What difficulty level are you looking for (Beginner, Intermediate, Advanced)?\".

2.  Based on the user's answers, use the find_workouts tool to find suitable workouts from the library.

3.  Suggest one or two workouts to the user and explain why you are suggesting them. For example: \"Since you're feeling energetic and have 30 minutes, I'd recommend the 'HIIT Cardio' session. It's a great way to get your heart rate up. Or, if you'd prefer something to build strength, the 'Full Body Strength' workout is a great option.\"

4.  You MUST only suggest workouts from the workout library.""",
    tools=[find_workouts, get_all_workouts],
)
