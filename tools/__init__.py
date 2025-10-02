"""
Tool Organization System for Multi-Agent LangGraph Project

This module organizes all business intelligence tools by functionality and provides
easy access for different agent types. Tools are grouped into logical categories
based on their primary purpose.

Tool Categories:
- SEARCH_TOOLS: For finding businesses and reviews
- ANALYSIS_TOOLS: For analyzing data and extracting insights
- RESPONSE_TOOLS: For generating responses and action plans
- HYBRID_TOOLS: For combined retrieval and processing

Usage:
    from tools import SEARCH_TOOLS, ANALYSIS_TOOLS, ALL_TOOLS
    from tools import BusinessSearchTool, SentimentAnalysisTool
"""

# Core imports - Try to import all tools, fail gracefully if any are missing
import warnings
from typing import Dict, List, Any, Optional

# === IMPORT ALL TOOLS ===

# Search Tools
try:
    from .business_search_tool import BusinessSearchTool
    BUSINESS_SEARCH_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"BusinessSearchTool not available: {e}")
    BusinessSearchTool = None
    BUSINESS_SEARCH_AVAILABLE = False

try:
    from .review_search_tool import ReviewSearchTool
    REVIEW_SEARCH_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"ReviewSearchTool not available: {e}")
    ReviewSearchTool = None
    REVIEW_SEARCH_AVAILABLE = False

# Analysis Tools
try:
    from .sentiment_analysis_tool import SentimentAnalysisTool
    SENTIMENT_ANALYSIS_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"SentimentAnalysisTool not available: {e}")
    SentimentAnalysisTool = None
    SENTIMENT_ANALYSIS_AVAILABLE = False

try:
    from .aspect_analysis import AspectABSAToolHF
    ASPECT_ANALYSIS_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"AspectAnalysisTool not available: {e}")
    AspectABSAToolHF = None
    ASPECT_ANALYSIS_AVAILABLE = False

try:
    from .business_pulse import BusinessPulse
    BUSINESS_PULSE_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"BusinessPulseTool not available: {e}")
    BusinessPulse = None
    BUSINESS_PULSE_AVAILABLE = False

# Response Tools
try:
    from .ActionPlanner import ActionPlannerTool
    ACTION_PLANNER_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"ActionPlannerTool not available: {e}")
    ActionPlannerTool = None
    ACTION_PLANNER_AVAILABLE = False

try:
    from .ReviewResponseTool import ReviewResponseTool
    REVIEW_RESPONSE_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"ReviewResponseTool not available: {e}")
    ReviewResponseTool = None
    REVIEW_RESPONSE_AVAILABLE = False

# Hybrid Tools
try:
    from .hybrid_retrieval_tool import HybridRetrieve as HybridRetrievalTool
    HYBRID_RETRIEVAL_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"HybridRetrievalTool not available: {e}")
    HybridRetrievalTool = None
    HYBRID_RETRIEVAL_AVAILABLE = False

# === TOOL ORGANIZATION BY FUNCTIONALITY ===

# Search Tools - For finding and retrieving data
SEARCH_TOOLS = {
    'business_search': {
        'class': BusinessSearchTool,
        'available': BUSINESS_SEARCH_AVAILABLE,
        'description': 'Search for business information using ChromaDB',
        'primary_methods': ['search_businesses', 'get_business_by_id'],
        'suitable_for': ['SearchAgent', 'SupervisorAgent']
    },
    'review_search': {
        'class': ReviewSearchTool,
        'available': REVIEW_SEARCH_AVAILABLE,
        'description': 'Search for customer reviews using ChromaDB',
        'primary_methods': ['search_reviews'],
        'suitable_for': ['SearchAgent', 'SupervisorAgent']
    },
    'hybrid_retrieval': {
        'class': HybridRetrievalTool,
        'available': HYBRID_RETRIEVAL_AVAILABLE,
        'description': 'Advanced semantic search with evidence generation',
        'primary_methods': ['__call__'],
        'suitable_for': ['SearchAgent', 'AnalysisAgent']
    }
}

# Analysis Tools - For processing and analyzing data
ANALYSIS_TOOLS = {
    'sentiment_analysis': {
        'class': SentimentAnalysisTool,
        'available': SENTIMENT_ANALYSIS_AVAILABLE,
        'description': 'Analyze sentiment in customer reviews',
        'primary_methods': ['analyze_reviews'],
        'suitable_for': ['AnalysisAgent', 'SupervisorAgent']
    },
    'aspect_analysis': {
        'class': AspectABSAToolHF,
        'available': ASPECT_ANALYSIS_AVAILABLE,
        'description': 'Aspect-based sentiment analysis using ABSA models',
        'primary_methods': ['analyze_aspects', 'read_data'],
        'suitable_for': ['AnalysisAgent']
    },
    'business_pulse': {
        'class': BusinessPulse,
        'available': BUSINESS_PULSE_AVAILABLE,
        'description': 'Business health metrics and sanity checks',
        'primary_methods': ['__call__'],
        'suitable_for': ['AnalysisAgent', 'SupervisorAgent']
    }
}

# Response Tools - For generating outputs and action plans
RESPONSE_TOOLS = {
    'action_planner': {
        'class': ActionPlannerTool,
        'available': ACTION_PLANNER_AVAILABLE,
        'description': 'Generate actionable business improvement plans',
        'primary_methods': ['__call__'],
        'suitable_for': ['ResponseAgent', 'SupervisorAgent']
    },
    'review_response': {
        'class': ReviewResponseTool,
        'available': REVIEW_RESPONSE_AVAILABLE,
        'description': 'Generate personalized responses to customer reviews',
        'primary_methods': ['__call__'],
        'suitable_for': ['ResponseAgent']
    }
}

# === COMBINED TOOL COLLECTIONS ===

# All tools organized by category
ALL_TOOLS_BY_CATEGORY = {
    'search': SEARCH_TOOLS,
    'analysis': ANALYSIS_TOOLS,
    'response': RESPONSE_TOOLS
}

# Flat dictionary of all available tools
ALL_TOOLS = {}
for category, tools in ALL_TOOLS_BY_CATEGORY.items():
    for tool_name, tool_info in tools.items():
        if tool_info['available']:
            ALL_TOOLS[tool_name] = tool_info

# === AGENT-SPECIFIC TOOL COLLECTIONS ===

def get_tools_for_agent(agent_type: str) -> Dict[str, Any]:
    """
    Get appropriate tools for a specific agent type.
    
    Args:
        agent_type: Type of agent ('search', 'analysis', 'response', 'supervisor')
    
    Returns:
        Dictionary of available tools for the agent
    """
    agent_tools = {}
    
    for tool_name, tool_info in ALL_TOOLS.items():
        suitable_agents = tool_info.get('suitable_for', [])
        agent_key = f"{agent_type.title()}Agent"
        
        if agent_key in suitable_agents or 'SupervisorAgent' in suitable_agents:
            agent_tools[tool_name] = tool_info
    
    return agent_tools

def get_search_agent_tools() -> Dict[str, Any]:
    """Get tools suitable for SearchAgent"""
    return get_tools_for_agent('search')

def get_analysis_agent_tools() -> Dict[str, Any]:
    """Get tools suitable for AnalysisAgent"""
    return get_tools_for_agent('analysis')

def get_response_agent_tools() -> Dict[str, Any]:
    """Get tools suitable for ResponseAgent"""
    return get_tools_for_agent('response')

def get_supervisor_agent_tools() -> Dict[str, Any]:
    """Get tools suitable for SupervisorAgent (usually all tools)"""
    return ALL_TOOLS

# === TOOL INSTANTIATION HELPERS ===

def create_tool_instance(tool_name: str, **kwargs) -> Optional[Any]:
    """
    Create an instance of a tool by name.
    
    Args:
        tool_name: Name of the tool to create
        **kwargs: Arguments to pass to the tool constructor
    
    Returns:
        Tool instance or None if tool not available
    """
    if tool_name not in ALL_TOOLS:
        warnings.warn(f"Tool '{tool_name}' not available")
        return None
    
    tool_info = ALL_TOOLS[tool_name]
    tool_class = tool_info['class']
    
    if tool_class is None:
        warnings.warn(f"Tool class for '{tool_name}' is None")
        return None
    
    try:
        return tool_class(**kwargs)
    except Exception as e:
        warnings.warn(f"Failed to create tool '{tool_name}': {e}")
        return None

def create_all_available_tools(**kwargs) -> Dict[str, Any]:
    """
    Create instances of all available tools.
    
    Args:
        **kwargs: Common arguments to pass to all tool constructors
    
    Returns:
        Dictionary of tool instances
    """
    tool_instances = {}
    
    for tool_name in ALL_TOOLS:
        instance = create_tool_instance(tool_name, **kwargs)
        if instance is not None:
            tool_instances[tool_name] = instance
    
    return tool_instances

def create_agent_tools(agent_type: str, **kwargs) -> Dict[str, Any]:
    """
    Create tool instances for a specific agent type.
    
    Args:
        agent_type: Type of agent ('search', 'analysis', 'response', 'supervisor')
        **kwargs: Arguments to pass to tool constructors
    
    Returns:
        Dictionary of tool instances for the agent
    """
    agent_tools = get_tools_for_agent(agent_type)
    tool_instances = {}
    
    for tool_name in agent_tools:
        instance = create_tool_instance(tool_name, **kwargs)
        if instance is not None:
            tool_instances[tool_name] = instance
    
    return tool_instances

# === SYSTEM STATUS AND DIAGNOSTICS ===

def get_tool_status() -> Dict[str, Any]:
    """
    Get status of all tools for diagnostics.
    
    Returns:
        Dictionary with tool availability status
    """
    status = {
        'total_tools': len(ALL_TOOLS_BY_CATEGORY['search']) + len(ALL_TOOLS_BY_CATEGORY['analysis']) + len(ALL_TOOLS_BY_CATEGORY['response']),
        'available_tools': len(ALL_TOOLS),
        'by_category': {}
    }
    
    for category, tools in ALL_TOOLS_BY_CATEGORY.items():
        available = sum(1 for tool in tools.values() if tool['available'])
        total = len(tools)
        status['by_category'][category] = {
            'available': available,
            'total': total,
            'tools': {name: info['available'] for name, info in tools.items()}
        }
    
    return status

def print_tool_summary():
    """Print a summary of available tools"""
    status = get_tool_status()
    
    print("🔧 Tool Organization System Status")
    print("=" * 40)
    print(f"Total Tools: {status['available_tools']}/{status['total_tools']} available")
    
    for category, info in status['by_category'].items():
        print(f"\n📂 {category.upper()} TOOLS ({info['available']}/{info['total']} available):")
        for tool_name, available in info['tools'].items():
            status_icon = "✅" if available else "❌"
            tool_info = ALL_TOOLS_BY_CATEGORY[category][tool_name]
            print(f"  {status_icon} {tool_name}: {tool_info['description']}")

# === EXPORTS ===

# Export main tool classes (if available)
__all__ = [
    # Tool classes
    'BusinessSearchTool', 'ReviewSearchTool', 'SentimentAnalysisTool',
    'AspectABSAToolHF', 'BusinessPulse', 'ActionPlannerTool', 
    'ReviewResponseTool', 'HybridRetrievalTool',
    
    # Tool collections
    'SEARCH_TOOLS', 'ANALYSIS_TOOLS', 'RESPONSE_TOOLS', 
    'ALL_TOOLS', 'ALL_TOOLS_BY_CATEGORY',
    
    # Helper functions
    'get_tools_for_agent', 'get_search_agent_tools', 'get_analysis_agent_tools',
    'get_response_agent_tools', 'get_supervisor_agent_tools',
    'create_tool_instance', 'create_all_available_tools', 'create_agent_tools',
    
    # Diagnostics
    'get_tool_status', 'print_tool_summary'
]

# Print status on import (can be disabled by setting environment variable)
import os
if os.getenv('TOOLS_QUIET_IMPORT', '').lower() not in ('1', 'true', 'yes'):
    print_tool_summary()