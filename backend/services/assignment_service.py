from backend.repositories import assignment_repo, scenario_repo, trainee_repo

def orchestrate_assignment(req):
    scenario = scenario_repo.get_scenario_by_id(req.scenario_id)
    trainee = trainee_repo.get_trainee_by_id(req.trainee_id)

    assignment_repo.insert_assignment(req.trainee_id, req.scenario_id)

    return {"status": "assigned"}
