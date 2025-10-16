import json

def parse_normal_json(agent_output: str):
    """Parse a normal JSON string and return the note and result fields."""
    data = json.loads(agent_output)
    note = data.get("note")
    result = data.get("result")
    return note, result

# Example normal JSON input
input_normal = '''
{
  "note": "This is a normal JSON input for testing.",
  "result": {
    "tool_outputs": {
      "search_businesses": [
        {
          "business_id": "abc123",
          "name": "Test Business",
          "stars": 5.0
        }
      ]
    },
    "query_processed": "Find information about Test Business",
    "reasoning_summary": "Used search_businesses tool to find Test Business."
  }
}
'''

if __name__ == "__main__":
    note, result = parse_normal_json(input_normal)
    print("Note:", note)
    print("Result:", result)
