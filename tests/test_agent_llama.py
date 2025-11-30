from backend.agent.rag_agent_llama import generate_scenario_llama

result = generate_scenario_llama(
    skill_category="Care Under Fire",
    skill="Stop Major Bleeding",
    difficulty="Intermediate"
)

print(result)
