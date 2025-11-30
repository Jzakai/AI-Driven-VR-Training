#orchestrator

from fastapi import FastAPI
from backend.routes.scenario_routes import router as scenario_router
from backend.routes.assignment_routes import router as assignment_router

app = FastAPI()

app.include_router(scenario_router)
app.include_router(assignment_router)

supabaseUrl = 'https://orxufngqjlljmrahvmgt.supabase.co'
supabaseKey ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9yeHVmbmdxamxsam1yYWh2bWd0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzAyOTkwOCwiZXhwIjoyMDc4NjA1OTA4fQ.oK87M171H-kbhdBGSEZcBBGVpypjbphuqNf5p82stSw'
supabase = createClient(supabaseUrl, supabaseKey)

