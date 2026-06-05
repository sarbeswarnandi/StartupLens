const result =
    JSON.parse(
        localStorage.getItem(
            "startupResult"
        )
    );

const startupData =
    JSON.parse(
        localStorage.getItem(
            "startupData"
        )
    );

if (!result) {

    document.body.innerHTML = `
        <div class="container">
            <h1>No Analysis Found</h1>

            <button
                onclick="window.location.href='index.html'">

                Go Back
            </button>
        </div>
    `;

    throw new Error(
        "No startup result found"
    );
}


/* ==========================
   Fundability Score
========================== */

document.getElementById(
    "fundability"
).innerText =
    result.scores.fundability_score;

    const fundability =
    result.scores.fundability_score;

const badge =
    document.getElementById(
        "recommendationBadge"
    );

if (fundability >= 8) {

    badge.innerText =
        "🟢 Strong Interest";

    badge.classList.add(
        "recommendation-strong"
    );

}
else if (fundability >= 6) {

    badge.innerText =
        "🟡 Moderate Interest";

    badge.classList.add(
        "recommendation-moderate"
    );

}
else {

    badge.innerText =
        "🔴 High Risk";

    badge.classList.add(
        "recommendation-risk"
    );

}


/* ==========================
   Detailed Scores
========================== */

document.getElementById(
    "scores"
).innerHTML =

`
<div class="score-grid">

    <div class="score-item">
        <strong>Market Score</strong>
        <p>${result.scores.market_score}/10</p>
    </div>

    <div class="score-item">
        <strong>Team Score</strong>
        <p>${result.scores.team_score}/10</p>
    </div>

    <div class="score-item">
        <strong>Traction Score</strong>
        <p>${result.scores.traction_score}/10</p>
    </div>

    <div class="score-item">
        <strong>Product Score</strong>
        <p>${result.scores.product_score}/10</p>
    </div>

</div>
`;


/* ==========================
   Risk Flags
========================== */

const flagsContainer =
    document.getElementById(
        "flags"
    );

if (
    !result.flags ||
    result.flags.length === 0
) {

    flagsContainer.innerHTML =
        "<li>No major risk flags detected.</li>";

} else {

    flagsContainer.innerHTML =
        result.flags
            .map(
                flag =>

                `<li class="flag-${flag.severity}">
                    <strong>
                        ${flag.severity.toUpperCase()}
                    </strong>
                    :
                    ${flag.message}
                </li>`
            )
            .join("");
}


/* ==========================
   Investor Matches
========================== */

const investorContainer =
    document.getElementById(
        "investors"
    );

if (
    !result.investors ||
    result.investors.length === 0
) {

    investorContainer.innerHTML =
        "<li>No investor matches found.</li>";

} else {

    investorContainer.innerHTML =
    result.investors
        .map(
            investor =>

            `
            <li class="investor-card">

                <div class="investor-name">
                    ${investor.archetype}
                </div>

                <div class="investor-score">
                    ${investor.match_score}%
                </div>

                <div class="investor-details">
                    Risk: ${investor.risk_appetite}
                    <br>
                    Ticket: ${investor.ticket_size}
                </div>

            </li>
            `
        )
        .join("");
}


/* ==========================
   PDF Download
========================== */

document
    .getElementById(
        "downloadMemo"
    )
    .addEventListener(
        "click",
        async () => {

            try {

                const button =
                    document.getElementById(
                        "downloadMemo"
                    );

                button.disabled = true;

                button.innerText =
                    "Generating PDF...";

                const response =
                    await fetch(
                        "http://127.0.0.1:8000/generate-memo",
                        {
                            method: "POST",
                            headers: {
                                "Content-Type":
                                    "application/json"
                            },
                            body:
                                JSON.stringify(
                                    startupData
                                )
                        }
                    );

                if (
                    !response.ok
                ) {

                    throw new Error(
                        "PDF generation failed"
                    );
                }

                const blob =
                    await response.blob();

                const url =
                    window.URL.createObjectURL(
                        blob
                    );

                const link =
                    document.createElement(
                        "a"
                    );

                link.href = url;

                link.download =
                    "startup_memo.pdf";

                document.body.appendChild(
                    link
                );

                link.click();

                link.remove();

                window.URL.revokeObjectURL(
                    url
                );

                button.disabled = false;

                button.innerText =
                    "📄 Download Investment Memo";

            } catch (error) {

                console.error(
                    error
                );

                alert(
                    "Failed to generate PDF."
                );

                document.getElementById(
                    "downloadMemo"
                ).innerText =
                    "📄 Download Investment Memo";
            }
        }
    );