# advanced_state_monitor.py
"""
Advanced state monitoring for the multi-agent system.
Provides detailed real-time inspection of AgentState changes.
"""

from multiagent_system import MultiAgentSystem, AgentState
from typing import Dict, Any, List
import json
import time
import os
from datetime import datetime

class AdvancedStateMonitor:
    """Advanced monitoring system for AgentState changes"""
    
    def __init__(self, save_to_file: bool = True, log_dir: str = "state_logs"):
        """Initialize the advanced monitor
        
        Args:
            save_to_file: Whether to save state changes to files
            log_dir: Directory to save state logs
        """
        self.save_to_file = save_to_file
        self.log_dir = log_dir
        self.state_history = []
        self.current_query = ""
        
        if save_to_file:
            os.makedirs(log_dir, exist_ok=True)
    
    def monitor_state_change(self, node_name: str, before_state: AgentState, after_state: AgentState):
        """Monitor and log state changes between before and after processing"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate differences
        changes = self._calculate_state_changes(before_state, after_state)
        
        # Create state change record
        state_record = {
            "timestamp": timestamp,
            "node": node_name,
            "query": self.current_query,
            "before_state": dict(before_state),
            "after_state": dict(after_state),
            "changes": changes
        }
        
        self.state_history.append(state_record)
        
        # Display changes
        self._display_detailed_changes(node_name, changes, timestamp)
        
        # Save to file if enabled
        if self.save_to_file:
            self._save_state_record(state_record)
    
    def _calculate_state_changes(self, before: AgentState, after: AgentState) -> Dict[str, Any]:
        """Calculate what changed between two states"""
        changes = {
            "added": {},
            "modified": {},
            "removed": {}
        }
        
        # Check each field
        for key in set(list(before.keys()) + list(after.keys())):
            before_val = before.get(key)
            after_val = after.get(key)
            
            if key not in before:
                changes["added"][key] = after_val
            elif key not in after:
                changes["removed"][key] = before_val
            elif before_val != after_val:
                changes["modified"][key] = {
                    "before": before_val,
                    "after": after_val,
                    "change_type": self._get_change_type(before_val, after_val)
                }
        
        return changes
    
    def _get_change_type(self, before_val: Any, after_val: Any) -> str:
        """Determine the type of change that occurred"""
        if isinstance(before_val, list) and isinstance(after_val, list):
            if len(after_val) > len(before_val):
                return "list_expanded"
            elif len(after_val) < len(before_val):
                return "list_reduced"
            else:
                return "list_modified"
        elif isinstance(before_val, dict) and isinstance(after_val, dict):
            before_keys = set(before_val.keys())
            after_keys = set(after_val.keys())
            if after_keys > before_keys:
                return "dict_expanded"
            elif after_keys < before_keys:
                return "dict_reduced"
            else:
                return "dict_modified"
        else:
            return "value_changed"
    
    def _display_detailed_changes(self, node_name: str, changes: Dict[str, Any], timestamp: str):
        """Display detailed state changes"""
        print(f"\n{'🔍 DETAILED STATE ANALYSIS':^80}")
        print(f"{'='*80}")
        print(f"Node: {node_name} | Time: {timestamp}")
        print(f"Query: {self.current_query}")
        print(f"{'='*80}")
        
        # Show added fields
        if changes["added"]:
            print(f"\n➕ ADDED FIELDS:")
            for key, value in changes["added"].items():
                print(f"  📝 {key}: {self._format_value_preview(value)}")
        
        # Show modified fields
        if changes["modified"]:
            print(f"\n🔄 MODIFIED FIELDS:")
            for key, change_info in changes["modified"].items():
                change_type = change_info["change_type"]
                print(f"  🔧 {key} ({change_type}):")
                
                if change_type == "list_expanded":
                    before_len = len(change_info["before"])
                    after_len = len(change_info["after"])
                    print(f"     📊 List size: {before_len} → {after_len} (+{after_len - before_len})")
                elif change_type == "dict_expanded":
                    before_keys = set(change_info["before"].keys())
                    after_keys = set(change_info["after"].keys())
                    new_keys = after_keys - before_keys
                    print(f"     🗝️  New keys: {list(new_keys)}")
                else:
                    print(f"     ⬅️ Before: {self._format_value_preview(change_info['before'])}")
                    print(f"     ➡️ After:  {self._format_value_preview(change_info['after'])}")
        
        # Show removed fields
        if changes["removed"]:
            print(f"\n➖ REMOVED FIELDS:")
            for key, value in changes["removed"].items():
                print(f"  🗑️ {key}: {self._format_value_preview(value)}")
        
        if not any(changes.values()):
            print("\n✅ No changes detected")
        
        print(f"{'='*80}")
        input("⏸️  Press Enter to continue...")
    
    def _format_value_preview(self, value: Any, max_length: int = 60) -> str:
        """Format value for preview display"""
        if isinstance(value, str):
            if len(value) > max_length:
                return f'"{value[:max_length]}..."'
            return f'"{value}"'
        elif isinstance(value, list):
            return f"List[{len(value)} items]"
        elif isinstance(value, dict):
            return f"Dict[{len(value)} keys: {list(value.keys())[:3]}{'...' if len(value) > 3 else ''}]"
        else:
            str_val = str(value)
            if len(str_val) > max_length:
                return str_val[:max_length] + "..."
            return str_val
    
    def _save_state_record(self, record: Dict[str, Any]):
        """Save state record to file"""
        timestamp = record["timestamp"].replace(":", "-").replace(" ", "_")
        filename = f"{self.log_dir}/state_log_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(record, f, indent=2, default=str, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Warning: Could not save state log: {e}")
    
    def set_current_query(self, query: str):
        """Set the current query being processed"""
        self.current_query = query
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get a summary of all state changes"""
        return {
            "total_states": len(self.state_history),
            "unique_nodes": list(set(record["node"] for record in self.state_history)),
            "queries_processed": list(set(record["query"] for record in self.state_history)),
            "last_update": self.state_history[-1]["timestamp"] if self.state_history else None
        }
    
    def export_full_history(self, filename: str = None):
        """Export complete state history to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.log_dir}/complete_state_history_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "summary": self.get_state_summary(),
                    "history": self.state_history
                }, f, indent=2, default=str, ensure_ascii=False)
            print(f"✅ State history exported to: {filename}")
        except Exception as e:
            print(f"❌ Error exporting history: {e}")


class MonitoredMultiAgentSystem(MultiAgentSystem):
    """MultiAgentSystem with advanced state monitoring"""
    
    def __init__(self, chroma_host: str = None, log_level: str = "INFO", 
                 enable_monitoring: bool = True, save_logs: bool = True):
        """Initialize system with monitoring"""
        self.monitor = AdvancedStateMonitor(save_to_file=save_logs) if enable_monitoring else None
        super().__init__(chroma_host=chroma_host, log_level=log_level, show_state_changes=False)
    
    def _supervisor_node(self, state: AgentState) -> AgentState:
        """Supervisor node with monitoring"""
        if self.monitor:
            before_state = state.copy()
        
        updated_state = super()._supervisor_node(state)
        
        if self.monitor:
            self.monitor.monitor_state_change("SUPERVISOR", before_state, updated_state)
        
        return updated_state
    
    def _search_agent_node(self, state: AgentState) -> AgentState:
        """Search agent node with monitoring"""
        if self.monitor:
            before_state = state.copy()
        
        # Process without the display (we'll handle it in monitor)
        self.logger.info("SearchAgent processing...")
        updated_state = self.search_agent.process(state)
        
        # Add message
        messages = updated_state.get("messages", [])
        search_results = updated_state.get("search_results", {})
        result_summary = []
        
        if "reviews" in search_results:
            result_summary.append(f"Found {len(search_results['reviews'])} reviews")
        if "businesses" in search_results:
            result_summary.append(f"Found {len(search_results['businesses'])} businesses")
        
        messages.append(f"SearchAgent completed: {', '.join(result_summary) if result_summary else 'No results'}")
        updated_state["messages"] = messages
        
        if self.monitor:
            self.monitor.monitor_state_change("SEARCH_AGENT", before_state, updated_state)
        
        return updated_state
    
    def _analysis_agent_node(self, state: AgentState) -> AgentState:
        """Analysis agent node with monitoring"""
        if self.monitor:
            before_state = state.copy()
        
        # Process without the display (we'll handle it in monitor)
        self.logger.info("AnalysisAgent processing...")
        updated_state = self.analysis_agent.process(state)
        
        # Add message
        messages = updated_state.get("messages", [])
        analysis_results = updated_state.get("analysis_results", {})
        analysis_summary = []
        
        if "sentiment_analysis" in analysis_results:
            sentiment = analysis_results["sentiment_analysis"]
            overall = sentiment.get("overall_sentiment", "Unknown")
            analysis_summary.append(f"Sentiment: {overall}")
        
        if "business_analysis" in analysis_results:
            business = analysis_results["business_analysis"] 
            avg_stars = business.get("average_stars", 0)
            analysis_summary.append(f"Avg rating: {avg_stars} stars")
        
        messages.append(f"AnalysisAgent completed: {', '.join(analysis_summary) if analysis_summary else 'No analysis'}")
        updated_state["messages"] = messages
        
        if self.monitor:
            self.monitor.monitor_state_change("ANALYSIS_AGENT", before_state, updated_state)
        
        return updated_state
    
    def _response_agent_node(self, state: AgentState) -> AgentState:
        """Response agent node with monitoring"""
        if self.monitor:
            before_state = state.copy()
        
        # Process without the display (we'll handle it in monitor)
        self.logger.info("ResponseAgent processing...")
        updated_state = self.response_agent.process(state)
        
        # Add message
        messages = updated_state.get("messages", [])
        has_response = bool(updated_state.get("final_response", ""))
        messages.append(f"ResponseAgent completed: {'Generated final response' if has_response else 'No response generated'}")
        updated_state["messages"] = messages
        
        if self.monitor:
            self.monitor.monitor_state_change("RESPONSE_AGENT", before_state, updated_state)
        
        return updated_state
    
    def process_query(self, user_query: str, max_iterations: int = 10) -> Dict[str, Any]:
        """Process query with monitoring"""
        if self.monitor:
            self.monitor.set_current_query(user_query)
        
        return super().process_query(user_query, max_iterations)


def main():
    """Run the advanced monitoring demo"""
    print("🔬 Advanced Multi-Agent State Monitor")
    print("="*60)
    
    # Configuration
    save_logs = input("Save state logs to files? (y/n, default=y): ").lower() != 'n'
    
    # Initialize monitored system
    system = MonitoredMultiAgentSystem(save_logs=save_logs)
    
    print("\n🎯 Advanced monitoring is now active!")
    print("You'll see detailed state changes before and after each agent processes.")
    print("Type 'quit' to exit and see summary.")
    print("="*60)
    
    try:
        while True:
            user_input = input("\n🧑 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', '']:
                break
            
            print(f"\n🚀 Processing query: {user_input}")
            result = system.process_query(user_input)
            
            if result["success"]:
                print(f"\n🎯 Final Result: {result['final_response']}")
            else:
                print(f"❌ Error: {result['error']}")
    
    except KeyboardInterrupt:
        pass
    
    # Show summary
    if system.monitor:
        print(f"\n📊 MONITORING SUMMARY:")
        print("="*40)
        summary = system.monitor.get_state_summary()
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        # Ask about exporting
        if input("\nExport complete history? (y/n): ").lower() == 'y':
            system.monitor.export_full_history()
    
    print("👋 Goodbye!")


if __name__ == "__main__":
    main()