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
# CUSTOM CSS - MINIMALISTIC WHITE-BLUE THEME
# ======================================

st.markdown("""
<style>
    /* ========================================
       ENHANCED PROFESSIONAL UI - MODERN DESIGN
       Colors: Light Blue (#3B82F6), White (#FFFFFF), Black (#000000)
       ======================================== */
    
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Main background - Enhanced gradient with animation */
    .stApp {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 50%, #E0F2FE 100%);
        color: #000000;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        animation: backgroundShift 15s ease infinite;
    }
    
    @keyframes backgroundShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Sidebar - Enhanced with glassmorphism effect */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
        border-right: 2px solid rgba(59, 130, 246, 0.2);
        box-shadow: 4px 0 30px rgba(59, 130, 246, 0.15);
        backdrop-filter: blur(20px);
        color: #1E293B;
    }
    
    [data-testid="stSidebar"] * {
        color: #1E293B !important;
    }
    
    /* Mode selection cards - Enhanced with smooth animations */
    [data-testid="stSidebar"] .stRadio {
        background: transparent;
        padding: 0.5rem 0;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin: 0.75rem 0;
        display: block;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        cursor: pointer;
        font-weight: 600;
        color: #334155 !important;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stSidebar"] .stRadio > label::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-color: #3B82F6;
        transform: translateX(6px) scale(1.02);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.25);
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover::before {
        left: 100%;
    }
    
    [data-testid="stSidebar"] .stRadio > label[data-baseweb="radio"] > div:first-child {
        background-color: #3B82F6 !important;
        border-color: #3B82F6 !important;
    }
    
    /* Selected mode highlight - Enhanced glow effect */
    [data-testid="stSidebar"] .stRadio input:checked + div {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        border-color: #1E40AF !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 24px rgba(59, 130, 246, 0.5),
                    0 0 40px rgba(59, 130, 246, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
        animation: pulseGlow 2s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 6px 24px rgba(59, 130, 246, 0.5), 0 0 40px rgba(59, 130, 246, 0.3); }
        50% { box-shadow: 0 8px 32px rgba(59, 130, 246, 0.6), 0 0 60px rgba(59, 130, 246, 0.4); }
    }
    
    [data-testid="stSidebar"] .stRadio input:checked + div * {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg,
            transparent 0%,
            #CBD5E1 50%,
            transparent 100%);
        margin: 1.5rem 0;
    }
    
    /* Sidebar title styling */
    [data-testid="stSidebar"] h1 {
        color: #1E293B !important;
        font-weight: 800;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #3B82F6;
        background: linear-gradient(135deg, #1E293B 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Mode selection label */
    [data-testid="stSidebar"] .stRadio > label:first-child {
        color: #475569 !important;
        font-weight: 600;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }
    
    /* Chat input - Enhanced with focus animation */
    .stChatInput {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%) !important;
        border-radius: 20px;
        border: 2px solid #3B82F6;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        padding: 6px;
        transition: all 0.3s ease;
    }
    
    .stChatInput:focus-within {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.6),
                    0 0 60px rgba(59, 130, 246, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: #60A5FA;
    }
    
    .stChatInput input {
        background-color: transparent !important;
        color: #FFFFFF !important;
        border: none;
        font-size: 1rem;
    }
    
    .stChatInput input::placeholder {
        color: #94A3B8 !important;
    }
    
    /* Chat messages - Enhanced with slide-in animation */
    .stChatMessage {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%);
        border-radius: 20px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.8);
        color: #000000;
        backdrop-filter: blur(15px);
        animation: slideInMessage 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    @keyframes slideInMessage {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(59, 130, 246, 0.2);
    }
    
    /* User message - Light blue glossy */
    [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%);
        border-radius: 12px;
        padding: 1rem;
        color: #000000;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.6);
    }
    
    /* Headers - Glossy text effect */
    h1, h2, h3, h4, h5, h6 {
        color: #000000;
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(59, 130, 246, 0.1);
    }
    
    h1 {
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Status box - Glossy blue */
    .stStatus {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        border-left: 4px solid #3B82F6;
        border-radius: 12px;
        color: #000000;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
    }
    
    /* Divider - Glossy gradient */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg,
            transparent 0%,
            #3B82F6 50%,
            transparent 100%);
        box-shadow: 0 1px 4px rgba(59, 130, 246, 0.3);
    }
    
    /* Execution trace - Enhanced with stagger animation */
    .trace-item {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%);
        padding: 1rem 1.5rem;
        margin: 0.75rem 0;
        border-radius: 12px;
        border-left: 5px solid #3B82F6;
        color: #000000;
        box-shadow: 0 3px 12px rgba(59, 130, 246, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.5);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out backwards;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .trace-item:nth-child(1) { animation-delay: 0.1s; }
    .trace-item:nth-child(2) { animation-delay: 0.2s; }
    .trace-item:nth-child(3) { animation-delay: 0.3s; }
    .trace-item:nth-child(4) { animation-delay: 0.4s; }
    
    .trace-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 5px;
        background: linear-gradient(180deg, #3B82F6, #60A5FA);
        transition: width 0.3s ease;
    }
    
    .trace-item:hover {
        transform: translateX(8px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
        border-left-color: #60A5FA;
    }
    
    .trace-item:hover::before {
        width: 100%;
        opacity: 0.1;
    }
    
    /* Analytics cards - Premium with 3D effect */
    .analytics-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #E0F2FE 100%);
        border: 2px solid rgba(59, 130, 246, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.8),
                    inset 0 -1px 0 rgba(59, 130, 246, 0.1);
        color: #000000;
        backdrop-filter: blur(15px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .analytics-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s ease;
    }
    
    .analytics-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 50px rgba(59, 130, 246, 0.35),
                    inset 0 1px 0 rgba(255, 255, 255, 0.9);
        border-color: #3B82F6;
    }
    
    .analytics-card:hover::before {
        opacity: 1;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
        animation: countUp 0.8s ease-out;
        letter-spacing: -1px;
    }
    
    @keyframes countUp {
        from {
            opacity: 0;
            transform: translateY(20px) scale(0.8);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .metric-label {
        color: #64748B;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button styling - Enhanced 3D with ripple effect */
    .stButton button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: #FFFFFF;
        border-radius: 14px;
        border: none;
        padding: 0.875rem 2.5rem;
        font-weight: 700;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2),
                    inset 0 -2px 0 rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
        font-size: 0.95rem;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    .stButton button:active {
        transform: translateY(0) scale(0.98);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Primary button - Extra glossy */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
    
    /* Sidebar buttons - White theme styling */
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: #FFFFFF;
        border-radius: 10px;
        padding: 0.65rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
    }
    
    /* Sidebar info box - White theme */
    [data-testid="stSidebar"] .stAlert {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%) !important;
        border: 2px solid #3B82F6 !important;
        border-radius: 12px;
        color: #1E293B !important;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    
    [data-testid="stSidebar"] .stAlert * {
        color: #1E293B !important;
    }
    }
    
    /* Info box - Glossy light blue */
    .stInfo {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        border-left: 4px solid #3B82F6;
        border-radius: 12px;
        color: #000000;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.5);
    }
    
    /* Expander - Enhanced with smooth transitions */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border-radius: 12px;
        color: #000000;
        font-weight: 700;
        box-shadow: 0 3px 10px rgba(59, 130, 246, 0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 0.5rem 0;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: #FFFFFF !important;
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.4);
        transform: translateX(4px);
    }
    
    .streamlit-expanderHeader svg {
        transition: transform 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover svg {
        transform: rotate(90deg);
    }
    
    /* Metrics - Glossy display */
    [data-testid="stMetricValue"] {
        color: #000000;
        font-weight: 700;
        font-size: 1.8rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Scrollbar - Modern minimal design */
    ::-webkit-scrollbar {
        width: 14px;
        height: 14px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(240, 249, 255, 0.5);
        border-radius: 12px;
        margin: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        border-radius: 12px;
        border: 3px solid rgba(240, 249, 255, 0.5);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        border-width: 2px;
    }
    
    ::-webkit-scrollbar-thumb:active {
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
    }
    
    /* Glass morphism effect for containers */
    .element-container {
        backdrop-filter: blur(15px);
    }
    
    /* Enhanced glossy overlay with animation */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 400px;
        background: radial-gradient(ellipse at top, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
        animation: overlayPulse 8s ease-in-out infinite;
    }
    
    @keyframes overlayPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Loading spinner enhancement */
    .stSpinner > div {
        border-color: #3B82F6 !important;
        border-top-color: transparent !important;
        animation: spin 0.8s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Status indicator enhancement */
    .stStatus {
        animation: statusFadeIn 0.5s ease-out;
    }
    
    @keyframes statusFadeIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Responsive design improvements */
    @media (max-width: 768px) {
        .analytics-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .stButton button {
            padding: 0.75rem 1.5rem;
            font-size: 0.85rem;
        }
        
        .trace-item {
            padding: 0.75rem 1rem;
        }
    }
    
    /* Focus states for accessibility */
    button:focus-visible,
    input:focus-visible {
        outline: 3px solid #3B82F6;
        outline-offset: 2px;
    }
    
    /* Smooth page transitions */
    .main .block-container {
        animation: pageLoad 0.6s ease-out;
    }
    
    @keyframes pageLoad {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# ======================================
# SIDEBAR
# ======================================

with st.sidebar:
    # IBM Logo with centered alignment and better spacing
    col_logo = st.columns([1, 2, 1])
    with col_logo[1]:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg",
            width=120
        )
    
    st.markdown("<h2 style='text-align: center; margin-top: 0.5rem; margin-bottom: 1.5rem;'>Strategy Control Panel</h2>", unsafe_allow_html=True)
    
    st.divider()
    
    # Modes Section with enhanced organization
    st.markdown("### 🎯 Workflow Modes")
    st.markdown("<p style='font-size: 0.85rem; color: #64748B; margin-bottom: 1rem;'>Choose your AI strategy workflow</p>", unsafe_allow_html=True)
    
    agent_mode = st.radio(
        "Select Mode:",
        [
            "🚀 Standard (Single Agent)",
            "👥 Quality (Multi-Agent Team)",
            "🤖 Autonomous (Agentic RAG)"
        ],
        label_visibility="collapsed"
    )
    
    # Mode descriptions
    mode_info = {
        "🚀 Standard (Single Agent)": "⚡ **Fast & Efficient** - Single-pass reasoning with direct tool access for quick responses",
        "👥 Quality (Multi-Agent Team)": "🎓 **Research & Review** - Multi-agent collaboration with Researcher and Critic for comprehensive analysis",
        "🤖 Autonomous (Agentic RAG)": "🧠 **Smart Retrieval** - RAG-powered with vector store and intelligent web search fallback"
    }
    
    st.markdown(f"<div style='background: #F0F9FF; padding: 0.75rem; border-radius: 8px; border-left: 3px solid #3B82F6; margin-top: 0.5rem;'><small>{mode_info[agent_mode]}</small></div>", unsafe_allow_html=True)

    st.divider()
    
    # Action buttons section
    st.markdown("### ⚙️ Actions")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    
    # User info with better styling
    st.markdown("### 👤 User Profile")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
                padding: 1rem;
                border-radius: 10px;
                border: 1px solid #3B82F6;'>
        <p style='margin: 0; font-weight: 600; color: #1E40AF;'>Rakshith PR</p>
        <p style='margin: 0.25rem 0 0 0; font-size: 0.85rem; color: #3B82F6;'>Delivery Consultant Intern</p>
    </div>
    """, unsafe_allow_html=True)

# ======================================
# SESSION INIT
# ======================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_section" not in st.session_state:
    st.session_state.active_section = "chat"

if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0

if "response_times" not in st.session_state:
    st.session_state.response_times = []

# ======================================
# TOGGLE NAVIGATION
# ======================================

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💬 Chat", key="btn_chat", use_container_width=True,
                 type="primary" if st.session_state.active_section == "chat" else "secondary"):
        st.session_state.active_section = "chat"
        st.rerun()

with col2:
    if st.button("📊 Architecture", key="btn_arch", use_container_width=True,
                 type="primary" if st.session_state.active_section == "architecture" else "secondary"):
        st.session_state.active_section = "architecture"
        st.rerun()

with col3:
    if st.button("📈 Analytics", key="btn_analytics", use_container_width=True,
                 type="primary" if st.session_state.active_section == "analytics" else "secondary"):
        st.session_state.active_section = "analytics"
        st.rerun()

st.divider()

# ======================================
# CHAT SECTION
# ======================================

if st.session_state.active_section == "chat":
    st.header("💬 Strategy Chat")
    
    # Display default information if no messages yet
    if len(st.session_state.messages) == 0:
        # Welcome section
        st.info("👋 **Welcome to IBM AI Strategy Desk** - Your intelligent assistant for IBM strategy insights, AI trends, and technical guidance.")
        
        # Current mode
        st.subheader(f"🎯 Current Mode: {agent_mode}")
        mode_description = (
            "Fast single-pass reasoning with tool calls" if "Standard" in agent_mode else
            "Multi-agent collaboration with Researcher and Critic for quality assurance" if "Quality" in agent_mode else
            "Autonomous RAG with vector store retrieval and intelligent web search fallback"
        )
        st.write(mode_description)
        
        st.divider()
        
        # What you can ask
        st.subheader("💡 What You Can Ask:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            - **IBM Strategy:** Business insights, market positioning, competitive analysis
            - **AI & Technology:** Latest trends, implementation strategies, best practices
            """)
        
        with col2:
            st.markdown("""
            - **RAG Systems:** Retrieval-Augmented Generation concepts and applications
            - **Technical Guidance:** Architecture decisions, system design, optimization
            """)
        
        st.divider()
        
        # Quick start examples
        st.subheader("🚀 Quick Start Examples:")
        with st.container():
            st.markdown("""
            - "What are IBM's key AI initiatives for 2026?"
            - "Explain how RAG systems improve LLM accuracy"
            - "Compare multi-agent vs single-agent architectures"
            - "What are best practices for enterprise AI deployment?"
            """)
        
        st.divider()
        
        # Mode capabilities
        st.subheader("⚙️ Mode Capabilities:")
        
        tab1, tab2, tab3 = st.tabs(["🚀 Standard", "👥 Quality", "🤖 Autonomous"])
        
        with tab1:
            st.write("**Fast single-pass reasoning with tool access**")
            st.write("✓ Quick responses")
            st.write("✓ Direct tool integration")
            st.write("✓ Efficient for straightforward queries")
        
        with tab2:
            st.write("**Multi-agent collaboration (Researcher + Critic)**")
            st.write("✓ Thorough research phase")
            st.write("✓ Quality verification loop")
            st.write("✓ Best for complex analysis")
        
        with tab3:
            st.write("**Agentic RAG with intelligent fallback**")
            st.write("✓ Vector store retrieval")
            st.write("✓ Automatic web search when needed")
            st.write("✓ Context-aware generation")
        
        st.divider()
        
        st.success("💬 **Ready to start?** Type your question below and press Enter to begin!")
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ======================================
    # CHAT INPUT
    # ======================================

    if prompt := st.chat_input("Ask about IBM Strategy, AI trends, or RAG insights..."):
        
        st.session_state.total_queries += 1
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            start_time = time.time()

            # Create placeholder for steps display
            steps_placeholder = st.empty()
            response_placeholder = st.empty()

            final_answer = ""
            trace_logs = []

            try:

                # ======================================
                # 👥 MULTI-AGENT MODE
                # ======================================
                if "Quality" in agent_mode:

                    trace_logs.append("🚀 **Initializing Multi-Agent System**")
                    trace_logs.append("\n- Mode: Quality Assurance (Researcher + Critic)")
                    trace_logs.append("\n- Max Iterations: 3")
                    steps_placeholder.markdown("  \n".join(trace_logs))

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
                                trace_logs.append(f"\n\n🔎 **Agent {step_count}: RESEARCHER**")
                                trace_logs.append("\n- Conducting web search")
                                trace_logs.append("\n- Synthesizing data with LLM")
                                trace_logs.append("\n- Status: ✅ Completed")
                                steps_placeholder.markdown("  \n".join(trace_logs))

                            elif "CRITIC FEEDBACK" in last_msg.content:
                                trace_logs.append(f"\n\n⚖️ **Agent {step_count}: CRITIC**")
                                trace_logs.append("\n- Evaluating report quality")
                                trace_logs.append("\n- Status: ⚠️ Requesting improvements")
                                trace_logs.append("\n- Action: Routing back to Researcher")
                                steps_placeholder.markdown("  \n".join(trace_logs))

                            elif "VERIFIED" in last_msg.content:
                                trace_logs.append(f"\n\n✅ **Agent {step_count}: CRITIC**")
                                trace_logs.append("\n- Final quality check")
                                trace_logs.append("\n- Status: ✅ APPROVED")
                                trace_logs.append("\n- Action: Task Complete")
                                steps_placeholder.markdown("  \n".join(trace_logs))

                            final_answer = last_msg.content

                # ======================================
                # 🤖 AGENTIC RAG MODE
                # ======================================
                elif "Autonomous" in agent_mode:

                    trace_logs.append("🚀 **Initializing Agentic RAG System**")
                    trace_logs.append("\n- Mode: Autonomous RAG (Retrieve → Grade → Search → Generate)")
                    trace_logs.append("\n- Vector Store: Simulated")
                    steps_placeholder.markdown("  \n".join(trace_logs))

                    trace_logs.append("\n\n📂 **Node 1: RETRIEVE**")
                    trace_logs.append("\n- Querying vector store")
                    trace_logs.append("\n- Status: Running...")
                    steps_placeholder.markdown("  \n".join(trace_logs))

                    rag_state: GraphState = {
                        "question": prompt,
                        "documents": [],
                        "needs_web_search": False,
                        "generation": ""
                    }
                    
                    result = agentic_rag_app.invoke(rag_state)

                    trace_logs.append("\n- Status: ✅ Completed")
                    
                    trace_logs.append("\n\n⚖️ **Node 2: GRADE**")
                    trace_logs.append("\n- Evaluating document relevance")
                    trace_logs.append("\n- LLM-based sufficiency check")
                    steps_placeholder.markdown("  \n".join(trace_logs))

                    if result.get("needs_web_search"):
                        trace_logs.append("\n- Decision: ❌ INSUFFICIENT")
                        trace_logs.append("\n\n🌐 **Node 3: WEB SEARCH**")
                        trace_logs.append("\n- Fallback to DuckDuckGo")
                        trace_logs.append("\n- Status: ✅ Completed")
                        steps_placeholder.markdown("  \n".join(trace_logs))
                    else:
                        trace_logs.append("\n- Decision: ✅ SUFFICIENT")
                        steps_placeholder.markdown("  \n".join(trace_logs))

                    trace_logs.append("\n\n🧠 **Node 4: GENERATE**")
                    trace_logs.append("\n- Synthesizing final answer")
                    trace_logs.append("\n- Status: ✅ Completed")
                    steps_placeholder.markdown("  \n".join(trace_logs))

                    final_answer = result.get("generation", "No response generated.")

                # ======================================
                # 🚀 STANDARD MODE
                # ======================================
                else:

                    trace_logs.append("🚀 **Initializing ReAct Agent**")
                    trace_logs.append("\n- Mode: Standard (Reason + Act)")
                    trace_logs.append("\n- Memory: SQLite Persistence")
                    trace_logs.append("\n- Tools: DuckDuckGo Search")
                    steps_placeholder.markdown("  \n".join(trace_logs))

                    trace_logs.append("\n\n🧠 **Node 1: AGENT (Reasoning)**")
                    trace_logs.append("\n- Analyzing query")
                    trace_logs.append("\n- Deciding if tool is needed")
                    trace_logs.append("\n- Status: Processing...")
                    steps_placeholder.markdown("  \n".join(trace_logs))

                    react_state: MessagesState = {"messages": [HumanMessage(content=prompt)]}
                    
                    result = single_agent_app.invoke(
                        react_state,
                        {"configurable": {"thread_id": "praveen_session"}}
                    )
                    
                    trace_logs.append("\n- Status: ✅ Completed")
                    
                    # Check if tool was used
                    if len(result["messages"]) > 2:
                        trace_logs.append("\n\n🔧 **Node 2: TOOLS**")
                        trace_logs.append("\n- Tool executed: DuckDuckGo Search")
                        trace_logs.append("\n- Status: ✅ Completed")
                        trace_logs.append("\n\n🧠 **Node 3: AGENT (Synthesis)**")
                        trace_logs.append("\n- Incorporating tool results")
                        trace_logs.append("\n- Status: ✅ Completed")
                    else:
                        trace_logs.append("\n- No tool call needed")
                        trace_logs.append("\n- Direct response generated")
                    
                    steps_placeholder.markdown("  \n".join(trace_logs))

                    final_answer = result["messages"][-1].content

                # ======================================
                # DISPLAY FINAL ANSWER
                # ======================================

                # Clear steps and show final response
                steps_placeholder.empty()
                response_placeholder.markdown(final_answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_answer
                })

                # ======================================
                # EXECUTION TRACE PANEL
                # ======================================

                elapsed = round(time.time() - start_time, 2)
                st.session_state.response_times.append(elapsed)

                st.divider()
                
                with st.expander("🔍 Execution Trace", expanded=False):
                    st.markdown("### Processing Steps")
                    for log in trace_logs:
                        st.markdown(f'<div class="trace-item">{log}</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("⏱ Execution Time", f"{elapsed}s")
                    with col_b:
                        st.metric("⚙ Mode", agent_mode.split("(")[0].strip())

            except Exception as e:
                steps_placeholder.empty()
                response_placeholder.error(f"Error: {e}")

# ======================================
# ARCHITECTURE SECTION
# ======================================

elif st.session_state.active_section == "architecture":
    st.header("📊 System Architecture")
    
    st.markdown("""
    <div class="analytics-card">
        <h3>Workflow Visualization</h3>
        <p>Visual representation of the current agent workflow and decision flow.</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        if "Quality" in agent_mode:
            graph = multi_agent_app.get_graph()
            st.info("**Multi-Agent System:** Researcher → Critic → Verification Loop")
        elif "Autonomous" in agent_mode:
            graph = agentic_rag_app.get_graph()
            st.info("**Agentic RAG:** Retrieval → Grading → Web Search (if needed) → Generation")
        else:
            graph = single_agent_app.get_graph()
            st.info("**Standard Agent:** Single-pass ReAct reasoning with tool calls")

        st.image(graph.draw_mermaid_png())

    except Exception as e:
        st.warning("Graph visualization requires Mermaid or Pyppeteer installed.")
        st.code(f"Error: {e}")

# ======================================
# ANALYTICS SECTION
# ======================================

elif st.session_state.active_section == "analytics":
    st.header("📈 Analytics Dashboard")
    
    # Calculate metrics
    total_queries = st.session_state.total_queries
    avg_response_time = round(sum(st.session_state.response_times) / len(st.session_state.response_times), 2) if st.session_state.response_times else 0
    total_messages = len(st.session_state.messages)
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="analytics-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Queries</div>
        </div>
        """.format(total_queries), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="analytics-card">
            <div class="metric-value">{}s</div>
            <div class="metric-label">Avg Response Time</div>
        </div>
        """.format(avg_response_time), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="analytics-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Messages</div>
        </div>
        """.format(total_messages), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="analytics-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Active Mode</div>
        </div>
        """.format(agent_mode.split("(")[0].strip()), unsafe_allow_html=True)
    
    st.divider()
    
    # Response time chart
    if st.session_state.response_times:
        st.subheader("⏱ Response Time Trend")
        
        import pandas as pd
        
        df = pd.DataFrame({
            'Query': [f"Q{i+1}" for i in range(len(st.session_state.response_times))],
            'Response Time (s)': st.session_state.response_times
        })
        
        st.line_chart(df.set_index('Query'))
        
        st.markdown("""
        <div class="analytics-card">
            <h4>Performance Insights</h4>
            <ul>
                <li><strong>Fastest Response:</strong> {}s</li>
                <li><strong>Slowest Response:</strong> {}s</li>
                <li><strong>Median Response:</strong> {}s</li>
            </ul>
        </div>
        """.format(
            round(min(st.session_state.response_times), 2),
            round(max(st.session_state.response_times), 2),
            round(sorted(st.session_state.response_times)[len(st.session_state.response_times)//2], 2)
        ), unsafe_allow_html=True)
    else:
        st.info("📊 No analytics data yet. Start chatting to see performance metrics!")
    
    st.divider()
    
    # Agent mode distribution
    st.subheader("🤖 Current Configuration")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("""
        <div class="analytics-card">
            <h4>Active Workflow</h4>
            <p><strong>{}</strong></p>
            <p style="color: #64748B; font-size: 0.9rem;">
                {}
            </p>
        </div>
        """.format(
            agent_mode,
            "Fast single-pass reasoning" if "Standard" in agent_mode else
            "Multi-agent collaboration with quality checks" if "Quality" in agent_mode else
            "Autonomous RAG with web fallback"
        ), unsafe_allow_html=True)
    
    with col_b:
        st.markdown("""
        <div class="analytics-card">
            <h4>Session Info</h4>
            <p><strong>User:</strong> Rakshith PR</p>
            <p><strong>Role:</strong> Delivery Consultant Intern</p>
            <p><strong>Messages:</strong> {}</p>
        </div>
        """.format(total_messages), unsafe_allow_html=True)