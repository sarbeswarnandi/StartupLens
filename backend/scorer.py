import json
from gemini_client import ask_gemini


def score_startup(data: dict) -> dict:

    prompt = f"""
You are an AI startup analyst.

Analyze this startup and score from 0–10:

1. market_score
2. team_score
3. traction_score
4. product_score

Startup:

Name: {data.get("name")}
Sector: {data.get("sector")}
Founding Year: {data.get("founding_year")}
Team Size: {data.get("team_size")}
Revenue Stage: {data.get("revenue_stage")}
Geography: {data.get("geography")}
Description: {data.get("description")}

IMPORTANT:
Return only valid JSON.
No markdown.
No explanation.

Format:

{{
    "market_score":0,
    "team_score":0,
    "traction_score":0,
    "product_score":0
}}
"""

    try:

        response = ask_gemini(prompt)

        cleaned = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        print("\nCLEANED RESPONSE:")
        print(cleaned)

        scores = json.loads(cleaned)

        required = [
            "market_score",
            "team_score",
            "traction_score",
            "product_score"
        ]

        for key in required:

            if key not in scores:
                raise Exception(
                    f"Missing key: {key}"
                )

    except Exception as e:

        print(
            "Scoring error:",
            str(e)
        )

        scores = {
            "market_score": 5,
            "team_score": 5,
            "traction_score": 5,
            "product_score": 5
        }

    fundability = (
        scores["market_score"] * 0.3 +
        scores["team_score"] * 0.2 +
        scores["traction_score"] * 0.3 +
        scores["product_score"] * 0.2
    )

    scores["fundability_score"] = round(
        fundability,
        2
    )

    return scores