from textwrap import dedent
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import LanceDB

import lancedb

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ------------------------------------------------------------------
# Knowledge Base (FREE embeddings)
# ------------------------------------------------------------------
def load_knowledge_base():
    pdf_path = "backend/protocols/TCCC_guidelines.pdf"
    db_uri = "tmp/lancedb_free"
    table_name = "tccc_knowledge_free"

    # FREE embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    # Connect to LanceDB
    db = lancedb.connect(db_uri)

    if table_name in db.table_names():
        print(" Loading CACHED FREE LanceDB")
        vectordb = LanceDB(
            embedding=embeddings,
            uri=db_uri,
            table_name=table_name,
        )
        return vectordb.as_retriever(search_kwargs={"k": 5})

    # Build table once
    print(" Building FREE LanceDB vectorstore (this happens one time).")

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    vectordb = LanceDB.from_documents(
        documents=docs,
        embedding=embeddings,
        uri=db_uri,
        table_name=table_name,
    )

    return vectordb.as_retriever(search_kwargs={"k": 5})


# ------------------------------------------------------------------
# Scenario Generation Agent (FREE LLaMA)
# ------------------------------------------------------------------
def generate_scenario_llama(skill_category: str, skill: str, difficulty: str):

    instructions = dedent(f"""
        You are the Scenario Generation Agent for the TACTEX VR system.
        Your job is to generate medically accurate, TCCC-compliant VR training scenarios.

        INPUT PARAMETERS:
        - Skill Category: {skill_category}
        - Skill: {skill}
        - Difficulty Level: {difficulty}

        You MUST:
        1. Retrieve relevant doctrine from the knowledge base.
        2. Use retrieval-augmented generation (RAG) to ensure accuracy.
        3. Generate TWO outputs:
            A. A short mission narrative (~150 words)
            B. A detailed ScenarioSpec JSON with this structure:

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
        - Follow TCCC strictly.
        - Do NOT hallucinate medical procedures.
        - JSON must be valid.
    """)

    retriever = load_knowledge_base()

    # FREE inference
    llm = ChatGroq(
        model="gemma2-9b-it",
        temperature=0.2,
        api_key=GROQ_API_KEY
    )

    # Manual RAG pipeline
    docs = retriever.get_relevant_documents(instructions)
    context = "\n\n".join([d.page_content for d in docs])

    final_prompt = f"""
    Use ONLY this retrieved context:

    {context}

    Now answer the following:
    {instructions}
    """

    return llm.invoke(final_prompt).content
