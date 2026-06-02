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
        ("Market", scores.get("market_score", 0)),
        ("Team", scores.get("team_score", 0)),
        ("Traction", scores.get("traction_score", 0)),
        ("Product", scores.get("product_score", 0)),
        ("Fundability", scores.get("fundability_score", 0))
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

            severity = flag.get("severity")
            message = flag.get("message")

            if severity == "critical":
                pdf.setFillColor(colors.red)
            else:
                pdf.setFillColor(colors.orange)

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
            f"{investor.get("archetype", "Unknown")} | "
            f"Match Score: {investor.get("match_score", 0)} | "
            f"Risk: {investor.get("risk_appetite", "n/A")} | "
            f"Ticket: {investor.get("ticket_size", "N/A")}"
        )

        pdf.drawString(
            60,
            y,
            investor_text
        )

        y -= 18

    # =========================
    # EXECUTIVE SUMMARY
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
        "Executive Summary"
    )

    y -= 25

    fundability = scores.get(
        "fundability_score",
        5
    )

    if fundability >= 8:
        recommendation = "Strong Interest"
    elif fundability >= 6:
        recommendation = "Moderate Interest"
    else:
        recommendation = "High Risk"

    summary_prompt = f"""
You are a venture capital analyst.

Startup:
{startup_data}

Scores:
{scores}

Flags:
{flags}

Write:

Executive Summary:
(2-3 professional sentences)

Key Strengths:
- bullet 1
- bullet 2

Investment Recommendation:
{recommendation}

Reason:
One concise sentence.

No markdown.
Keep under 120 words.
"""

    try:

        summary = ask_gemini(summary_prompt)

        summary = (
            summary
            .replace("**", "")
            .replace("*", "")
            .strip()
        )

    except Exception:

        summary = "Unable to generate AI summary."

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    if recommendation == "Strong Interest":
        pdf.setFillColor(colors.darkgreen)
    elif recommendation == "Moderate Interest":
        pdf.setFillColor(colors.orange)
    else:
        pdf.setFillColor(colors.red)

    pdf.drawString(
        60,
        y,
        f"Recommendation: {recommendation}"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.setFillColor(
        colors.black
    )

    summary_lines = wrap(
        summary,
        width=85
    )

    for line in summary_lines:

        if y < 80:

            pdf.showPage()

            y = height - 60

            pdf.setFont(
                "Helvetica",
                11
            )

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