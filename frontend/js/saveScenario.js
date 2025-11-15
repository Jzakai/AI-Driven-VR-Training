async function saveScenario() {
    const scenarioId = document.getElementById("scenario_id").value;
    const jsonText = document.getElementById("scenario_json").value;

    const payload = {
        scenario_id: scenarioId,
        scenario_json: JSON.parse(jsonText),
        skill: document.getElementById("skill").value,
        skill_category: document.getElementById("skill_category").value,
        difficulty: document.getElementById("difficulty").value,
        version: 1,
        edits: null  // add edits later
    };

    const res = await fetch("http://localhost:8000/scenario/save_scenario", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await res.json();
    alert("Scenario Saved!");
}
