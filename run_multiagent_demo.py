# run_multiagent_demo.py
from agents.orchestrator_agent import OrchestratorAgent

def main():
    user_query = "What is the best strategy for the given data?"
    orchestrator = OrchestratorAgent()
    final_state = orchestrator.run(user_query)
    print("\n=== Final State ===")
    for k, v in final_state.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
