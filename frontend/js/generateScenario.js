async function generateScenario() {
    const skill_category = document.getElementById("skill_category").value;
    const skill = document.getElementById("skill").value;
    const difficulty = document.getElementById("difficulty").value;

    const payload = {
        skill_category,
        skill,
        difficulty
    };

    const res = await fetch("http://localhost:8000/scenario/generate_scenario", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    // Show scenario JSON in UI
    document.getElementById("output").textContent =
        JSON.stringify(data.scenario_json, null, 2);
}
