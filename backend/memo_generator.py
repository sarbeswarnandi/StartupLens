from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from io import BytesIO
from datetime import datetime
from textwrap import wrap

from gemini_client import ask_gemini


def generate_memo(
    startup_data,
    scores,
    flags,
    investors
):

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=letter
    )

    width, height = letter

    y = height - 50

    # =========================
    # HEADER
    # =========================

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.setFillColor(
        colors.darkblue
    )

    pdf.drawString(
        50,
        y,
        "StartupLens"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.setFillColor(
        colors.black
    )

    pdf.drawString(
        50,
        y - 20,
        "AI-powered startup intelligence"
    )

    pdf.drawRightString(
        width - 50,
        y,
        datetime.now().strftime(
            "%d %b %Y"
        )
    )

    y -= 70

    # =========================
    # COMPANY OVERVIEW
    # =========================

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawString(
        50,
        y,
        "Company Overview"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        12
    )

    overview = [

        f"Name: {startup_data.get('name')}",

        f"Sector: {startup_data.get('sector')}",

        f"Stage: {startup_data.get('revenue_stage')}",

        f"Geography: {startup_data.get('geography')}"

    ]

    for item in overview:

        pdf.drawString(
            60,
            y,
            item
        )

        y -= 18

    # =========================
    # DESCRIPTION
    # =========================

    y -= 5

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        60,
        y,
        "Description:"
    )

    y -= 18

    pdf.setFont(
        "Helvetica",
        10
    )

    description_lines = wrap(
        startup_data.get(
            "description",
            ""
        ),
        width=90
    )

    for line in description_lines[:5]:

        pdf.drawString(
            70,
            y,
            line
        )

        y -= 15

    # =========================
    # SCORE BREAKDOWN
    # =========================

    y -= 15

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawString(
        50,
        y,
        "Score Breakdown"
    )

    y -= 30

    score_items = [

        ("Market", scores["market_score"]),
        ("Team", scores["team_score"]),
        ("Traction", scores["traction_score"]),
        ("Product", scores["product_score"]),
        ("Fundability", scores["fundability_score"])

    ]

    for label, value in score_items:

        pdf.setFont(
            "Helvetica",
            11
        )

        pdf.setFillColor(
            colors.black
        )

        pdf.drawString(
            60,
            y + 5,
            f"{label}: {value}"
        )

        # background bar
        pdf.setFillColor(
            colors.lightgrey
        )

        pdf.rect(
            170,
            y,
            200,
            12,
            fill=1
        )

        # score bar
        pdf.setFillColor(
            colors.darkblue
        )

        pdf.rect(
            170,
            y,
            min(value, 10) * 20,
            12,
            fill=1
        )

        y -= 25

    # =========================
    # RED FLAGS
    # =========================

    y -= 10

    pdf.setFillColor(
        colors.black
    )

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawString(
        50,
        y,
        "Red Flags"
    )

    y -= 25

    if not flags:

        pdf.setFillColor(
            colors.green
        )

        pdf.drawString(
            60,
            y,
            "No major risks detected"
        )

        y -= 20

    else:

        for flag in flags:

            severity = flag.get(
                "severity"
            )

            message = flag.get(
                "message"
            )

            if severity == "critical":

                pdf.setFillColor(
                    colors.red
                )

            else:

                pdf.setFillColor(
                    colors.orange
                )

            pdf.drawString(
                60,
                y,
                f"{severity.upper()}: {message}"
            )

            y -= 18

    # =========================
    # INVESTOR FITS
    # =========================

    y -= 10

    pdf.setFillColor(
        colors.black
    )

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawString(
        50,
        y,
        "Top Investor Fits"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    for investor in investors:

        investor_text = (
            f"{investor['archetype']} "
            f"(Score: {investor['match_score']})"
        )

        pdf.drawString(
            60,
            y,
            investor_text
        )

        y -= 18

    # =========================
    # AI VERDICT
    # =========================

    y -= 15

    pdf.setFillColor(
        colors.black
    )

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.drawString(
        50,
        y,
        "AI Verdict"
    )

    y -= 25

    verdict_prompt = f"""
You are a startup investment analyst.

Startup:
{startup_data}

Scores:
{scores}

Flags:
{flags}

Write a concise professional investment verdict in 3 short lines.
Do not use markdown.
"""

    verdict = ask_gemini(
        verdict_prompt
    )

    verdict = (
        verdict
        .replace("**", "")
        .replace("*", "")
        .strip()
    )

    verdict_lines = wrap(
        verdict,
        width=85
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.setFillColor(
        colors.black
    )

    for line in verdict_lines[:6]:

        pdf.drawString(
            60,
            y,
            line
        )

        y -= 18

    # =========================
    # FOOTER
    # =========================

    pdf.setFillColor(
        colors.grey
    )

    pdf.setFont(
        "Helvetica-Oblique",
        9
    )

    pdf.drawString(
        50,
        30,
        "Generated by StartupLens | AI-powered startup intelligence"
    )

    pdf.save()

    buffer.seek(0)

    return buffer.getvalue()