from textwrap import dedent
import os
from dotenv import load_dotenv

# LangChain Imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import LanceDB
from langchain.chains import RetrievalQA


# Load env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ------------------------------------------------------------------
# Build Knowledge Base (PDF → Embeddings → LanceDB)
# ------------------------------------------------------------------
def load_knowledge_base():
    import lancedb
    pdf_path = "backend/protocols/TCCC_guidelines.pdf"
    db_uri = "tmp/lancedb"
    table_name = "tccc_knowledge"

    # Connect or create DB
    db = lancedb.connect(db_uri)

    # Embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPENAI_API_KEY
    )

    # --- CHECK IF TABLE EXISTS (LOAD CACHED DB) ---
    if table_name in db.table_names():
        print("📌 Loading CACHED LanceDB table — no embedding cost.")
        vectordb = LanceDB(
            embedding=embeddings,
            uri=db_uri,
            table_name=table_name,
        )
        return vectordb.as_retriever(search_kwargs={"k": 5})

    # --- FIRST TIME: BUILD DB ---
    print("Table not found — Building vector DB (this happens once).")

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    vectordb = LanceDB.from_documents(
        documents=documents,
        embedding=embeddings,
        uri=db_uri,
        table_name=table_name,
    )

    return vectordb.as_retriever(search_kwargs={"k": 5})


# ------------------------------------------------------------------
# Scenario Generation Agent
# ------------------------------------------------------------------
def generate_scenario_from_agent(skill_category: str, skill: str, difficulty: str):

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

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=OPENAI_API_KEY
    )


    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )

    # Run RAG chain
    result = chain.run(instructions)

    return result


# ------------------------------------------------------------------
# Modify Scenario Agent
# ------------------------------------------------------------------
def modify_scenario_with_agent(existing_json: str, edits: str):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=OPENAI_API_KEY
    )

    instructions = f"""
    Modify the following JSON scenario ONLY according to the requested edits.
    Preserve structure and schema.

    EXISTING SCENARIO:
    {existing_json}

    REQUESTED EDITS:
    {edits}
    """

    response = llm.invoke(instructions)

    return response.content
