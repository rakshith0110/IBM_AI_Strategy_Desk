# 🤖 IBM AI Strategy Desk

A sophisticated multi-agent AI system built with LangGraph and Ollama, featuring three distinct workflow modes for enterprise strategy consulting and analysis.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.0+-orange.svg)
![Ollama](https://img.shields.io/badge/Ollama-Llama3.1-red.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0+-ff4b4b.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow Modes](#workflow-modes)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Sample Questions](#sample-questions)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The IBM AI Strategy Desk is an advanced AI-powered consulting system that leverages multiple agent architectures to provide executive-level strategic insights. Built on LangGraph and powered by local Ollama models, it demonstrates three distinct approaches to AI agent design:

1. **Standard (ReAct Agent)** - Single agent with tool-calling capabilities and memory
2. **Quality (Multi-Agent System)** - Researcher-Critic collaboration with iterative refinement
3. **Autonomous (Agentic RAG)** - Self-routing RAG with web search fallback

## ✨ Features

### Core Capabilities
- 🧠 **Local LLM Integration** - Runs entirely on Ollama (Llama 3.1) - no API keys required
- 🔍 **Web Search Integration** - Real-time information retrieval via DuckDuckGo
- 💾 **Persistent Memory** - SQLite-based conversation history across sessions
- 🎨 **Modern UI** - Professional Streamlit interface with glassmorphism design
- 📊 **Execution Tracing** - Detailed step-by-step processing visualization
- 🔄 **Multiple Workflows** - Three distinct agent architectures for different use cases

### Advanced Features
- **ReAct Pattern** - Reasoning and Acting in iterative loops
- **Multi-Agent Collaboration** - Researcher and Critic agents working together
- **Agentic RAG** - Autonomous decision-making for retrieval augmentation
- **Quality Assurance** - Built-in critique and refinement loops
- **Executive-Level Output** - Professional strategy consultant persona

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                   │
│                  (Modern Glassmorphism UI)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Workflow Router                         │
│           (Selects appropriate agent system)                 │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────┐
│ ReactAgent   │    │ MultiAgentSystem │    │ AgenticRAG   │
│              │    │                  │    │              │
│ • Tool Call  │    │ • Researcher     │    │ • Retrieve   │
│ • Memory     │    │ • Critic         │    │ • Grade      │
│ • ReAct Loop │    │ • Iteration      │    │ • Web Search │
└──────────────┘    └──────────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌──────────────────┐
                    │  Ollama (Local)  │
                    │   Llama 3.1      │
                    └──────────────────┘
                              │
                    ┌──────────────────┐
                    │  DuckDuckGo API  │
                    │  (Web Search)    │
                    └──────────────────┘
```

### LangGraph Workflows

Each workflow is implemented as a state machine using LangGraph:

**1. ReAct Agent Flow:**
```
START → Agent → Router → [Tools] → Agent → END
                  ↓
                 END
```

**2. Multi-Agent Flow:**
```
START → Researcher → Critic → [Researcher] → Critic → END
                               ↑______________|
                              (if needs improvement)
```

**3. Agentic RAG Flow:**
```
START → Retrieve → Grade → [Web Search] → Generate → END
                     ↓
                  Generate → END
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- Llama 3.1 model pulled in Ollama

### Step 1: Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### Step 2: Pull Llama 3.1 Model

```bash
ollama pull llama3.1
```

### Step 3: Clone Repository

```bash
git clone https://github.com/yourusername/IBM_AI_Strategy_Desk.git
cd IBM_AI_Strategy_Desk
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment (Optional)

```bash
cp .env.example .env
# Edit .env if you need custom Ollama host configuration
```

## 💻 Usage

### Start Ollama Server

```bash
ollama serve
```

### Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Interface

1. **Select Workflow Mode** - Choose from the sidebar:
   - 🎯 Standard (ReAct Agent)
   - 🏆 Quality (Multi-Agent)
   - 🚀 Autonomous (Agentic RAG)

2. **Ask Questions** - Type your query in the chat input

3. **View Results** - See detailed execution traces and final responses

4. **Continue Conversation** - Memory persists across sessions (ReAct mode)

## 🔄 Workflow Modes

### 1. Standard (ReAct Agent) 🎯

**Best for:** General queries, conversational AI, tasks requiring tool use

**Features:**
- Single agent with reasoning capabilities
- Tool-calling (web search)
- Persistent memory across sessions
- Fast response times

**How it works:**
1. Agent receives query
2. Decides if tool use is needed
3. Calls tools if necessary
4. Generates response
5. Stores conversation in SQLite

**Example Use Cases:**
- "What is IBM's current stock price?"
- "Compare IBM vs Microsoft AI strategy"
- "Tell me about IBM Watson"

### 2. Quality (Multi-Agent System) 🏆

**Best for:** Complex analysis, high-quality reports, strategic insights

**Features:**
- Researcher agent for data gathering
- Critic agent for quality assurance
- Iterative refinement (up to 3 iterations)
- Executive-level output

**How it works:**
1. Researcher gathers and synthesizes information
2. Critic evaluates quality against criteria
3. If insufficient, Researcher refines
4. Repeats until quality standards met
5. Returns verified executive report

**Example Use Cases:**
- "Analyze IBM's competitive position in enterprise AI"
- "Provide strategic recommendations for IBM's cloud business"
- "Evaluate IBM's AI investment opportunities"

### 3. Autonomous (Agentic RAG) 🚀

**Best for:** Information retrieval, current events, data-driven queries

**Features:**
- Simulated vector store retrieval
- LLM-based sufficiency grading
- Automatic web search fallback
- Optimized for speed and accuracy

**How it works:**
1. Retrieves from vector store
2. LLM grades document sufficiency
3. If insufficient, triggers web search
4. Synthesizes final answer
5. Returns executive-level response

**Example Use Cases:**
- "What are IBM's latest quarterly earnings?"
- "IBM's historical stock performance"
- "Latest IBM AI product announcements"

## 📁 Project Structure

```
IBM_AI_Strategy_Desk/
│
├── app.py                          # Main Streamlit application
├── ReactAgent.py                   # Standard workflow (ReAct pattern)
├── MultiAgentSystem.py             # Quality workflow (Multi-agent)
├── AgenticRAG.py                   # Autonomous workflow (RAG)
│
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment configuration template
├── .gitignore                      # Git ignore rules
│
├── agent_memory.db                 # SQLite database (auto-generated)
├── agent_memory.db-shm            # SQLite shared memory
├── agent_memory.db-wal            # SQLite write-ahead log
│
├── ReactAgent_Guide.md            # Comprehensive ReAct agent guide
├── ReactAgent_Flowchart.md        # Detailed flowchart documentation
├── ReactAgent_Simple_Flowchart.md # Simplified flowchart
├── sample_questions_agentic_rag.md # Sample questions for testing
│
└── README.md                       # This file
```

## 🔧 Technical Details

### Dependencies

**Core Framework:**
- `streamlit>=1.31.0` - Web interface
- `python-dotenv>=1.0.0` - Environment management

**LangChain Ecosystem:**
- `langchain>=0.1.0` - LLM framework
- `langchain-core>=0.1.0` - Core abstractions
- `langchain-community>=0.0.20` - Community tools
- `langgraph>=0.2.0` - State machine graphs
- `langgraph-checkpoint>=1.0.0` - Checkpointing
- `langgraph-checkpoint-sqlite>=1.0.0` - SQLite persistence

**LLM Integration:**
- `langchain-ollama>=0.1.0` - Ollama integration

**Tools:**
- `duckduckgo-search>=4.0.0` - Web search
- `ddgs>=9.10.0` - DuckDuckGo search wrapper

### Model Configuration

**Default Model:** Llama 3.1 (via Ollama)
- **Temperature:** 0 (deterministic)
- **Context Window:** Optimized for tool stability
- **Tool Binding:** Enabled for ReAct agent

### Memory System

**Storage:** SQLite database (`agent_memory.db`)
- **Persistence:** Across sessions
- **Thread-based:** Separate conversations per thread_id
- **Checkpointing:** Automatic state saving

### Performance Characteristics

| Workflow | Avg Response Time | Memory Usage | Best For |
|----------|------------------|--------------|----------|
| Standard | 3-5 seconds | Low | General queries |
| Quality | 8-15 seconds | Medium | Complex analysis |
| Autonomous | 5-8 seconds | Low | Information retrieval |

## 📝 Sample Questions

### For Standard (ReAct Agent)
- "What is IBM's current stock price?"
- "Compare IBM vs Microsoft AI strategy"
- "Tell me about IBM Watson capabilities"
- "What are IBM's latest AI announcements?"

### For Quality (Multi-Agent)
- "Analyze IBM's competitive position in enterprise AI"
- "Provide strategic recommendations for IBM's cloud business"
- "Evaluate IBM's AI investment opportunities"
- "Compare IBM vs Microsoft 2026 AI strategy"

### For Autonomous (Agentic RAG)
- "What are IBM's latest quarterly earnings?"
- "IBM's historical stock performance"
- "Latest IBM AI product announcements"
- "IBM vs competitors in quantum computing"

See [sample_questions_agentic_rag.md](sample_questions_agentic_rag.md) for comprehensive test cases.

## 📚 Documentation

### Detailed Guides

- **[ReactAgent_Guide.md](ReactAgent_Guide.md)** - Complete guide to ReAct agent implementation (1000+ lines)
  - Step-by-step implementation
  - Code explanations
  - Working examples
  - Best practices
  - Troubleshooting

- **[ReactAgent_Flowchart.md](ReactAgent_Flowchart.md)** - Detailed flowchart documentation
  - Visual workflow representation
  - State transitions
  - Decision points

- **[sample_questions_agentic_rag.md](sample_questions_agentic_rag.md)** - Testing guide
  - Categorized sample questions
  - Expected behaviors
  - Testing strategies

### Key Concepts

**ReAct Pattern:**
- **Re**asoning: LLM thinks about the problem
- **Act**ing: LLM uses tools to gather information
- Iterative loop until task completion

**Multi-Agent Collaboration:**
- Specialized agents for different tasks
- Quality assurance through critique
- Iterative refinement

**Agentic RAG:**
- Autonomous decision-making
- Dynamic routing (vector store vs web search)
- LLM-based grading

## 🎨 UI Features

### Modern Design
- **Glassmorphism** - Frosted glass effect with blur
- **Gradient Backgrounds** - Smooth color transitions
- **Smooth Animations** - Fade-in, slide-in effects
- **Responsive Layout** - Adapts to screen size

### Execution Tracing
- **Step-by-step visualization** - See agent reasoning
- **Color-coded status** - Success, processing, error states
- **Detailed logs** - LLM calls, tool usage, decisions
- **Performance metrics** - Response times, iterations

## 🔒 Security & Privacy

- **Local Execution** - All LLM processing happens locally via Ollama
- **No API Keys** - No external API calls for LLM inference
- **Data Privacy** - Conversation history stored locally in SQLite
- **Web Search** - Only external call is DuckDuckGo (no tracking)

## 🐛 Troubleshooting

### Common Issues

**1. Ollama Connection Error**
```bash
# Ensure Ollama is running
ollama serve

# Check if model is available
ollama list
```

**2. Model Not Found**
```bash
# Pull the required model
ollama pull llama3.1
```

**3. Memory Database Locked**
```bash
# Close all running instances
# Delete database files
rm agent_memory.db*
```

**4. Slow Response Times**
```bash
# Check Ollama resource usage
# Consider using a smaller model
ollama pull llama3.1:8b
```

## 🚀 Future Enhancements

- [ ] Support for multiple LLM providers (OpenAI, Anthropic)
- [ ] Vector database integration (Chroma, Pinecone)
- [ ] Document upload and analysis
- [ ] Export conversation history
- [ ] Custom agent configuration
- [ ] API endpoint for programmatic access
- [ ] Multi-language support
- [ ] Advanced visualization tools

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

**IBM AI Strategy Desk Team**
- Rakshith PR - *Initial work and development*

## 🙏 Acknowledgments

- **LangChain** - For the excellent LLM framework
- **LangGraph** - For state machine orchestration
- **Ollama** - For local LLM inference
- **Streamlit** - For the web interface framework
- **IBM** - For the internship opportunity

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Contact: [Your Email]
- Documentation: See guides in repository

## 📊 Project Status

**Version:** 1.0.0  
**Status:** Active Development  
**Last Updated:** March 20, 2026  
**Python Version:** 3.8+  
**Tested On:** macOS, Linux

---

**Built with ❤️ for IBM Internship 2026**

*Demonstrating advanced AI agent architectures with LangGraph and Ollama*