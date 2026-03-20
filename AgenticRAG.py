import os
from typing import List, TypedDict
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
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

model = ChatOllama(
    model="llama3.1",
    temperature=0
)

# ==============================
# 4️⃣ NODES
# ==============================

def retrieve(state: GraphState):
    """Simulated Vector Store Retrieval."""
    
    print("\n📋 **RETRIEVE NODE - PROCESSING STEPS:**")
    print("\n**Step 1: Vector Store Query**")
    print(f"- Query: {state['question']}")
    print(f"- Method: Similarity Search")
    print(f"- Status: Executing...")
    
    # In production: vectorstore.similarity_search(state["question"])
    docs = ["IBM stock historical data suggests long-term enterprise stability."]
    
    print(f"- Status: ✅ Completed")
    print(f"- Documents Retrieved: {len(docs)}")
    print(f"- Document Length: {len(docs[0])} characters")
    print("\n" + "=" * 60)
    
    return {
        "documents": docs,
        "question": state["question"]
    }


def grade_retrieval(state: GraphState):
    """LLM decides if retrieval is sufficient."""
    
    doc_content = state["documents"][0]
    
    print("\n📋 **GRADE NODE - PROCESSING STEPS:**")
    print("\n**Step 1: Document Quality Assessment**")
    print(f"- Question: {state['question']}")
    print(f"- Document Length: {len(doc_content)} characters")
    print(f"- Assessment Method: LLM-based evaluation")
    
    prompt = f"""
Question: {state['question']}

Document:
{doc_content}

Is this document sufficient to fully answer the question?
Reply ONLY with YES or NO.
"""
    
    print("\n**Step 2: LLM Evaluation**")
    print(f"- Model: Llama 3.1")
    print(f"- Task: Sufficiency check")
    print(f"- Status: Processing...")
    
    response = model.invoke([HumanMessage(content=prompt)])
    
    # Ensure response.content is a string before calling .upper()
    content_str = str(response.content) if response.content else ""
    decision = "NO" in content_str.upper()
    
    print(f"- Status: ✅ Completed")
    print(f"- LLM Response: {content_str.strip()}")
    
    print("\n**Step 3: Routing Decision**")
    if decision:
        print(f"- Decision: INSUFFICIENT ❌")
        print(f"- Action: Trigger Web Search")
        print(f"- Next Node: web_search")
    else:
        print(f"- Decision: SUFFICIENT ✅")
        print(f"- Action: Proceed to generation")
        print(f"- Next Node: generate")
    print("\n" + "=" * 60)

    return {
        "needs_web_search": decision,
        "documents": state["documents"],
        "question": state["question"]
    }


def web_search(state: GraphState):
    """Fallback Agentic Web Search."""
    
    print("\n📋 **WEB SEARCH NODE - PROCESSING STEPS:**")
    print("\n**Step 1: Search Initialization**")
    print(f"- Query: {state['question']}")
    print(f"- Tool: DuckDuckGo Search")
    print(f"- Reason: Vector store retrieval insufficient")
    
    search = DuckDuckGoSearchRun()
    
    print("\n**Step 2: Web Search Execution**")
    print(f"- Status: Running...")
    
    try:
        result = search.run(state["question"])
        print(f"- Status: ✅ Completed")
        print(f"- Data Retrieved: {len(result)} characters")
    except Exception as e:
        result = f"Search failed: {str(e)}"
        print(f"- Status: ❌ Failed")
        print(f"- Error: {str(e)}")
    
    print("\n**Step 3: Document Update**")
    print(f"- Replacing vector store results with web search data")
    print(f"- Next Node: generate")
    print("\n" + "=" * 60)
    
    return {
        "documents": [result],
        "question": state["question"]
    }


def generate(state: GraphState):
    """Final synthesis step."""
    
    print("\n📋 **GENERATE NODE - PROCESSING STEPS:**")
    print("\n**Step 1: Context Preparation**")
    print(f"- Question: {state['question']}")
    print(f"- Context Documents: {len(state['documents'])}")
    print(f"- Total Context Length: {sum(len(doc) for doc in state['documents'])} characters")
    
    synthesis_prompt = f"""
You are an IBM Strategy Consultant.

Question:
{state['question']}

Context:
{state['documents']}

Provide a professional executive-level answer.
"""
    
    print("\n**Step 2: LLM Synthesis**")
    print(f"- Model: Llama 3.1")
    print(f"- Task: Generate executive answer")
    print(f"- Status: Processing...")
    
    response = model.invoke([HumanMessage(content=synthesis_prompt)])
    
    print(f"- Status: ✅ Completed")
    print(f"- Response Length: {len(response.content)} characters")
    
    print("\n**Step 3: Final Output**")
    print(f"- Formatting response")
    print(f"- Task Complete")
    print("\n" + "=" * 60)
    
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