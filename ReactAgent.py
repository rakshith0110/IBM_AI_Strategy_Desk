import os
import sqlite3
from typing import cast
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
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

model = ChatOllama(
    model="llama3.1",
    temperature=0
).bind_tools(tools)


# ==============================
# 5️⃣ AGENT NODE
# ==============================

def call_model(state: MessagesState):
    
    print("\n📋 **REACT AGENT - PROCESSING STEPS:**")
    print("\n**Step 1: Message History Management**")
    print(f"- Total Messages in State: {len(state['messages'])}")
    
    system_prompt = (
        "You are the IBM AI Strategy Desk assistant for Rakshith. "
        "If you need current information, use ONLY the 'duckduckgo_search' tool. "
        "Do NOT invent new tool names. "
        "If you know the answer without search, answer directly."
    )

    # Keep conversation small to avoid tool corruption
    trimmed_history = state["messages"][-6:]
    
    print(f"- Trimmed to Last: {len(trimmed_history)} messages")
    print(f"- Context Window: Optimized for tool stability")

    messages = [{"role": "system", "content": system_prompt}] + trimmed_history
    
    print("\n**Step 2: LLM Invocation**")
    print(f"- Model: Llama 3.1 (with tool binding)")
    print(f"- Available Tools: duckduckgo_search")
    print(f"- Task: Reasoning + Tool Selection")
    print(f"- Status: Processing...")

    try:
        response = model.invoke(messages)
        
        print(f"- Status: ✅ Completed")
        
        # Check if tool was called
        if hasattr(response, "tool_calls") and response.tool_calls:
            print(f"\n**Step 3: Tool Call Detected**")
            print(f"- Tool: {response.tool_calls[0].get('name', 'Unknown')}")
            print(f"- Arguments: {response.tool_calls[0].get('args', {})}")
            print(f"- Next Node: tools (for execution)")
        else:
            print(f"\n**Step 3: Direct Response**")
            print(f"- No tool call needed")
            print(f"- Response Length: {len(response.content)} characters")
            print(f"- Next Node: END (Task Complete)")
        
        print("\n" + "=" * 60)

        # IMPORTANT: append response, not overwrite
        return {"messages": state["messages"] + [response]}

    except Exception as e:
        print(f"- Status: ❌ Failed")
        print(f"- Error: {str(e)}")
        print(f"\n**Step 3: Fallback Response**")
        print(f"- Generating error message")
        print("\n" + "=" * 60)
        
        fallback = AIMessage(
            content="⚠️ Temporary technical issue. Please try again."
        )
        return {"messages": state["messages"] + [fallback]}


# ==============================
# 6️⃣ ROUTER
# ==============================

def should_continue(state: MessagesState):
    """Router function to determine next step."""
    
    print("\n📋 **ROUTER - PROCESSING STEPS:**")
    print("\n**Step 1: Message Analysis**")
    
    last_message = state["messages"][-1]
    print(f"- Last Message Type: {type(last_message).__name__}")

    # If model made a tool call → go to tool node
    if isinstance(last_message, AIMessage) and hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print(f"- Tool Calls Detected: {len(last_message.tool_calls)}")
        print(f"\n**Step 2: Routing Decision**")
        print(f"- Decision: ROUTE TO TOOLS 🔧")
        print(f"- Next Node: tools")
        print(f"- Action: Execute tool and return to agent")
        print("\n" + "=" * 60)
        return "tools"

    print(f"- Tool Calls: None")
    print(f"\n**Step 2: Routing Decision**")
    print(f"- Decision: TASK COMPLETE ✅")
    print(f"- Next Node: END")
    print(f"- Action: Return final response to user")
    print("\n" + "=" * 60)
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