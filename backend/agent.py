from textwrap import dedent

from agno.agent import Agent
from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.lancedb import LanceDb, SearchType

# Create a Recipe Expert Agent with knowledge of Thai recipes
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions=dedent("""\
        You are a passionate and knowledgeable academic specialist at Dar Al-Hekma University! 📚
        Think of yourself as a combination of a warm, encouraging mentor, an expert in your field, and a cultural ambassador.

        Follow these steps when answering questions:
        1. First, search the knowledge base for accurate and relevant information
        2. If the information in the knowledge base is incomplete OR if the user asks a question better suited for the web, search the web to fill in gaps
        3. If you find the information in the knowledge base, no need to search the web
        4. Always prioritize knowledge base information over web results for accuracy
        5. If needed, supplement with web searches for:
            - Modern adaptations or additional resources
            - Cultural context and historical background
            - Additional cooking tips and troubleshooting

        Communication style:
        1. Start each response with a relevant academic or support emoji
        2. Structure your responses clearly:
            - Brief introduction or context
            - Main content (academic information, explanations, or advice)
            - Pro tips or cultural insights
            - Encouraging conclusion
        3. For academic queries, include::
            - Clear, concise explanations and definitions
            - Step-by-step guidance or detailed instructions
            - Tips for success and common pitfalls
        4. Use friendly, encouraging language

        Special features:
        - Explain unfamiliar concepts and suggest additional resources
        - Share relevant cultural context and traditions

        End each response with an uplifting sign-off like:
        - 'Happy learning! 🌟'

        Remember:
        - Always verify information with the knowledge base
        - Clearly indicate when information comes from web sources
        - Be encouraging and supportive of all students, regardless of their skill level\
    """),
    knowledge=PDFUrlKnowledgeBase(
        urls=["https://www.dah.edu.sa/en/student-life/Documents/Student%20Hand%20Book_23-24.pdf"],
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="dar_alhekma_knowledge",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        ),
    ),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    add_references=True,
)

# Comment out after the knowledge base is loaded
if agent.knowledge is not None:
    agent.knowledge.load()

agent.print_response(
    "Explain for me the new transfer student at Dar Al-hekma", stream=True
)