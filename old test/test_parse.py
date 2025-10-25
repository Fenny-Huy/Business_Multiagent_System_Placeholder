import json
import re
from typing import Tuple, Dict, Any, Optional

def _parse_structured_output(agent_output: str) -> tuple[str, Dict[str, Any]]:
    """Parse the structured output from the agent"""
    # Extract JSON from the agent output
    json_match = re.search(r'```json\s*(.*?)\s*```', agent_output, re.DOTALL)
    if json_match:
        raw_json = json_match.group(1)
        try:
            parsed = json.loads(raw_json)
            note = parsed.get("note", "No note found")
            result = parsed.get("result", {})
            return note, result
        except Exception as e:
            print(f"⚠️ Error parsing JSON: {e}")
            return "SearchAgent completed task (invalid JSON)", {"full_output": raw_json}
    else:
        print("⚠️ No JSON structure found in agent output")
        print(f"⚠️ Agent output: {agent_output[:200]}...")
        return "SearchAgent completed task (no structured output)", {"full_output": agent_output}


# Test with the Vietnamese Food Truck example (with string-based JSON output)
input_vietnamese = """
```json
{
  "note": "I found two businesses that match the description 'Vietnamese Food Truck': 'Vietnamese Food Truck' and 'Chao Vietnamese Street Food'. I retrieved detailed information for both businesses.",
  "result": {
    "tool_outputs": {
      "search_businesses": [
        {
          "business_id": "eEOYSgkmpB90uNA7lDOMRA",
          "name": "Vietnamese Food Truck",
          "address": "",
          "stars": 4.0,
          "categories": "Vietnamese, Food, Restaurants, Food Trucks",
          "score": 0.43442684
        },
        {
          "business_id": "5gIfmupQTP3Lk4wIgNfoEQ",
          "name": "Chao Vietnamese Street Food",
          "address": "7854 E 96th St",
          "stars": 4.0,
          "categories": "Vietnamese, Restaurants",
          "score": 0.3315393
        }
      ],
      "get_business_info": [
        {
          "business_id": "eEOYSgkmpB90uNA7lDOMRA",
          "name": "Vietnamese Food Truck",
          "address": "",
          "city": "Tampa Bay",
          "state": "FL",
          "postal_code": "33602",
          "latitude": 27.9552692,
          "longitude": -82.4563199,
          "stars": 4.0,
          "review_count": 10,
          "is_open": true,
          "attributes": {
            "AcceptsInsurance": null,
            "AgesAllowed": null,
            "Alcohol": "'none'",
            "Ambience": "{'touristy': False, 'hipster': False, 'romantic': False, 'divey': False, 'intimate': False, 'trendy': False, 'upscale': False, 'classy': False, 'casual': False}",       
            "BYOB": null,
            "BYOBCorkage": null,
            "BestNights": null,
            "BikeParking": null,
            "BusinessAcceptsBitcoin": null,
            "BusinessAcceptsCreditCards": null,
            "BusinessParking": "{'garage': False, 'street': False, 'validated': False, 'lot': False, 'valet': False}",
            "ByAppointmentOnly": null,
            "Caters": null,
            "CoatCheck": null,
            "Corkage": null,
            "DietaryRestrictions": null,
            "DogsAllowed": null,
            "DriveThru": null,
            "GoodForDancing": null,
            "GoodForKids": null,
            "GoodForMeal": "{'dessert': False, 'latenight': False, 'lunch': False, 'dinner': False, 'brunch': False, 'breakfast': False}",
            "HairSpecializesIn": null,
            "HappyHour": null,
            "HasTV": null,
            "Music": null,
            "NoiseLevel": null,
            "Open24Hours": null,
            "OutdoorSeating": "None",
            "RestaurantsAttire": null,
            "RestaurantsCounterService": null,
            "RestaurantsDelivery": null,
            "RestaurantsGoodForGroups": null,
            "RestaurantsPriceRange2": null,
            "RestaurantsReservations": "False",
            "RestaurantsTableService": null,
            "RestaurantsTakeOut": null,
            "Smoking": null,
            "WheelchairAccessible": null,
            "WiFi": null
          },
          "categories": "Vietnamese, Food, Restaurants, Food Trucks",
          "hours": {
            "Friday": "11:0-14:0",
            "Monday": "11:0-14:0",
            "Saturday": "5:0-10:0",
            "Sunday": "15:0-18:0",
            "Thursday": "11:0-14:0",
            "Tuesday": "11:0-14:0",
            "Wednesday": "11:0-14:0"
          },
          "created_at": "2025-09-25T01:50:58.520808",
          "updated_at": "2025-09-25T01:50:58.522807"
        },
        {
          "business_id": "5gIfmupQTP3Lk4wIgNfoEQ",
          "name": "Chao Vietnamese Street Food",
          "address": "7854 E 96th St",
          "city": "Fishers",
          "state": "IN",
          "postal_code": "46037",
          "latitude": 39.9282154152,
          "longitude": -86.0245093592,
          "stars": 4.0,
          "review_count": 315,
          "is_open": true,
          "attributes": {
            "AcceptsInsurance": null,
            "AgesAllowed": null,
            "Alcohol": "u'beer_and_wine'",
            "Ambience": "{'touristy': False, 'hipster': None, 'romantic': False, 'divey': False, 'intimate': False, 'trendy': None, 'upscale': False, 'classy': False, 'casual': True}",
            "BYOB": null,
            "BYOBCorkage": null,
            "BestNights": null,
            "BikeParking": "True",
            "BusinessAcceptsBitcoin": null,
            "BusinessAcceptsCreditCards": "True",
            "BusinessParking": "{'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}",
            "ByAppointmentOnly": null,
            "Caters": "True",
            "CoatCheck": null,
            "Corkage": null,
            "DietaryRestrictions": null,
            "DogsAllowed": "False",
            "DriveThru": null,
            "GoodForDancing": null,
            "GoodForKids": "True",
            "GoodForMeal": "{'dessert': None, 'latenight': False, 'lunch': True, 'dinner': True, 'brunch': None, 'breakfast': False}",
            "HairSpecializesIn": null,
            "HappyHour": "False",
            "HasTV": "True",
            "Music": null,
            "NoiseLevel": "u'average'",
            "Open24Hours": null,
            "OutdoorSeating": "True",
            "RestaurantsAttire": "'casual'",
            "RestaurantsCounterService": null,
            "RestaurantsDelivery": "True",
            "RestaurantsGoodForGroups": "True",
            "RestaurantsPriceRange2": "2",
            "RestaurantsReservations": "False",
            "RestaurantsTableService": "True",
            "RestaurantsTakeOut": "True",
            "Smoking": null,
            "WheelchairAccessible": "True",
            "WiFi": "u'no'"
          },
          "categories": "Vietnamese, Restaurants",
          "hours": {
            "Friday": "16:0-20:0",
            "Monday": "0:0-0:0",
            "Saturday": "16:0-20:0",
            "Sunday": null,
            "Thursday": "16:0-20:0",
            "Tuesday": "16:0-20:0",
            "Wednesday": "16:0-20:0"
          },
          "created_at": "2025-09-25T01:50:58.520808",
          "updated_at": "2025-09-25T01:50:58.522807"
        }
      ]
    },
    "query_processed": "Find information about the Vietnamese Food Truck",
    "reasoning_summary": "The user is asking for information about a Vietnamese Food Truck. I used the `search_businesses` tool to find businesses matching that description, and then used the `get_business_info` tool to retrieve detailed information about the businesses found."
  }
}
```"""

# Test with the Pizza example (with normal JSON structure)
input_pizza = """
```json
{
  "note": "I found two pizza places in Philadelphia: Franco's Pizza and Castello Pizza. Franco's Pizza has 4 stars and is open, while Castello Pizza has 2.5 stars and is closed.",
  "result": {
    "tool_outputs": {
      "search_businesses": [
        [
          {
            "business_id": "6FJOC5YTJOBeF6fSedqOOA",
            "name": "Franco's Pizza",
            "address": "2573 Tulip St",
            "stars": 4.0,
            "categories": "Restaurants, Pizza",
            "score": 0.18483479999999997
          },
          {
            "business_id": "xZpgV4EKF1DACo__pQi2QQ",
            "name": "Castello Pizza",
            "address": "6700 Rising Sun Ave",
            "stars": 2.5,
            "categories": "Pizza, Restaurants",
            "score": 0.17310727000000004
          }
        ]
      ],
      "get_business_info": [
        {
          "business_id": "6FJOC5YTJOBeF6fSedqOOA",
          "name": "Franco's Pizza",
          "address": "2573 Tulip St",
          "city": "Philadelphia",
          "state": "PA",
          "postal_code": "19125",
          "latitude": 39.9820407,
          "longitude": -75.1215841,
          "stars": 4.0,
          "review_count": 141,
          "is_open": true,
          "attributes": {
            "AcceptsInsurance": null,
            "AgesAllowed": null,
            "Alcohol": "u'none'",
            "Ambience": "{u'divey': False, u'hipster': False, u'casual': None, u'touristy': False, u'trendy': None, u'intimate': False, u'romantic': False, u'classy': False, u'upscale': False}",
            "BYOB": null,
            "BYOBCorkage": null,
            "BestNights": null,
            "BikeParking": "False",
            "BusinessAcceptsBitcoin": null,
            "BusinessAcceptsCreditCards": "True",
            "BusinessParking": "{'garage': False, 'street': True, 'validated': False, 'lot': False, 'valet': False}",
            "ByAppointmentOnly": null,
            "Caters": "True",
            "CoatCheck": null,
            "Corkage": null,
            "DietaryRestrictions": null,
            "DogsAllowed": null,
            "DriveThru": null,
            "GoodForDancing": null,
            "GoodForKids": "True",
            "GoodForMeal": null,
            "HairSpecializesIn": null,
            "HappyHour": null,
            "HasTV": "True",
            "Music": null,
            "NoiseLevel": "u'average'",
            "Open24Hours": null,
            "OutdoorSeating": "False",
            "RestaurantsAttire": "u'casual'",
            "RestaurantsCounterService": null,
            "RestaurantsDelivery": "True",
            "RestaurantsGoodForGroups": "False",
            "RestaurantsPriceRange2": "1",
            "RestaurantsReservations": "False",
            "RestaurantsTableService": null,
            "RestaurantsTakeOut": "True",
            "Smoking": null,
            "WheelchairAccessible": null,
            "WiFi": "u'no'"
          },
          "categories": "Restaurants, Pizza",
          "hours": {
            "Friday": "11:0-23:30",
            "Monday": "11:0-22:30",
            "Saturday": "11:0-23:30",
            "Sunday": "12:0-22:0",
            "Thursday": "11:0-22:30",
            "Tuesday": "11:0-22:30",
            "Wednesday": "11:0-22:30"
          },
          "created_at": "2025-09-25T01:50:58.520808",
          "updated_at": "2025-09-25T01:50:58.522807"
        },
        {
          "business_id": "xZpgV4EKF1DACo__pQi2QQ",
          "name": "Castello Pizza",
          "address": "6700 Rising Sun Ave",
          "city": "Philadelphia",
          "state": "PA",
          "postal_code": "19111",
          "latitude": 40.0535314,
          "longitude": -75.092024,
          "stars": 2.5,
          "review_count": 8,
          "is_open": false,
          "attributes": {},
          "categories": "Pizza, Restaurants",
          "hours": {
            "Friday": "11:0-0:0",
            "Monday": "11:0-23:0",
            "Saturday": "11:0-0:0",
            "Sunday": "12:0-23:0",
            "Thursday": "11:0-23:0",
            "Tuesday": "11:0-23:0",
            "Wednesday": "11:0-23:0"
          },
          "created_at": "2025-09-25T01:50:58.520808",
          "updated_at": "2025-09-25T01:50:58.522807"
        }
      ]
    },
    "query_processed": "If I want to have pizza, where do you recommend?",
    "reasoning_summary": "The user is asking for a recommendation for pizza. I used the search_businesses tool to find businesses that serve pizza. Then, I used the get_business_info tool to get more information about these businesses."
  }
}
```"""


# Test Vietnamese Food Truck example (with string-based JSON output)
print("=== TESTING VIETNAMESE FOOD TRUCK EXAMPLE ===")
note_v, result_v = _parse_structured_output(input_vietnamese)
print("Note:", note_v)
print("Result: ", result_v)

# Test Pizza example (with normal JSON structure)
print("\n=== TESTING PIZZA RESTAURANTS EXAMPLE ===")
note_p, result_p = _parse_structured_output(input_pizza)
print("Note:", note_p)
print("Result: ", result_p)