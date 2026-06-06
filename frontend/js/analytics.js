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
    <div class="score-grid">

        <div class="score-item">
            <strong>Total Reports</strong>
            <p>${data.total_reports}</p>
        </div>

        <div class="score-item">
            <strong>Average Fundability</strong>
            <p>${data.average_fundability}</p>
        </div>

        <div class="score-item">
            <strong>Top Sector</strong>
            <p>${data.top_sector}</p>
        </div>

        <div class="score-item">
            <strong>Highest Startup</strong>
            <p>${data.highest_startup}</p>
        </div>

    </div>
    `;

    renderCharts(
        data
    );
}


function renderCharts(
    data
){

    new Chart(

        document.getElementById(
            "fundabilityChart"
        ),

        {
            type: "bar",

            data: {

                labels:
                    data.startup_names,

                datasets: [

                    {
                        label:
                            "Fundability Score",

                        data:
                            data.fundability_scores
                    }
                ]
            }
        }
    );

    new Chart(

        document.getElementById(
            "sectorChart"
        ),

        {
            type: "pie",

            data: {

                labels:
                    Object.keys(
                        data.sector_distribution
                    ),

                datasets: [

                    {
                        data:
                            Object.values(
                                data.sector_distribution
                            )
                    }
                ]
            }
        }
    );
}

loadAnalytics();