document
    .getElementById("startupForm")
    .addEventListener(
        "submit",
        async function (e) {

            e.preventDefault();

            const data = {

                name:
                    document.getElementById("name").value,

                sector:
                    document.getElementById("sector").value,

                founding_year:
                    parseInt(
                        document.getElementById(
                            "founding_year"
                        ).value
                    ),

                team_size:
                    parseInt(
                        document.getElementById(
                            "team_size"
                        ).value
                    ),

                revenue_stage:
                    document.getElementById(
                        "revenue_stage"
                    ).value,

                geography:
                    document.getElementById(
                        "geography"
                    ).value,

                description:
                    document.getElementById(
                        "description"
                    ).value
            };

            try {

                const response =
                    await fetch(
                        "http://127.0.0.1:8000/test-score",
                        {
                            method: "POST",
                            headers: {
                                "Content-Type":
                                    "application/json"
                            },
                            body:
                                JSON.stringify(data)
                        }
                    );

                const result =
                    await response.json();

                localStorage.setItem(
                    "startupResult",
                    JSON.stringify(result)
                );

                localStorage.setItem(
                    "startupData",
                    JSON.stringify(data)
                );

                window.location.href =
                    "result.html";

            } catch (err) {

                alert(
                    "Backend connection failed"
                );

                console.error(err);
            }
        }
    );