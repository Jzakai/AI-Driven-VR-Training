from backend.agent.rag_agent_openrouter import generate_scenario_from_agent

result = generate_scenario_from_agent(
    skill_category="Care Under Fire",
    skill="Stop Major Bleeding",
    difficulty="Intermediate"
)

print(result)
