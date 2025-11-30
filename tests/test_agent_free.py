from backend.agent.rag_agent_free import generate_scenario_from_agent

result = generate_scenario_from_agent(
    "Care Under Fire", 
    "Major Bleeding Control", 
    "Intermediate"
)

print(result)
