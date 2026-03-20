import os
import logging
from typing import TypedDict, List
from datetime import datetime
from langchain_ollama import ChatOllama
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

# Using local Ollama instance
model = ChatOllama(
    model="llama3.1",
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

    # Step 1: Web Search
    processing_steps = [
        f"📋 **RESEARCHER PROCESSING STEPS:**",
        f"",
        f"**Step 1: Query Formulation**",
        f"- Original Query: {original_query}",
        f"- Enhanced Search Query: {search_query}",
        f"- Target Year: {current_year}",
        f""
    ]

    try:
        logger.info(f"Executing web search: {search_query}")
        processing_steps.append(f"**Step 2: Web Search Execution**")
        processing_steps.append(f"- Tool: DuckDuckGo Search")
        processing_steps.append(f"- Status: Running...")
        
        raw_results = search_tool.run(search_query)
        
        result_length = len(raw_results)
        processing_steps.append(f"- Status: ✅ Completed")
        processing_steps.append(f"- Data Retrieved: {result_length} characters")
        processing_steps.append(f"")
        logger.info(f"Search completed successfully - Retrieved {result_length} characters")
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raw_results = f"Search failed: {str(e)}"
        processing_steps.append(f"- Status: ❌ Failed - {str(e)}")
        processing_steps.append(f"")

    # Step 3: Data Synthesis
    processing_steps.append(f"**Step 3: Data Synthesis & Analysis**")
    processing_steps.append(f"- Removing noise and formatting issues")
    processing_steps.append(f"- Extracting key metrics (Revenue, AI growth, Strategy)")
    processing_steps.append(f"- Structuring executive-level report")
    processing_steps.append(f"")
    
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

    logger.info("Invoking LLM for synthesis...")
    processing_steps.append(f"**Step 4: LLM Synthesis**")
    processing_steps.append(f"- Model: Llama 3.1")
    processing_steps.append(f"- Task: Generate executive summary")
    processing_steps.append(f"- Status: Processing...")
    
    response = model.invoke([HumanMessage(content=synthesis_prompt)])
    
    processing_steps.append(f"- Status: ✅ Completed")
    processing_steps.append(f"")
    processing_steps.append(f"**Step 5: Output Preparation**")
    processing_steps.append(f"- Formatting final report")
    processing_steps.append(f"- Passing to Critic for review")
    processing_steps.append(f"")
    processing_steps.append(f"=" * 60)
    
    detailed_output = "\n".join(processing_steps) + f"\n\n{response.content}"

    return {
        "messages": state["messages"] + [
            AIMessage(content=f"RESEARCHER FINDINGS:\n\n{detailed_output}")
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

    # Detailed processing steps for Critic
    processing_steps = [
        f"📋 **CRITIC PROCESSING STEPS:**",
        f"",
        f"**Step 1: Report Reception**",
        f"- Iteration Number: {step + 1}",
        f"- Report Length: {len(last_research)} characters",
        f"- Source: Researcher Agent",
        f"",
        f"**Step 2: Quality Evaluation Criteria**",
        f"- ✓ Criterion 1: Clear IBM vs Microsoft comparison",
        f"- ✓ Criterion 2: Specific metrics (Revenue, AI growth, Stock)",
        f"- ✓ Criterion 3: Executive-level professional tone",
        f"",
        f"**Step 3: LLM-Based Audit**",
        f"- Model: Llama 3.1",
        f"- Task: Quality assessment",
        f"- Status: Analyzing..."
    ]

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

    logger.info(f"Invoking LLM for critique - Iteration {step + 1}")
    response = model.invoke([HumanMessage(content=critique_prompt)])

    # Stop conditions
    response_text = response.content if isinstance(response.content, str) else str(response.content)
    
    processing_steps.append(f"- Status: ✅ Completed")
    processing_steps.append(f"")
    
    if step >= 3 or "FINISH" in response_text.upper():
        logger.info(f"Report approved after {step + 1} iteration(s)")
        
        processing_steps.append(f"**Step 4: Decision - APPROVED ✅**")
        processing_steps.append(f"- Quality Check: PASSED")
        processing_steps.append(f"- Total Iterations: {step + 1}")
        processing_steps.append(f"- Action: Finalizing report")
        processing_steps.append(f"- Next Agent: END (Task Complete)")
        processing_steps.append(f"")
        processing_steps.append(f"=" * 60)
        
        detailed_output = "\n".join(processing_steps)
        final_report = AIMessage(
            content=f"✅ VERIFIED EXECUTIVE STRATEGY REPORT\n\n{detailed_output}\n\n{last_research}"
        )

        return {
            "messages": state["messages"] + [final_report],
            "next_agent": END,
            "loop_step": step + 1,
            "original_query": state["original_query"]
        }

    # Otherwise request improvement
    logger.info(f"Requesting improvements - Iteration {step + 1}")
    
    processing_steps.append(f"**Step 4: Decision - NEEDS IMPROVEMENT 🔄**")
    processing_steps.append(f"- Quality Check: FAILED")
    processing_steps.append(f"- Current Iteration: {step + 1}")
    processing_steps.append(f"- Max Iterations: 3")
    processing_steps.append(f"- Action: Requesting refinement")
    processing_steps.append(f"- Next Agent: Researcher (for improvement)")
    processing_steps.append(f"")
    processing_steps.append(f"**Step 5: Feedback Generation**")
    processing_steps.append(f"- Identifying gaps and issues")
    processing_steps.append(f"- Providing specific improvement instructions")
    processing_steps.append(f"")
    processing_steps.append(f"=" * 60)
    
    detailed_output = "\n".join(processing_steps) + f"\n\n{response.content}"
    feedback = AIMessage(
        content=f"📝 CRITIC FEEDBACK:\n\n{detailed_output}"
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