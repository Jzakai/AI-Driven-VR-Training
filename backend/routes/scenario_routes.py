from fastapi import APIRouter
from backend.models.scenario_models import GenerateScenarioRequest, SaveScenarioRequest
from backend.services.scenario_service import orchestrate_generate_scenario, orchestrate_save_scenario

router = APIRouter(prefix="/scenario")

@router.post("/generate_scenario")
def generate_scenario(req: GenerateScenarioRequest):
    return orchestrate_generate_scenario(req)

@router.post("/save_scenario")
def save_scenario(req: SaveScenarioRequest):
    return orchestrate_save_scenario(req)
