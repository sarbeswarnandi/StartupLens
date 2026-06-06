const API =
    "http://127.0.0.1:8000";


async function loadAnalytics() {

    const response =
        await fetch(
            `${API}/analytics`
        );

    const data =
        await response.json();

    document.getElementById(
        "analytics"
    ).innerHTML =

    `
    <div class="result-card">

        <h2>
            Total Reports
        </h2>

        <p>
            ${data.total_reports}
        </p>

    </div>

    <div class="result-card">

        <h2>
            Average Fundability
        </h2>

        <p>
            ${data.average_fundability}
        </p>

    </div>

    <div class="result-card">

        <h2>
            Top Sector
        </h2>

        <p>
            ${data.top_sector}
        </p>

    </div>

    <div class="result-card">

        <h2>
            Highest Scoring Startup
        </h2>

        <p>
            ${data.highest_startup}
        </p>

        <p>
            Score:
            ${data.highest_score}
        </p>

    </div>
    `;
}

loadAnalytics();