import streamlit as st
import time
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from MultiAgentSystem import app as multi_agent_app, AgentState
from ReactAgent import app as single_agent_app
from AgenticRAG import agentic_rag_app, GraphState

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="IBM AI Strategy Desk",
    layout="wide",
    page_icon="🤖"
)

# ======================================
# SIDEBAR
# ======================================

with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg",
        width=100
    )

    st.title("Strategy Control Panel")

    agent_mode = st.radio(
        "Select Workflow Mode:",
        [
            "🚀 Standard (Single Agent)",
            "👥 Quality (Multi-Agent Team)",
            "🤖 Autonomous (Agentic RAG)"
        ],
        help="Standard = Fast | Quality = Research + Critic | Autonomous = RAG + Web fallback"
    )

    st.divider()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.info("User: Praveen\nRole: Delivery Consultant Intern")

# ======================================
# SESSION INIT
# ======================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================================
# TABS
# ======================================

tab1, tab2 = st.tabs(["💬 Strategy Chat", "📊 System Architecture"])

# ======================================
# CHAT DISPLAY
# ======================================

with tab1:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ======================================
# CHAT INPUT
# ======================================

if prompt := st.chat_input("Ask about IBM Strategy, AI trends, or RAG insights..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with tab1:

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            start_time = time.time()

            with st.status("🛠️ Initiating Workflow...", expanded=True) as status:

                final_answer = ""
                trace_logs = []

                try:

                    # ======================================
                    # 👥 MULTI-AGENT MODE
                    # ======================================
                    if "Quality" in agent_mode:

                        status.update(label="👥 Researcher + Critic Running...", state="running")

                        initial_state: AgentState = {
                            "messages": [HumanMessage(content=prompt)],
                            "next_agent": "researcher",
                            "loop_step": 0,
                            "original_query": prompt
                        }

                        step_count = 0

                        for event in multi_agent_app.stream(initial_state, stream_mode="values"):
                            if "messages" in event:
                                last_msg = event["messages"][-1]
                                step_count += 1

                                if "RESEARCHER FINDINGS" in last_msg.content:
                                    trace_logs.append(f"🔎 Step {step_count}: Researcher gathered data")

                                elif "CRITIC FEEDBACK" in last_msg.content:
                                    trace_logs.append(f"⚖️ Step {step_count}: Critic requested improvement")

                                elif "VERIFIED" in last_msg.content:
                                    trace_logs.append(f"✅ Step {step_count}: Critic approved final report")

                                final_answer = last_msg.content

                        status.update(label="✅ Multi-Agent Workflow Complete", state="complete")

                    # ======================================
                    # 🤖 AGENTIC RAG MODE
                    # ======================================
                    elif "Autonomous" in agent_mode:

                        status.update(label="🤖 Agentic RAG Running...", state="running")

                        trace_logs.append("📂 Retrieving from Vector Store")

                        rag_state: GraphState = {
                            "question": prompt,
                            "documents": [],
                            "needs_web_search": False,
                            "generation": ""
                        }
                        
                        result = agentic_rag_app.invoke(rag_state)

                        if result.get("needs_web_search"):
                            trace_logs.append("🌐 Retrieval insufficient → Triggered Web Search")

                        trace_logs.append("🧠 Generating final synthesis")

                        final_answer = result.get("generation", "No response generated.")

                        status.update(label="✅ Agentic RAG Completed", state="complete")

                    # ======================================
                    # 🚀 STANDARD MODE
                    # ======================================
                    else:

                        status.update(label="🚀 Standard Agent Running...", state="running")

                        trace_logs.append("🧠 Single-pass reasoning")
                        trace_logs.append("🔧 Tool call (if required)")

                        react_state: MessagesState = {"messages": [HumanMessage(content=prompt)]}
                        
                        result = single_agent_app.invoke(
                            react_state,
                            {"configurable": {"thread_id": "praveen_session"}}
                        )

                        final_answer = result["messages"][-1].content

                        status.update(label="✅ Standard Response Ready", state="complete")

                    # ======================================
                    # DISPLAY FINAL ANSWER
                    # ======================================

                    st.markdown(final_answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": final_answer
                    })

                    # ======================================
                    # EXECUTION TRACE PANEL
                    # ======================================

                    elapsed = round(time.time() - start_time, 2)

                    st.divider()
                    st.subheader("🔍 Execution Trace")

                    for log in trace_logs:
                        st.write(log)

                    st.write(f"⏱ Execution Time: {elapsed} seconds")
                    st.write(f"⚙ Mode: {agent_mode}")

                except Exception as e:
                    status.update(label="⚠️ System Error", state="error")
                    st.error(f"Error: {e}")

# ======================================
# ARCHITECTURE TAB
# ======================================

with tab2:
    st.subheader("Workflow Visualization")

    try:
        if "Quality" in agent_mode:
            graph = multi_agent_app.get_graph()
        elif "Autonomous" in agent_mode:
            graph = agentic_rag_app.get_graph()
        else:
            graph = single_agent_app.get_graph()

        st.image(graph.draw_mermaid_png())

    except Exception:
        st.info("Graph visualization requires Mermaid or Pyppeteer installed.")