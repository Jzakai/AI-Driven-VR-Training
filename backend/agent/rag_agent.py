
from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat, OpenAIEmbeddings
from agno.knowledge.loaders.file_loader import FileLoader

from agno.knowledge import KnowledgeBase
from agno.vectordb.lancedb import LanceDB
from agno.vectordb.search import SearchType

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

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

    # Knowledge Base
    kb = KnowledgeBase(
        loaders=[PDFReader("backend/protocols/TCCC_guidelines.pdf")],
        vector_db=LanceDB(
            uri="tmp/scenario_lancedb",
            table_name="tccc_knowledge",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbeddings(model="text-embedding-3-small"),
        )
    )

    # Load PDF + create embeddings if not already embedded
    kb.load()

   # Agent
    agent = Agent(
        model=OpenAIChat(model="gpt-4o-mini"),
        instructions=instructions,
        knowledge=kb,
        markdown=True,
        add_references=True,
    )

    # Return response
    response = agent({
        "skill_category": skill_category,
        "skill": skill,
        "difficulty": difficulty
    })

    return response.output

def modify_scenario_with_agent(existing_json, edits):
    agent = Agent(
       model=OpenAIChat(model="gpt-4o-mini"),
        instructions="Modify the scenario based on edits without changing structure."
    )

    response = agent({
        "existing_scenario": existing_json,
        "requested_edits": edits
    })

    return response.output