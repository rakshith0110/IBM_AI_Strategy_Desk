import os
from typing import List, TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph, START

# ==============================
# 1️⃣ LOAD ENV
# ==============================

load_dotenv()

# ==============================
# 2️⃣ STATE
# ==============================

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]
    needs_web_search: bool

# ==============================
# 3️⃣ MODEL
# ==============================

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# ==============================
# 4️⃣ NODES
# ==============================

def retrieve(state: GraphState):
    """Simulated Vector Store Retrieval."""
    
    # In production: vectorstore.similarity_search(state["question"])
    docs = ["IBM stock historical data suggests long-term enterprise stability."]
    
    return {
        "documents": docs,
        "question": state["question"]
    }


def grade_retrieval(state: GraphState):
    """LLM decides if retrieval is sufficient."""
    
    doc_content = state["documents"][0]
    
    prompt = f"""
Question: {state['question']}

Document:
{doc_content}

Is this document sufficient to fully answer the question?
Reply ONLY with YES or NO.
"""
    
    response = model.invoke([HumanMessage(content=prompt)])
    
    # Ensure response.content is a string before calling .upper()
    content_str = str(response.content) if response.content else ""
    decision = "NO" in content_str.upper()

    return {
        "needs_web_search": decision,
        "documents": state["documents"],
        "question": state["question"]
    }


def web_search(state: GraphState):
    """Fallback Agentic Web Search."""
    
    search = DuckDuckGoSearchRun()
    
    try:
        result = search.run(state["question"])
    except Exception as e:
        result = f"Search failed: {str(e)}"
    
    return {
        "documents": [result],
        "question": state["question"]
    }


def generate(state: GraphState):
    """Final synthesis step."""
    
    synthesis_prompt = f"""
You are an IBM Strategy Consultant.

Question:
{state['question']}

Context:
{state['documents']}

Provide a professional executive-level answer.
"""
    
    response = model.invoke([HumanMessage(content=synthesis_prompt)])
    
    return {
        "generation": response.content,
        "documents": state["documents"],
        "question": state["question"]
    }

# ==============================
# 5️⃣ BUILD GRAPH
# ==============================

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade", grade_retrieval)
workflow.add_node("web_search", web_search)
workflow.add_node("generate", generate)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade")

workflow.add_conditional_edges(
    "grade",
    lambda state: "web_search" if state["needs_web_search"] else "generate",
    {
        "web_search": "web_search",
        "generate": "generate"
    }
)

workflow.add_edge("web_search", "generate")
workflow.add_edge("generate", END)

agentic_rag_app = workflow.compile()