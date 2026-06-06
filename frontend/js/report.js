const reportId =
    localStorage.getItem(
        "selectedReportId"
    );

const API =
    "http://127.0.0.1:8000";


async function loadReport(){

    const response =
        await fetch(
            `${API}/report/${reportId}`
        );

    const report =
        await response.json();

    renderReport(
        report
    );
}


function renderReport(
    report
){

    document.getElementById(
        "reportContent"
    ).innerHTML =

    `
    <div class="result-card">

        <h2>
            ${report.startup_data.name}
        </h2>

        <p>
            Sector:
            ${report.startup_data.sector}
        </p>

        <p>
            Geography:
            ${report.startup_data.geography}
        </p>

        <p>
            Fundability:
            ${report.scores.fundability_score}
        </p>

        <h3>
            Scores
        </h3>

        <pre>
${JSON.stringify(
    report.scores,
    null,
    2
)}
        </pre>

        <h3>
            Flags
        </h3>

        <pre>
${JSON.stringify(
    report.flags,
    null,
    2
)}
        </pre>

        <h3>
            Investors
        </h3>

        <pre>
${JSON.stringify(
    report.investors,
    null,
    2
)}
        </pre>

    </div>
    `;
}

loadReport();