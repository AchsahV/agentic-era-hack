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
import re
from google.adk.agents import Agent

def search_recipes(query: str) -> str:
    """Searches for recipes with optional calorie constraints."""
    calorie_constraint = None
    match = re.search(r"(under|less than) (\d+) calories", query, re.IGNORECASE)
    if match:
        calorie_constraint = int(match.group(2))
        query = query.replace(match.group(0), "").strip()

    try:
        search_response = httpx.get(f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1")
        search_response.raise_for_status()
        search_data = search_response.json()

        if "products" not in search_data or not search_data["products"]:
            return f"No recipes found for '{query}'."

        filtered_recipes = []
        for product in search_data["products"][:10]: # Check top 10 results
            product_id = product.get("id")
            if not product_id:
                continue

            product_response = httpx.get(f"https://world.openfoodfacts.org/api/v0/product/{product_id}.json")
            if product_response.status_code != 200:
                continue

            product_data = product_response.json()
            if "product" in product_data and "nutriments" in product_data["product"]:
                nutriments = product_data["product"]["nutriments"]
                calories = nutriments.get("energy-kcal_100g")

                if calories and (not calorie_constraint or calories <= calorie_constraint):
                    product_name = product_data["product"].get("product_name", "N/A")
                    ingredients = product_data["product"].get("ingredients_text", "N/A")
                    filtered_recipes.append(f"- {product_name} ({calories} kcal/100g): {ingredients}")

        if filtered_recipes:
            return "\n".join(filtered_recipes)
        else:
            return f"No recipes found for '{query}' that meet the calorie constraint."

    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

recipe_agent = Agent(
    name="recipe_agent",
    model="gemini-2.5-flash",
    instruction="""You are a Recipe Expert. Your goal is to help users find nutritious meals that support their fitness goals. Use the `search_recipes` tool, and be sure to consider any dietary constraints the user mentions.""",
    tools=[search_recipes],
)
