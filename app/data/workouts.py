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

from typing import Optional

WORKOUTS = [
    {
        "name": "Morning Yoga",
        "type": "Yoga",
        "duration": 15,
        "difficulty": "Beginner",
        "description": "A gentle yoga routine to start your day."
    },
    {
        "name": "HIIT Cardio",
        "type": "Cardio",
        "duration": 20,
        "difficulty": "Intermediate",
        "description": "A high-intensity interval training session to get your heart rate up."
    },
    {
        "name": "Full Body Strength",
        "type": "Strength",
        "duration": 45,
        "difficulty": "Advanced",
        "description": "A challenging workout to build strength in all major muscle groups."
    },
    {
        "name": "Evening Stretch",
        "type": "Stretching",
        "duration": 10,
        "difficulty": "Beginner",
        "description": "A relaxing stretching routine to wind down before bed."
    },
    {
        "name": "30-Minute Run",
        "type": "Cardio",
        "duration": 30,
        "difficulty": "Intermediate",
        "description": "A steady-state run to improve your cardiovascular endurance."
    }
]

def find_workouts(type: Optional[str] = None, duration: Optional[int] = None, difficulty: Optional[str] = None) -> list:
    """Finds workouts based on type, duration, and difficulty."""
    results = []
    for workout in WORKOUTS:
        if type and workout["type"].lower() != type.lower():
            continue
        if duration and workout["duration"] > duration:
            continue
        if difficulty and workout["difficulty"].lower() != difficulty.lower():
            continue
        results.append(workout)
    return results

def get_all_workouts() -> list:
    """Returns all workouts."""
    return WORKOUTS