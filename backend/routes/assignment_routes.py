from fastapi import APIRouter
from backend.services.assignment_service import orchestrate_assignment
from pydantic import BaseModel

router = APIRouter(prefix="/assignment")

class AssignRequest(BaseModel):
    trainee_id: str
    scenario_id: str

@router.post("/assign_course")
def assign_course(req: AssignRequest):
    return orchestrate_assignment(req)
