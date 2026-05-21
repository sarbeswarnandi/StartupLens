def detect_flags(
    data: dict,
    scores: dict
):

    flags = []


    team_size = data.get(
        "team_size",
        0
    )

    founding_year = data.get(
        "founding_year",
        2025
    )

    revenue_stage = data.get(
        "revenue_stage",
        ""
    )

    description = data.get(
        "description",
        ""
    )

    sector = data.get(
        "sector",
        ""
    )


    # Rule 1
    if team_size == 1:

        flags.append(

            {
                "severity":"warning",

                "message":
                "Solo founder risk"
            }

        )


    # Rule 2

    if (
        founding_year < 2021
        and
        revenue_stage
        ==
        "pre-revenue"
    ):

        flags.append(

            {
                "severity":"critical",

                "message":
                "Old startup with no revenue traction"
            }

        )


    # Rule 3

    score_keys = [

        "market_score",

        "team_score",

        "traction_score",

        "product_score"

    ]


    for key in score_keys:

        if scores.get(
            key,
            5
        ) < 4:

            readable = (
                key
                .replace(
                    "_score",
                    ""
                )
            )

            flags.append(

                {
                    "severity":
                    "warning",

                    "message":
                    f"Low {readable} score"
                }

            )


    # Rule 4

    if (
        scores.get(
            "fundability_score",
            5
        )
        <5
    ):

        flags.append(

            {
                "severity":
                "critical",

                "message":
                "Low overall fundability"
            }

        )


    # Rule 5

    if len(
        description
    ) < 50:

        flags.append(

            {
                "severity":
                "warning",

                "message":
                "Insufficient product description"
            }

        )


    # Rule 6

    if (
        sector=="B2C"
        and
        scores.get(
            "market_score",
            5
        ) <6
    ):

        flags.append(

            {
                "severity":
                "warning",

                "message":
                "Highly competitive B2C space"
            }

        )


    return flags