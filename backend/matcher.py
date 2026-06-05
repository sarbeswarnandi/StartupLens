import json


def match_investors(
    startup_data: dict,
    scores: dict
):

    try:

        with open(
            "investors.json",
            "r"
        ) as file:

            investors = json.load(file)

    except Exception as e:

        print(
            "Investor file error:",
            str(e)
        )

        return []

    matches = []

    startup_sector = (
        startup_data.get(
            "sector",
            ""
        ).strip()
    )

    startup_stage = (
        startup_data.get(
            "revenue_stage",
            ""
        ).strip()
    )

    startup_geo = (
        startup_data.get(
            "geography",
            ""
        ).strip()
    )

    fundability = (
        scores.get(
            "fundability_score",
            5
        )
    )

    for investor in investors:

        score = 0

        # =========================
        # SECTOR MATCH (40%)
        # =========================

        sectors = investor.get(
            "sectors",
            []
        )

        if (
            startup_sector in sectors
            or
            "Any" in sectors
        ):

            score += 40

        # =========================
        # STAGE MATCH (30%)
        # =========================

        preferred_stages = investor.get(
            "preferred_stage",
            []
        )

        if (
            startup_stage
            in preferred_stages
        ):

            score += 30

        # =========================
        # GEOGRAPHY MATCH (10%)
        # =========================

        geographies = investor.get(
            "geography",
            []
        )

        if (
            startup_geo in geographies
            or
            "Global" in geographies
        ):

            score += 10

        # =========================
        # RISK APPETITE MATCH (20%)
        # =========================

        risk = investor.get(
            "risk_appetite",
            "medium"
        ).lower()

        if fundability >= 8:

            if risk == "low":
                score += 20

        elif fundability >= 6:

            if risk in [
                "medium",
                "high"
            ]:
                score += 20

        else:

            if risk == "high":
                score += 20

        # =========================
        # INVESTOR OBJECT
        # =========================

        matches.append(

            {
                "archetype":
                investor.get(
                    "archetype",
                    "Unknown"
                ),

                "ticket_size":
                investor.get(
                    "ticket_size",
                    "N/A"
                ),

                "risk_appetite":
                investor.get(
                    "risk_appetite",
                    "N/A"
                ),

                "match_score":
                score
            }

        )

    matches.sort(

        key=lambda x:
        x["match_score"],

        reverse=True

    )

    return matches[:3]