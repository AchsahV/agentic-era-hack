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
from google.cloud import bigquery
import google.auth

_, project_id = google.auth.default()

def get_activity_streak(user_name: str) -> str:
    """Calculates the user's activity streak from BigQuery."""
    client = bigquery.Client()
    query = f"""
        WITH dates AS (
            SELECT DISTINCT date
            FROM `{project_id}.fitmate_data.activities`
            WHERE user_name = '{user_name}'
        ),
        date_groups AS (
            SELECT
                date,
                DATE_DIFF(date, LAG(date, 1, date) OVER (ORDER BY date), DAY) as diff
            FROM dates
        ),
        streaks AS (
            SELECT
                date,
                COUNTIF(diff > 1) OVER (ORDER BY date) as streak_group
            FROM date_groups
        )
        SELECT COUNT(*) as streak_length
        FROM streaks
        GROUP BY streak_group
        ORDER BY streak_length DESC
        LIMIT 1
    """
    query_job = client.query(query)
    results = list(query_job)
    if results:
        return f"Your current activity streak is {results[0].streak_length} days."
    else:
        return "You don't have an activity streak yet. Let's start one today!"

def get_user_badges(user_name: str) -> str:
    """Gets the user's badges from BigQuery."""
    client = bigquery.Client()
    query = f"""
        SELECT badge
        FROM `{project_id}.fitmate_data.activities`,
        UNNEST(badges) as badge
        WHERE user_name = '{user_name}'
    """
    query_job = client.query(query)
    badges = [row.badge for row in query_job]
    if badges:
        return f"Your badges: {', '.join(set(badges))}"
    else:
        return "You haven't earned any badges yet."

def award_badge(user_name: str, badge_name: str) -> str:
    """Awards a badge to a user by updating the latest activity record in BigQuery."""
    client = bigquery.Client()
    # First, find the latest activity for the user
    query = f"""
        SELECT date, details
        FROM `{project_id}.fitmate_data.activities`
        WHERE user_name = '{user_name}'
        ORDER BY date DESC
        LIMIT 1
    """
    query_job = client.query(query)
    results = list(query_job)
    if not results:
        return "Cannot award badge: no activities found for the user."

    latest_activity = results[0]
    # Now, update the record to add the badge
    update_query = f"""
        UPDATE `{project_id}.fitmate_data.activities`
        SET badges = ARRAY_CONCAT(badges, ['{badge_name}'])
        WHERE user_name = '{user_name}' AND date = '{latest_activity.date}' AND details = '{latest_activity.details}'
    """
    update_job = client.query(update_query)
    update_job.result() # Wait for the job to complete
    return f"Awarded badge: {badge_name}"

gamification_agent = Agent(
    name="gamification_agent",
    model="gemini-2.5-flash",
    instruction="""You are a Gamification Expert. Your goal is to motivate users by tracking their progress with streaks and badges. Use the `get_activity_streak`, `get_user_badges`, and `award_badge` tools to create a fun and engaging experience.""",
    tools=[get_activity_streak, get_user_badges, award_badge],
)
