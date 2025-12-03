from backend.agent.rag_agent import generate_scenario_from_agent, modify_scenario_with_agent
from backend.repositories import scenario_repo
from backend.utils.schema_validator import validate_scenario_schema

def orchestrate_generate_scenario(req):
    scenario_json = generate_scenario_from_agent(
        req.skill_category, req.skill, req.difficulty
    )

    validate_scenario_schema(scenario_json)

    scenario_id = scenario_repo.save_scenario(
        scenario_json,
        req.skill,
        req.skill_category,
        req.difficulty,
        version=1,
    
    )

    return {
        "scenario_id": scenario_id,
        "scenario_json": scenario_json,
        "skill": req.skill,
        "skill_category": req.skill_category,
        "difficulty": req.difficulty,
        "version": 1,
    }


def orchestrate_save_scenario(req):
    validate_scenario_schema(req.scenario_json)

    updated_json = req.scenario_json

    if req.edits:
        updated_json = modify_scenario_with_agent(req.scenario_json, req.edits)
        validate_scenario_schema(updated_json)

    scenario_repo.save_scenario(
        updated_json,
        req.skill,
        req.skill_category,
        req.difficulty,
        req.version,
        req.course_name

    )

    return {"status": "Saved", "scenario_id": req.scenario_id}


def orchestrate_edit_scenario(req):

    if req.edits:
        updated_json = modify_scenario_with_agent(req.scenario_json, req.edits)
        validate_scenario_schema(updated_json)

    scenario_repo.save_scenario(
        updated_json,
        req.skill,
        req.skill_category,
        req.difficulty,
        req.version,
        req.course_name

    )

    return {"status": "Saved", "scenario_id": req.scenario_id}