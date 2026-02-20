import os
import logging
from typing import TypedDict, List
from datetime import datetime
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==============================
# 1️⃣ DEFINE STATE
# ==============================

class AgentState(TypedDict):
    messages: List[BaseMessage]
    next_agent: str
    loop_step: int
    original_query: str


# ==============================
# 2️⃣ MODEL SETUP
# ==============================

# Get API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in .env file")

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

search_tool = DuckDuckGoSearchRun()


# ==============================
# 3️⃣ RESEARCHER NODE
# ==============================

def researcher_node(state: AgentState) -> AgentState:
    logger.info("🔎 Researcher conducting structured analysis...")

    original_query = state["original_query"]
    current_year = datetime.now().year
    search_query = f"latest {original_query} strategy and financial performance {current_year}"

    try:
        raw_results = search_tool.run(search_query)
        logger.info(f"Search completed for query: {search_query}")
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raw_results = f"Search failed: {str(e)}"

    # 🧠 Synthesize search results professionally
    synthesis_prompt = f"""
You are an IBM Strategy Research Analyst.

Using the raw search data below, create a clean executive summary.
Remove:
- 'See full list on'
- Broken formatting
- Repeated text
- Random stock analysis noise

Focus only on:
- Strategy comparison
- Revenue
- AI growth
- Financial performance

Raw Data:
{raw_results}

Produce a structured executive-level report.
"""

    response = model.invoke([HumanMessage(content=synthesis_prompt)])

    return {
        "messages": state["messages"] + [
            AIMessage(content=f"RESEARCHER FINDINGS:\n\n{response.content}")
        ],
        "next_agent": "critic",
        "loop_step": state["loop_step"],
        "original_query": original_query
    }

# ==============================
# 4️⃣ CRITIC NODE
# ==============================

def critic_node(state: AgentState) -> AgentState:
    logger.info("⚖️ Critic auditing report...")

    step = state["loop_step"]
    last_research = state["messages"][-1].content

    critique_prompt = f"""
You are a Senior Strategy Consultant auditing a competitive AI report.

Report:
{last_research}

Evaluation Criteria:
1. Does it clearly compare IBM and Microsoft?
2. Does it include at least one specific metric (Revenue, AI growth, Stock)?
3. Is the tone executive-level professional?

If all criteria are satisfied, respond ONLY with: FINISH
Otherwise, provide specific improvement instructions.
"""

    response = model.invoke([HumanMessage(content=critique_prompt)])

    # Stop conditions
    response_text = response.content if isinstance(response.content, str) else str(response.content)
    if step >= 3 or "FINISH" in response_text.upper():
        logger.info(f"Report approved after {step + 1} iteration(s)")
        final_report = AIMessage(
            content=f"✅ VERIFIED EXECUTIVE STRATEGY REPORT\n\n{last_research}"
        )

        return {
            "messages": state["messages"] + [final_report],
            "next_agent": END,
            "loop_step": step + 1,
            "original_query": state["original_query"]
        }

    # Otherwise request improvement
    logger.info(f"Requesting improvements - Iteration {step + 1}")
    feedback = AIMessage(
        content=f"📝 CRITIC FEEDBACK:\n\n{response.content}"
    )

    return {
        "messages": state["messages"] + [feedback],
        "next_agent": "researcher",
        "loop_step": step + 1,
        "original_query": state["original_query"]
    }


# ==============================
# 5️⃣ BUILD WORKFLOW
# ==============================

workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("critic", critic_node)

workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "critic")

workflow.add_conditional_edges(
    "critic",
    lambda state: state["next_agent"],
    {
        "researcher": "researcher",
        END: END
    }
)

app = workflow.compile()


# ==============================
# 6️⃣ RUN EXAMPLE
# ==============================

if __name__ == "__main__":
    user_question = "IBM vs Microsoft 2026 AI strategy"

    initial_state: AgentState = {
        "messages": [HumanMessage(content=user_question)],
        "next_agent": "researcher",
        "loop_step": 0,
        "original_query": user_question
    }

    result = app.invoke(initial_state)

    logger.info("\n\n===== FINAL OUTPUT =====\n")
    print(result["messages"][-1].content)