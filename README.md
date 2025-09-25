# README.md
# Multi-Agent Business Intelligence System with LangGraph

A sophisticated multi-agent system built with LangGraph that coordinates specialized agents to handle business intelligence queries about restaurants and reviews.

## Overview

This system uses a **supervisor approach** where a coordinator agent routes tasks between specialized agents:

- **SupervisorAgent**: Coordinates and routes tasks between agents
- **SearchAgent**: Finds reviews and business information from ChromaDB
- **AnalysisAgent**: Performs sentiment analysis and data insights  
- **ResponseAgent**: Generates comprehensive responses and recommendations

## Architecture

```
User Query → SupervisorAgent → [SearchAgent/AnalysisAgent/ResponseAgent] → Final Response
                ↑                                    ↓
                ←────────────────────────────────────
```

## Features

- **Multi-agent coordination** using LangGraph state management
- **ChromaDB integration** for semantic search of reviews and businesses
- **Sentiment analysis** using HuggingFace transformers
- **Flexible input handling** supporting JSON strings and dictionaries
- **Gemini LLM integration** for natural language processing
- **Comprehensive logging** and error handling

## Setup Instructions

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Configure API Keys

Set your Gemini API key:
```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
```

Or create a `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
CHROMA_HOST=localhost
```

### 3. Transfer Data Files

Copy these from your original project:
- `chroma_db/` folder → `move_on_G2/data/chroma_db/`
- `business_chroma_db/` folder → `move_on_G2/data/business_chroma_db/`
- `*.duckdb` files → `move_on_G2/data/` (if needed)

### 4. Start ChromaDB Servers

Start the review search server:
```powershell
chroma run --host localhost --port 8001 --path ./data/chroma_db
```

Start the business search server (in another terminal):
```powershell
chroma run --host localhost --port 8000 --path ./data/business_chroma_db
```

## Usage

### Basic Usage

```python
from multiagent_system import MultiAgentSystem

# Initialize system
system = MultiAgentSystem(chroma_host="localhost")

# Process a query
result = system.process_query("What do people say about Italian restaurants?")

print(result["final_response"])
```

### Example Queries

- "Find reviews for Hernandez Restaurant"
- "What's the sentiment about pizza places?"
- "Show me highly rated businesses in the food category"
- "Analyze customer feedback for business ID ABC123"

### Advanced Usage

```python
# Custom configuration
system = MultiAgentSystem(
    chroma_host="your-chroma-host",
    log_level="DEBUG"
)

# Process with full results
result = system.process_query("Your query here")

if result["success"]:
    print("Response:", result["final_response"])
    print("Search Results:", result["search_results"])
    print("Analysis:", result["analysis_results"])
    print("Execution Log:", result["execution_log"])
```

## Project Structure

```
move_on_G2/
├── agents/                 # Specialized agent implementations
│   ├── base_agent.py      # Base agent class
│   ├── supervisor_agent.py # Coordinator agent
│   ├── search_agent.py    # Data retrieval agent
│   ├── analysis_agent.py  # Data analysis agent
│   └── response_agent.py  # Response generation agent
├── tools/                 # Tool implementations
│   ├── review_search_tool.py
│   ├── business_search_tool.py
│   └── sentiment_analysis_tool.py
├── llm/                   # LLM integrations
│   └── gemini_llm.py     # Gemini API wrapper
├── config/               # Configuration modules
│   ├── api_keys.py       # Secure API key management
│   └── logging_config.py # Logging setup
├── data/                 # Data storage
├── logs/                 # Log files
├── multiagent_system.py  # Main system orchestrator
└── requirements.txt      # Dependencies
```

## Key Components

### Agent Communication

Agents communicate through a shared `AgentState` that contains:
- `user_query`: Original user question
- `search_results`: Data retrieved by SearchAgent
- `analysis_results`: Insights from AnalysisAgent  
- `final_response`: Generated response
- `messages`: Execution log

### Tool Integration

Tools are designed with flexible input handling:
```python
# Supports multiple input formats
tool("simple string query")
tool({"query": "complex query", "k": 10, "business_id": "ABC123"})
tool('{"query": "JSON string", "k": 5}')
```

### Error Handling

- Graceful degradation when services are unavailable
- Comprehensive error logging
- Fallback responses for failed operations

## Monitoring and Debugging

Enable debug logging:
```python
system = MultiAgentSystem(log_level="DEBUG")
```

View execution flow:
```python
result = system.process_query("Your query")
for message in result["execution_log"]:
    print(f"- {message}")
```

## Extending the System

### Adding New Agents

1. Inherit from `BaseAgent`
2. Implement required methods
3. Add to supervisor's available agents
4. Update workflow graph

### Adding New Tools

1. Create tool class with flexible input handling
2. Add to appropriate agent's tool list
3. Update agent descriptions

## Troubleshooting

**ChromaDB Connection Issues:**
- Ensure ChromaDB servers are running
- Check host/port configuration
- Verify data directories exist

**API Key Issues:**
- Check environment variables
- Verify API key permissions
- Use APIKeyManager for secure storage

**Import Errors:**
- Install all requirements: `pip install -r requirements.txt`
- Check Python environment activation

## License

This project is part of the COS30018 Intelligent Systems course.