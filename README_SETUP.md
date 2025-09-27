# LangGraph Multi-Agent Business Intelligence System - Setup Guide

## Quick Start

### Option 1: Using pip (Recommended)

```bash
# Create virtual environment
python -m venv langgraph-env

# Activate virtual environment
# On Windows:
langgraph-env\Scripts\activate
# On macOS/Linux:
source langgraph-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up API key
export GEMINI_API_KEY="your_google_api_key_here"
# On Windows:
set GEMINI_API_KEY=your_google_api_key_here

# Run the system
python langgraph_multiagent_system.py
```

### Option 2: Using Conda

```bash
# Create environment from file
conda env create -f langchain-demo-env.yml

# Activate environment
conda activate multi-agent-env

# Set up API key
export GEMINI_API_KEY="your_google_api_key_here"
# On Windows:
set GEMINI_API_KEY=your_google_api_key_here

# Run the system
python langgraph_multiagent_system.py
```

## Required Environment Variables

```bash
# Google Gemini API Key (required)
GEMINI_API_KEY=your_google_api_key_here

# ChromaDB Host (optional, defaults to localhost)
CHROMA_HOST=localhost
```

## Getting a Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Set it as an environment variable

## System Requirements

- **Python**: 3.10 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space for dependencies
- **Network**: Internet connection for API calls

## Key Dependencies

- **LangGraph**: Multi-agent orchestration framework
- **LangChain Google GenAI**: Official Google Gemini integration
- **ChromaDB**: Vector database for business/review search
- **Transformers**: Sentiment analysis models
- **Gemini 2.0 Flash Lite**: Fast, efficient LLM for multi-agent systems

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure `GEMINI_API_KEY` is set correctly
2. **ChromaDB Connection**: Ensure ChromaDB server is running if using external host
3. **Memory Issues**: Close other applications if experiencing OOM errors
4. **Rate Limits**: Gemini has free tier limits (10 requests/minute)

### Verification

Test your setup:
```bash
python -c "
import langgraph
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.business_search_tool import BusinessSearchTool
print('✅ All core dependencies working!')
"
```

## Architecture Overview

The system consists of:

1. **SearchAgent**: Uses ChromaDB to find business data and reviews
2. **AnalysisAgent**: Performs sentiment analysis on reviews
3. **ResponseAgent**: Synthesizes comprehensive final answers
4. **Supervisor**: Orchestrates workflow between agents

## Usage Modes

1. **Example Queries**: Pre-built demonstration queries
2. **Interactive Mode**: Chat with the system
3. **Single Query**: Test specific questions

## Performance Notes

- **Flash Lite Model**: Optimized for speed and cost efficiency
- **Parallel Tool Calls**: Multiple searches can run simultaneously
- **Smart Caching**: Results cached to avoid redundant API calls
- **Error Recovery**: Graceful fallbacks when services unavailable

## Next Steps

1. Run the system with example queries
2. Try your own business intelligence questions
3. Explore the logs in `logs/` directory
4. Customize agent prompts for your domain
5. Add new tools for additional data sources

For support, check the logs or review the LangGraph documentation.
