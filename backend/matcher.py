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
        )
    )


    startup_stage = (
        startup_data.get(
            "revenue_stage",
            ""
        )
    )


    startup_geo = (
        startup_data.get(
            "geography",
            ""
        )
    )


    fundability = (
        scores.get(
            "fundability_score",
            5
        )
    )



    for investor in investors:

        score = 0


        # sector match
        if (
            startup_sector in investor["sectors"]
            or
            "Any" in investor["sectors"]
        ):

            score += 2


        # stage match
        if (
            startup_stage
            in investor[
                "preferred_stage"
            ]
        ):

            score += 2


        # geography match
        if (
            startup_geo
            in investor[
                "geography"
            ]

            or

            "Global"
            in investor[
                "geography"
            ]
        ):

            score += 1


        # risk appetite match

        risk = investor[
            "risk_appetite"
        ]


        if (
            fundability < 5
            and
            risk == "high"
        ):

            score += 1


        elif (
            fundability >= 5
            and
            risk != "low"
        ):

            score += 1


        # clean response object
        matches.append(

            {
                "archetype":
                investor[
                    "archetype"
                ],

                "ticket_size":
                investor[
                    "ticket_size"
                ],

                "risk_appetite":
                investor[
                    "risk_appetite"
                ],

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