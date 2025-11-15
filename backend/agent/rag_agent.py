from textwrap import dedent
from agno.agent import Agent
from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.openai import OpenAIChat
from agno.vectordb.lancedb import LanceDb, SearchType

def generate_scenario_from_agent(skill_category: str, skill: str, difficulty: str):
    """
    Creates a Scenario Generation Agent that:
    - Pulls doctrine knowledge (TCCC, MARCH, etc.) from vector DB
    - Generates ScenarioSpec JSON using admin inputs
    """

    instructions = dedent(f"""
        You are the Scenario Generation Agent for the TACTEX VR system.
        Your job is to generate medically accurate, TCCC-compliant VR training scenarios.

        INPUT PARAMETERS:
        - Skill Category: {skill_category}
        - Skill: {skill}
        - Difficulty Level: {difficulty}

        You MUST:
        1. Retrieve relevant doctrine from the knowledge base (TCCC, MARCH, evacuation protocols)
        2. Use retrieval-augmented generation (RAG) to ensure accuracy
        3. Generate TWO main outputs:
            A. A short mission narrative (~150 words)
            B. A detailed ScenarioSpec JSON with the following structure:

            {{
                "environment": "...",
                "skill_category": "...",
                "skill": "...",
                "difficulty": "...",
                "casualties": [...],
                "injects": [...],
                "objectives": [...],
                "expected_actions": [...],
                "evaluation_metrics": [...]
            }}

        RULES:
        - Follow TCCC standards precisely.
        - Do NOT hallucinate medical steps not in doctrine.
        - Every medical action must be justified using retrieved doctrine.
        - JSON must be valid, strict, and conform to schema.

        Your tone must be factual, concise, and militarily accurate.
    """)

    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        instructions=instructions,
        knowledge=PDFUrlKnowledgeBase(
            urls=[
                # Replace with real TCCC/MARCH PDF storage URLs or direct content
                "https://example.com/TCCC_guidelines.pdf"
            ],
            vector_db=LanceDb(
                uri="tmp/scenario_lancedb",
                table_name="tccc_knowledge",
                search_type=SearchType.hybrid,
                embedder=OpenAIEmbedder(id="text-embedding-3-small"),
            ),
        ),
        markdown=True,
        add_references=True,
    )

    # Load embeddings for RAG
    if agent.knowledge is not None:
        agent.knowledge.load()

    # Return response
    response = agent.run({
        "skill_category": skill_category,
        "skill": skill,
        "difficulty": difficulty
    })

    return response.output

def modify_scenario_with_agent(existing_json, edits):
    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        instructions="Modify the scenario based on edits without changing structure."
    )

    response = agent.run({
        "existing_scenario": existing_json,
        "requested_edits": edits
    })

    return response.output