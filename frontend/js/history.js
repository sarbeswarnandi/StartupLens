const API =
    "http://127.0.0.1:8000";


async function loadReports() {

    try {

        const response =
            await fetch(
                `${API}/reports`
            );

        const reports =
            await response.json();

        renderReports(
            reports
        );

    } catch (error) {

        console.error(
            error
        );

        document.getElementById(
            "historyContainer"
        ).innerHTML =
            "<p>Failed to load reports.</p>";
    }
}


async function searchReports() {

    const name =
        document
        .getElementById(
            "searchInput"
        )
        .value
        .trim();

    if (!name) {

        loadReports();

        return;
    }

    try {

        const response =
            await fetch(
                `${API}/reports/${name}`
            );

        const reports =
            await response.json();

        renderReports(
            reports
        );

    } catch (error) {

        console.error(
            error
        );

        document.getElementById(
            "historyContainer"
        ).innerHTML =
            "<p>Search failed.</p>";
    }
}


function viewReport(
    reportId
) {

    localStorage.setItem(
        "selectedReportId",
        reportId
    );

    window.location.href =
        "report.html";
}


async function deleteReport(
    reportId
) {

    const confirmed =
        confirm(
            "Delete this report?"
        );

    if (!confirmed) {

        return;
    }

    try {

        const response =
            await fetch(
                `${API}/report/${reportId}`,
                {
                    method: "DELETE"
                }
            );

        const result =
            await response.json();

        if (
            result.error
        ) {

            alert(
                result.error
            );

            return;
        }

        loadReports();

    } catch (error) {

        console.error(
            error
        );

        alert(
            "Failed to delete report."
        );
    }
}


function renderReports(
    reports
) {

    const container =
        document.getElementById(
            "historyContainer"
        );

    if (
        !reports ||
        reports.length === 0
    ) {

        container.innerHTML =
            "<p>No reports found.</p>";

        return;
    }

    container.innerHTML =
        reports
            .map(
                report =>

                `
                <div class="result-card">

                    <h3>
                        ${report.startup_data?.name || "Unknown Startup"}
                    </h3>

                    <p>
                        <strong>Sector:</strong>
                        ${report.startup_data?.sector || "N/A"}
                    </p>

                    <p>
                        <strong>Fundability:</strong>
                        ${report.scores?.fundability_score || 0}
                    </p>

                    <p>
                        <strong>Created:</strong>
                        ${
                            report.created_at
                                ? new Date(
                                      report.created_at
                                  ).toLocaleString(
                                      "en-IN",
                                      {
                                          timeZone: "Asia/Kolkata"
                                      }
                                  )
                                : "N/A"
                        }
                    </p>

                    <div class="report-actions">

                        <button
                            onclick="viewReport('${report._id}')"
                            class="view-btn">

                            📄 View Full Report

                        </button>

                        <button
                            onclick="deleteReport('${report._id}')"
                            class="delete-btn">

                            🗑 Delete Report

                        </button>

                    </div>

                </div>
                `
            )
            .join("");
}


loadReports();