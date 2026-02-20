# IBM AI Strategy Desk

A sophisticated multi-agent AI system built with LangChain, LangGraph, and Streamlit, featuring three distinct workflow modes for strategic analysis and research.

## 🚀 Features

### Three Workflow Modes

1. **🚀 Standard (Single Agent)**
   - Fast, single-agent ReAct pattern
   - Persistent conversation memory using SQLite
   - DuckDuckGo search integration
   - Ideal for quick queries and straightforward tasks

2. **👥 Quality (Multi-Agent Team)**
   - Collaborative researcher-critic workflow
   - Live competitive audit capabilities
   - Quality assurance with iterative refinement
   - Maximum 3 iteration safety brake
   - Perfect for in-depth analysis requiring validation

3. **🤖 Autonomous (Agentic RAG)**
   - Self-correcting RAG pipeline
   - Autonomous decision-making for web search fallback
   - Document grading and relevance assessment
   - Ideal for research tasks requiring retrieval augmentation

## 📋 Prerequisites

- Python 3.8 or higher
- GROQ API key ([Get one here](https://console.groq.com/keys))

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd MAG
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your GROQ API key:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

## 🚀 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Interface

1. **Select Workflow Mode** - Choose from the sidebar:
   - Standard for quick responses
   - Quality for validated research
   - Autonomous for RAG-enhanced queries

2. **Ask Questions** - Type your query in the chat input
   - "Compare IBM vs Microsoft AI strategy"
   - "What is IBM's latest stock performance?"
   - "Analyze IBM's competitive position in 2026"

3. **View System Architecture** - Switch to the "System Architecture" tab to visualize the agent workflow graph

## 📁 Project Structure

```
MAG/
├── app.py                    # Main Streamlit application
├── MultiAgentSystem.py       # Multi-agent researcher-critic workflow
├── ReactAgent.py             # Single agent with ReAct pattern
├── AgenticRAG.py            # Autonomous RAG pipeline
├── agent_memory.db          # SQLite database for conversation memory
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

- `GROQ_API_KEY` - Your GROQ API key for LLM access

### Model Configuration

All agents use `llama-3.1-8b-instant` by default. To change the model, edit the respective agent files:

```python
model = ChatGroq(model="your-preferred-model", temperature=0)
```

## 🔒 Security

- **Never commit `.env` file** - It contains sensitive API keys
- The `.gitignore` file is configured to exclude `.env` automatically
- Use `.env.example` as a template for new setups
- Rotate API keys regularly

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **API key not found**
   - Ensure `.env` file exists in the project root
   - Verify `GROQ_API_KEY` is set correctly
   - Restart the Streamlit application

3. **Database locked errors**
   - Close any other instances of the application
   - Delete `agent_memory.db` to reset conversation history

4. **Graph visualization not working**
   - Install optional dependencies:
     ```bash
     pip install pyppeteer
     ```

## 📊 System Architecture

### Multi-Agent System Flow
```
User Query → Researcher (Web Search) → Critic (Quality Check) → [Loop if needed] → Final Report
```

### Single Agent Flow
```
User Query → Agent (with Tools) → [Tool Execution if needed] → Response
```

### Agentic RAG Flow
```
User Query → Retrieve → Grade → [Web Search if needed] → Generate → Response
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for internal IBM use. All rights reserved.

## 👤 Author

**Praveen Kumar Reddy**  
Delivery Consultant Intern, IBM

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [LangGraph](https://langchain-ai.github.io/langgraph/)
- UI by [Streamlit](https://streamlit.io/)
- LLM by [GROQ](https://groq.com/)