from gemini_client import ask_gemini
import json


def analyze_competitors(
    startup_data: dict
):

    prompt = f"""
You are a venture capital analyst.

Startup Name:
{startup_data.get("name")}

Sector:
{startup_data.get("sector")}

Description:
{startup_data.get("description")}

Return ONLY valid JSON.

Format:

{{
    "competitors": [
        "Competitor 1",
        "Competitor 2",
        "Competitor 3"
    ],
    "advantages": [
        "Advantage 1",
        "Advantage 2"
    ],
    "risks": [
        "Risk 1",
        "Risk 2"
    ]
}}
"""

    try:

        response = ask_gemini(
            prompt
        )

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(
            response
        )

    except Exception as e:

        print(
            "Competitor Analysis Error:",
            str(e)
        )

        return {

            "competitors": [],

            "advantages": [],

            "risks": []
        }