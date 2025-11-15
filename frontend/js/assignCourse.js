async function assignCourse() {
    const trainee_id = document.getElementById("trainee").value;
    const scenario_id = document.getElementById("scenario").value;

    const payload = { trainee_id, scenario_id };

    const res = await fetch("http://localhost:8000/assignment/assign_course", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await res.json();
    alert("Course Assigned!");
}
