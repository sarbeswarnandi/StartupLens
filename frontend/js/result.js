const result =
    JSON.parse(
        localStorage.getItem(
            "startupResult"
        )
    );

if (!result) {

    document.body.innerHTML =
        "<h2>No analysis found</h2>";
}

document.getElementById(
    "fundability"
).innerText =
    result.scores.fundability_score;

document.getElementById(
    "scores"
).innerHTML =

`
Market Score:
${result.scores.market_score}<br>

Team Score:
${result.scores.team_score}<br>

Traction Score:
${result.scores.traction_score}<br>

Product Score:
${result.scores.product_score}
`;

document.getElementById(
    "flags"
).innerHTML =

result.flags
    .map(
        f =>
            `<li>${f.message}</li>`
    )
    .join("");

document.getElementById(
    "investors"
).innerHTML =

result.investors
    .map(
        i =>
            `<li>
                ${i.archetype}
                (Score:
                ${i.match_score})
            </li>`
    )
    .join("");