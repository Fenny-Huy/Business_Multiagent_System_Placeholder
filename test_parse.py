from typing import Dict, Any, List

def _parse_structured_output(agent_output: str) -> tuple[str, Dict[str, Any]]:
        """Parse the structured output from the agent"""
        import re
        import json
        
        
        # Extract JSON from the agent output
        json_match = re.search(r'```json\s*(.*?)\s*```', agent_output, re.DOTALL)
        
        if json_match:
            try:
                json_data = json.loads(json_match.group(1))
                
                # Extract note and result from the JSON structure
                note = json_data.get("note", "SearchAgent completed search task")
                result = json_data.get("result", {})
                
                # Store the full output for reference
                result["full_agent_output"] = agent_output
                
                # Create a backward compatible structure for search_results
                search_results = {}
                
                # Extract data from tool outputs for backward compatibility
                tool_outputs = result.get("tool_outputs", {})
                
                # Extract businesses and reviews from tool outputs
                businesses = []
                reviews = []
                
                # Look for business data in tool outputs
                for tool_name, output in tool_outputs.items():
                    # Get business data from business search tools
                    if "business" in tool_name.lower() and isinstance(output, list):
                        businesses.extend(output)
                    elif isinstance(output, dict) and "businesses" in output:
                        businesses.extend(output["businesses"])
                    
                    # Get review data from review search tools
                    if "review" in tool_name.lower() and isinstance(output, list):
                        reviews.extend(output)
                    elif isinstance(output, dict) and "reviews" in output:
                        reviews.extend(output["reviews"])
                
                # Add to structured result for backward compatibility
                search_results["businesses"] = businesses
                search_results["reviews"] = reviews
                result["search_results"] = search_results
                
                # Debug logging
                print(f"✅ Successfully parsed structured output")
                print(f"  - Note: {note[:50]}...")
                print(f"  - Tool outputs found: {list(tool_outputs.keys())}")
                print(f"  - Businesses found: {len(businesses)}")
                print(f"  - Reviews found: {len(reviews)}")
                
                return note, result
                
            except json.JSONDecodeError as e:
                print(f"⚠️ Failed to parse JSON from agent output: {e}")
                print(f"⚠️ JSON snippet that failed parsing: {json_match.group(1)[:100]}...")
                return f"SearchAgent encountered error: {e}", {"error": str(e), "full_output": agent_output}
        else:
            # Fallback if no JSON found - this shouldn't happen if agent follows instructions
            print("⚠️ No JSON structure found in agent output")
            print(f"⚠️ Agent output: {agent_output[:200]}...")
            return "SearchAgent completed task (no structured output)", {"full_output": agent_output}
        


input = """
```json
{
  "note": "I found information about the Vietnamese Food Truck in Tampa Bay, FL, including its address, hours, rating, and other attributes.",
  "result": {
    "tool_outputs": {
      "get_business_id": [
        "eEOYSgkmpB90uNA7lDOMRA"
      ],
      "get_business_info": [
        "{\"business_id\": \"eEOYSgkmpB90uNA7lDOMRA\", \"name\": \"Vietnamese Food Truck\", \"address\": \"\", \"city\": \"Tampa Bay\", \"state\": \"FL\", \"postal_code\": \"33602\", \"latitude\": 27.9552692, \"longitude\": -82.4563199, \"stars\": 4.0, \"review_count\": 10, \"is_open\": true, \"attributes\": '{\'AcceptsInsurance\': None, \'AgesAllowed\': None, \'Alcohol\': \"\\'none\\'\", \'Ambience\': \"{\'touristy\': False, \'hipster\': False, \'romantic\': False, \'divey\': False, \'intimate\': False, \'trendy\': False, \'upscale\': False, \'classy\': False, \'casual\': False}\", \'BYOB\': None, \'BYOBCorkage\': None, \'BestNights\': None, \'BikeParking\': None, \'BusinessAcceptsBitcoin\': None, \'BusinessAcceptsCreditCards\': None, \'BusinessParking\': \"{\'garage\': False, \'street\': False, \'validated\': False, \'lot\': False, \'valet\': False}\", \'ByAppointmentOnly\': None, \'Caters\': None, \'CoatCheck\': None, \'Corkage\': None, \'DietaryRestrictions\': None, \'DogsAllowed\': None, \'DriveThru\': None, \'GoodForDancing\': None, \'GoodForKids\': None, \'GoodForMeal\': \"{\'dessert\': False, \'latenight\': False, \'lunch\': False, \'dinner\': False, \'brunch\': False, \'breakfast\': False}\", \'HairSpecializesIn\': None, \'HappyHour\': None, \'HasTV\': None, \'Music\': None, \'NoiseLevel\': None, \'Open24Hours\': None, \'OutdoorSeating\': \'None\', \'RestaurantsAttire\': None, \'RestaurantsCounterService\': None, \'RestaurantsDelivery\': None, \'RestaurantsGoodForGroups\': None, \'RestaurantsPriceRange2\': None, \'RestaurantsReservations\': \'False\', \'RestaurantsTableService\': None, \'RestaurantsTakeOut\': None, \'Smoking\': None, \'WheelchairAccessible\': None, \'WiFi\': None}', \"categories\": \"Vietnamese, Food, Restaurants, Food Trucks\", \"hours\": \"{'Friday': '11:0-14:0', 'Monday': '11:0-14:0', 'Saturday': '5:0-10:0', 'Sunday': '15:0-18:0', 'Thursday': '11:0-14:0', 'Tuesday': '11:0-14:0', 'Wednesday': '11:0-14:0'}\", \"created_at\": \"2025-09-25T01:50:58.520808\", \"updated_at\": \"2025-09-25T01:50:58.522807\"}"
      ]
    },
    "query_processed": "can you tell me some information about a business called Vietnamese Food Truck?",
    "reasoning_summary": "I first used get_business_id to find the business ID of 'Vietnamese Food Truck'. Then, I used get_business_info to retrieve detailed information about the business using the obtained business ID."
  }
}
```"""


note, result = _parse_structured_output(input)
print("Note:", note)
print("Result:", result)