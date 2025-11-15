#orchestrator

from fastapi import FastAPI
from backend.routes.scenario_routes import router as scenario_router
from backend.routes.assignment_routes import router as assignment_router

app = FastAPI()

app.include_router(scenario_router)
app.include_router(assignment_router)
