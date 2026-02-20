import os
import sqlite3
from typing import cast
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver

# ==============================
# 1️⃣ LOAD ENV
# ==============================

load_dotenv()

# ==============================
# 2️⃣ TOOLS
# ==============================

search_tool = DuckDuckGoSearchRun()
tools = [search_tool]

tool_node = ToolNode(tools)

# ==============================
# 3️⃣ MEMORY (SQLite Persistence)
# ==============================

conn = sqlite3.connect("agent_memory.db", check_same_thread=False)
memory = SqliteSaver(conn)

# ==============================
# 4️⃣ MODEL (Bound with Tools)
# ==============================

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
).bind_tools(tools)


# ==============================
# 5️⃣ AGENT NODE
# ==============================

def call_model(state: MessagesState):

    system_prompt = (
        "You are the IBM AI Strategy Desk assistant for Praveen. "
        "If you need current information, use ONLY the 'duckduckgo_search' tool. "
        "Do NOT invent new tool names. "
        "If you know the answer without search, answer directly."
    )

    # Keep conversation small to avoid tool corruption
    trimmed_history = state["messages"][-6:]

    messages = [{"role": "system", "content": system_prompt}] + trimmed_history

    try:
        response = model.invoke(messages)

        # IMPORTANT: append response, not overwrite
        return {"messages": state["messages"] + [response]}

    except Exception as e:
        fallback = AIMessage(
            content="⚠️ Temporary technical issue. Please try again."
        )
        return {"messages": state["messages"] + [fallback]}


# ==============================
# 6️⃣ ROUTER
# ==============================

def should_continue(state: MessagesState):
    last_message = state["messages"][-1]

    # If model made a tool call → go to tool node
    if isinstance(last_message, AIMessage) and hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END


# ==============================
# 7️⃣ GRAPH BUILD
# ==============================

workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app = workflow.compile(checkpointer=memory)


# ==============================
# 8️⃣ EXECUTION
# ==============================

if __name__ == "__main__":
    print("🚀 Launching Production Agent (Llama 3.1 Stable)...")

    config: RunnableConfig = {
        "configurable": {
            "thread_id": "manager_demo_1"  # Enables memory
        }
    }

    query = "IBM vs Microsoft 2026 AI strategy"
    input_data: MessagesState = {
        "messages": [HumanMessage(content=query)]
    }

    try:
        for chunk in app.stream(input_data, config, stream_mode="values"):
            chunk["messages"][-1].pretty_print()

    except Exception as e:
        print(f"⚠️ System Note: {e}")