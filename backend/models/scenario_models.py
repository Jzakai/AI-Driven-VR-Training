from pydantic import BaseModel
from typing import Dict

class GenerateScenarioRequest(BaseModel):
    skill_category: str
    skill: str
    difficulty: str


class SaveScenarioRequest(BaseModel):
    scenario_id: str | None = None
    scenario_json: Dict
    skill: str
    skill_category: str
    difficulty: str
    version: int
    edits: Dict | None = None
    course_name: str


class EditScenarioRequest(BaseModel):
    edits: str

