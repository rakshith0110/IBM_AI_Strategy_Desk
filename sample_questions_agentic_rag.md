# Sample Questions for Agentic RAG System

This document provides sample questions designed to test and demonstrate the capabilities of the IBM AI Strategy Desk's Agentic RAG workflow.

## 📋 Overview

The Agentic RAG system features:
- **Vector Store Retrieval**: Simulated document retrieval
- **LLM-based Grading**: Autonomous decision on document sufficiency
- **Web Search Fallback**: DuckDuckGo search when retrieval is insufficient
- **Executive Synthesis**: Professional strategy consultant-level responses

---

## 🎯 Category 1: Questions That Should Trigger Vector Store Only

These questions should be answerable with the simulated vector store data about IBM's historical stability.

### Basic Historical Queries
1. "What does IBM's historical stock data suggest about the company?"
2. "Is IBM a stable enterprise based on historical data?"
3. "Tell me about IBM's long-term stability"
4. "What can we learn from IBM's historical performance?"

### Expected Behavior
- ✅ Retrieve from vector store
- ✅ Grade as SUFFICIENT
- ✅ Generate answer without web search
- ⏱️ Fastest response time

---

## 🌐 Category 2: Questions That Should Trigger Web Search

These questions require current information not available in the vector store.

### Current Events & Recent Data
1. "What is IBM's stock price today?"
2. "What are IBM's latest quarterly earnings for 2026?"
3. "What is IBM's current market capitalization?"
4. "How did IBM stock perform this week?"

### Competitive Analysis
5. "Compare IBM vs Microsoft AI strategy in 2026"
6. "Who is leading in quantum computing: IBM or Google?"
7. "What is IBM's market share in cloud computing compared to AWS?"
8. "How does IBM's AI revenue compare to competitors?"

### Recent Announcements
9. "What are IBM's latest AI product announcements?"
10. "What acquisitions has IBM made in 2026?"
11. "What is IBM's latest partnership announcement?"
12. "What new services did IBM launch this year?"

### Technology & Innovation
13. "What is IBM's current AI strategy?"
14. "What are IBM's latest developments in quantum computing?"
15. "How is IBM using generative AI in its products?"
16. "What is IBM Watson's current capabilities?"

### Financial Performance
17. "What is IBM's revenue growth rate in 2026?"
18. "How profitable is IBM's cloud division?"
19. "What is IBM's R&D spending this year?"
20. "What are analysts saying about IBM's financial outlook?"

### Expected Behavior
- ✅ Retrieve from vector store
- ❌ Grade as INSUFFICIENT
- 🔍 Trigger web search
- ✅ Generate answer with web data
- ⏱️ Longer response time

---

## 🧪 Category 3: Edge Cases & System Testing

These questions test the system's robustness and decision-making.

### Ambiguous Queries
1. "Tell me about IBM"
2. "IBM performance"
3. "What's happening with IBM?"
4. "IBM news"

### Complex Multi-Part Questions
5. "Compare IBM's historical stability with its current AI strategy and predict future growth"
6. "How has IBM's stock performance correlated with its AI investments over the past 5 years?"
7. "Analyze IBM's competitive position considering both historical data and current market trends"

### Specific Technical Queries
8. "What is IBM's approach to responsible AI governance?"
9. "How does IBM's hybrid cloud architecture compare to competitors?"
10. "What programming languages does IBM Watson support?"

### Strategic Analysis
11. "Should I invest in IBM stock based on historical and current data?"
12. "What are the risks and opportunities for IBM in 2026?"
13. "How is IBM positioned for the future of enterprise AI?"

### Expected Behavior
- 🤔 System must decide retrieval sufficiency
- 🔄 May trigger iterative refinement
- 📊 Tests grading logic robustness

---

## 🎓 Category 4: Executive-Level Strategy Questions

These questions test the system's ability to provide professional, executive-level responses.

### Strategic Planning
1. "What should IBM's AI strategy focus on for the next 3 years?"
2. "How can IBM compete more effectively against Microsoft and Google in cloud?"
3. "What market opportunities should IBM prioritize?"

### Investment Analysis
4. "Is IBM a good long-term investment for institutional investors?"
5. "What are the key value drivers for IBM's stock?"
6. "How does IBM's dividend yield compare to tech peers?"

### Market Position
7. "What is IBM's competitive moat in enterprise AI?"
8. "How sustainable is IBM's business model?"
9. "What are IBM's key differentiators in the market?"

### Risk Assessment
10. "What are the biggest risks facing IBM in 2026?"
11. "How vulnerable is IBM to disruption from startups?"
12. "What regulatory challenges does IBM face?"

### Expected Behavior
- 📈 Professional, executive-level tone
- 📊 Data-driven insights
- 🎯 Strategic recommendations
- 💼 Business-focused analysis

---

## 🔬 Category 5: System Capability Testing

These questions specifically test different aspects of the agentic RAG pipeline.

### Testing Retrieval
1. "IBM historical data" (Should use vector store)
2. "IBM enterprise stability" (Should use vector store)

### Testing Grading Logic
3. "IBM stock historical trends and current price" (Mixed - tests grading decision)
4. "IBM's past performance and future outlook" (Mixed - tests grading decision)

### Testing Web Search
5. "Latest IBM news today" (Should trigger web search)
6. "IBM stock price right now" (Should trigger web search)

### Testing Synthesis
7. "Provide an executive summary of IBM's position in enterprise AI" (Tests synthesis quality)
8. "What makes IBM unique in the technology sector?" (Tests synthesis quality)

### Expected Behavior
- 🧪 Validates each pipeline component
- ✅ Confirms correct routing decisions
- 📝 Assesses output quality

---

## 📊 Usage Guidelines

### For Testing
1. Start with **Category 1** questions to verify basic retrieval
2. Move to **Category 2** to test web search fallback
3. Use **Category 3** for edge case validation
4. Apply **Category 4** for quality assessment
5. Employ **Category 5** for systematic testing

### For Demonstrations
- Use **Category 2** questions for impressive live demos
- Use **Category 4** for executive presentations
- Use **Category 1** for quick functionality demos

### For Development
- Use **Category 5** for debugging specific components
- Use **Category 3** for improving robustness
- Use **Category 2** for optimizing web search

---

## 🎯 Expected System Behavior Summary

| Question Type | Retrieval | Grading | Web Search | Response Quality |
|--------------|-----------|---------|------------|------------------|
| Historical | ✅ | SUFFICIENT | ❌ | Good |
| Current Events | ✅ | INSUFFICIENT | ✅ | Excellent |
| Competitive | ✅ | INSUFFICIENT | ✅ | Excellent |
| Strategic | ✅ | INSUFFICIENT | ✅ | Executive-level |
| Technical | ✅ | INSUFFICIENT | ✅ | Detailed |

---

## 🚀 Quick Start Examples

### Example 1: Fast Response (Vector Store Only)
**Question:** "What does IBM's historical data suggest?"
**Expected Flow:** Retrieve → Grade (SUFFICIENT) → Generate
**Response Time:** ~2-3 seconds

### Example 2: Web-Enhanced Response
**Question:** "Compare IBM vs Microsoft AI strategy in 2026"
**Expected Flow:** Retrieve → Grade (INSUFFICIENT) → Web Search → Generate
**Response Time:** ~5-8 seconds

### Example 3: Executive Analysis
**Question:** "Should institutional investors consider IBM stock?"
**Expected Flow:** Retrieve → Grade (INSUFFICIENT) → Web Search → Generate (Executive-level)
**Response Time:** ~5-8 seconds

---

## 📝 Notes

- All questions are designed for the **Autonomous (Agentic RAG)** workflow mode
- Questions can be adapted for other workflow modes (Standard, Quality)
- The system uses Llama 3.1 via Ollama for all LLM operations
- Web search is powered by DuckDuckGo
- Responses are tailored for IBM Strategy Consultant persona

---

## 🔄 Continuous Improvement

As you test the system, consider:
1. Adding questions that expose weaknesses
2. Documenting unexpected behaviors
3. Creating new categories for emerging use cases
4. Refining questions based on user feedback

---

**Last Updated:** March 20, 2026
**Version:** 1.0
**Author:** IBM AI Strategy Desk Team