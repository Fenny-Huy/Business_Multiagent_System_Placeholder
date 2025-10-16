import re
import json

def _find_balanced_braces(s, start_index):
    """Return substring that is the balanced {...} starting at start_index (s[start_index] == '{')."""
    assert s[start_index] == '{'
    i = start_index
    depth = 0
    in_string = False
    escape = False
    while i < len(s):
        ch = s[i]
        if escape:
            escape = False
        elif ch == '\\':
            escape = True
        elif ch == '"' and not escape:
            in_string = not in_string
        elif not in_string:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return s[start_index:i+1], i+1
        i += 1
    raise ValueError("Unbalanced braces starting at index {}".format(start_index))

def _parse_structured_output(text):
    """
    Return (note, result) where:
      - note is a Python string (or None)
      - result is either a Python object (if JSON parse succeeded) or a raw string containing the {...} after "result"
    """
    # extract fenced block if present
    m = re.search(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    content = m.group(1) if m else text

    # extract note
    note = None
    nm = re.search(r'"note"\s*:\s*("(?:\\.|[^"\\])*")', content, flags=re.DOTALL)
    if nm:
        try:
            note = json.loads(nm.group(1))
        except Exception:
            # fallback: raw trimming of surrounding quotes
            note = nm.group(1).strip('"')

    # locate "result" followed by an object
    rm = re.search(r'"result"\s*:\s*({)', content, flags=re.DOTALL)
    if not rm:
        return note, None

    start = rm.start(1)
    try:
        result_text, endpos = _find_balanced_braces(content, start)
    except ValueError:
        # if braces are unbalanced, return remaining substring after "result":
        result_text = content[rm.end():].strip()
        return note, result_text

    # try to parse JSON; if fails, return raw text
    try:
        parsed = json.loads(result_text)
        return note, parsed
    except Exception:
        return note, result_text.strip()




# Test with the Vietnamese Food Truck example (with string-based JSON output)
input_vietnamese = """
```json
{
  "note": "Found two businesses related to the query 'Vietnamese Food Truck': 'Vietnamese Food Truck' and 'Chao Vietnamese Street Food'. Detailed information for both businesses has been retrieved.",
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
          "attributes": "{\"AcceptsInsurance\": None, \"AgesAllowed\": None, \"Alcohol\": \"\"none\"\", \"Ambience\": \"{\"touristy\": False, \"hipster\": False, \"romantic\": False, \"divey\": False, \"intimate\": False, \"trendy\": False, \"upscale\": False, \"classy\": False, \"casual\": False}\", \"BYOB\": None, \"BYOBCorkage\": None, \"BestNights\": None, \"BikeParking\": None, \"BusinessAcceptsBitcoin\": None, \"BusinessAcceptsCreditCards\": None, \"BusinessParking\": \"{\"garage\": False, \"street\": False, \"validated\": False, \"lot\": False, \"valet\": False}\", \"ByAppointmentOnly\": None, \"Caters\": None, \"CoatCheck\": None, \"Corkage\": None, \"DietaryRestrictions\": None, \"DogsAllowed\": None, \"DriveThr\": None, \"GoodForDancing\": None, \"GoodForKids\": None, \"GoodForMeal\": \"{\"dessert\": False, \"latenight\": False, \"lunch\": False, \"dinner\": False, \"brunch\": False, \"breakfast\": False}\", \"HairSpecializesIn\": None, \"HappyHour\": None, \"HasTV\": None, \"Music\": None, \"NoiseLevel\": None, \"Open24Hours\": None, \"OutdoorSeating\": \"None\", \"RestaurantsAttire\": None, \"RestaurantsCounterService\": None, \"RestaurantsDelivery\": None, \"RestaurantsGoodForGroups\": None, \"RestaurantsPriceRange2\": None, \"RestaurantsReservations\": \"False\", \"RestaurantsTableService\": None, \"RestaurantsTakeOut\": None, \"Smoking\": None, \"WheelchairAccessible\": None, \"WiFi\": None}",
          "categories": "Vietnamese, Food, Restaurants, Food Trucks",
          "hours": "{\"Friday\": \"11:0-14:0\", \"Monday\": \"11:0-14:0\", \"Saturday\": \"5:0-10:0\", \"Sunday\": \"15:0-18:0\", \"Thursday\": \"11:0-14:0\", \"Tuesday\": \"11:0-14:0\", \"Wednesday\": \"11:0-14:0\"}",
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
          "attributes": "{\"AcceptsInsurance\": None, \"AgesAllowed\": None, \"Alcohol\": \"\"beer_and_wine\"\", \"Ambience\": \"{\"touristy\": False, \"hipster\": None, \"romantic\": False, \"divey\": False, \"intimate\": False, \"trendy\": None, \"upscale\": False, \"classy\": False, \"casual\": True}\", \"BYOB\": None, \"BYOBCorkage\": None, \"BestNights\": None, \"BikeParking\": \"True\", \"BusinessAcceptsBitcoin\": None, \"BusinessAcceptsCreditCards\": \"True\", \"BusinessParking\": \"{\"garage\": False, \"street\": False, \"validated\": False, \"lot\": True, \"valet\": False}\", \"ByAppointmentOnly\": None, \"Caters\": \"True\", \"CoatCheck\": None, \"Corkage\": None, \"DietaryRestrictions\": None, \"DogsAllowed\": \"False\", \"DriveThr\": None, \"GoodForDancing\": None, \"GoodForKids\": \"True\", \"GoodForMeal\": \"{\"dessert\": None, \"latenight\": False, \"lunch\": True, \"dinner\": True, \"brunch\": None, \"breakfast\": False}\", \"HairSpecializesIn\": None, \"HappyHour\": \"False\", \"HasTV\": \"True\", \"Music\": None, \"NoiseLevel\": \"\"average\"\", \"Open24Hours\": None, \"OutdoorSeating\": \"True\", \"RestaurantsAttire\": \"\"casual\"\", \"RestaurantsCounterService\": None, \"RestaurantsDelivery\": \"True\", \"RestaurantsGoodForGroups\": \"True\", \"RestaurantsPriceRange2\": \"2\", \"RestaurantsReservations\": \"False\", \"RestaurantsTableService\": \"True\", \"RestaurantsTakeOut\": \"True\", \"Smoking\": None, \"WheelchairAccessible\": \"True\", \"WiFi\": \"\"no\"\"}",
          "categories": "Vietnamese, Restaurants",
          "hours": "{\"Friday\": \"16:0-20:0\", \"Monday\": \"0:0-0:0\", \"Saturday\": \"16:0-20:0\", \"Sunday\": null, \"Thursday\": \"16:0-20:0\", \"Tuesday\": \"16:0-20:0\", \"Wednesday\": \"16:0-20:0\"}",
          "created_at": "2025-09-25T01:50:58.520808",
          "updated_at": "2025-09-25T01:50:58.522807"
        }
      ]
    },
    "query_processed": "Find information about the Vietnamese Food Truck",
    "reasoning_summary": "The user requested information about 'Vietnamese Food Truck'. I used the `search_businesses` tool to find relevant businesses and then used the `get_business_info` tool to retrieve detailed information for each found business. Two businesses were found: 'Vietnamese Food Truck' and 'Chao Vietnamese Street Food'."
  }
}
```"""

# Test with the Pizza example (with normal JSON structure)
input_pizza = """
```json
{
  "note": "I found two pizza restaurants in Philadelphia: Franco's Pizza and Castello Pizza. Franco's Pizza has a 4.0-star rating and is currently open, while Castello Pizza has a 2.5-star rating and is closed.",
  "result": {
    "tool_outputs": {
      "search_businesses": [
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
          "attributes": "{\"AcceptsInsurance\": None, \"AgesAllowed\": None, \"Alcohol\": \"\"none\"\", \"Ambience\": \"{\"divey\": False, \"hipster\": False, \"casual\": None, \"touristy\": False, \"trendy\": None, \"intimate\": False, \"romantic\": False, \"classy\": False, \"upscale\": False}\", \"BYOB\": None, \"BYOBCorkage\": None, \"BestNights\": None, \"BikeParking\": \"False\", \"BusinessAcceptsBitcoin\": None, \"BusinessAcceptsCreditCards\": \"True\", \"BusinessParking\": \"{\"garage\": False, \"street\": True, \"validated\": False, \"lot\": False, \"valet\": False}\", \"ByAppointmentOnly\": None, \"Caters\": \"True\", \"CoatCheck\": None, \"Corkage\": None, \"DietaryRestrictions\": None, \"DogsAllowed\": None, \"DriveThr\": None, \"GoodForDancing\": None, \"GoodForKids\": \"True\", \"GoodForMeal\": None, \"HairSpecializesIn\": None, \"HappyHour\": None, \"HasTV\": \"True\", \"Music\": None, \"NoiseLevel\": \"\"average\"\", \"Open24Hours\": None, \"OutdoorSeating\": \"False\", \"RestaurantsAttire\": \"\"casual\"\", \"RestaurantsCounterService\": None, \"RestaurantsDelivery\": \"True\", \"RestaurantsGoodForGroups\": \"False\", \"RestaurantsPriceRange2\": \"1\", \"RestaurantsReservations\": \"False\", \"RestaurantsTableService\": None, \"RestaurantsTakeOut\": \"True\", \"Smoking\": None, \"WheelchairAccessible\": None, \"WiFi\": \"\"no\"\"}",
          "categories": "Restaurants, Pizza",
          "hours": "{\"Friday\": \"11:0-23:30\", \"Monday\": \"11:0-22:30\", \"Saturday\": \"11:0-23:30\", \"Sunday\": \"12:0-22:0\", \"Thursday\": \"11:0-22:30\", \"Tuesday\": \"11:0-22:30\", \"Wednesday\": \"11:0-22:30\"}",
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
          "attributes": "{}",
          "categories": "Pizza, Restaurants",
          "hours": "{\"Friday\": \"11:0-0:0\", \"Monday\": \"11:0-23:0\", \"Saturday\": \"11:0-0:0\", \"Sunday\": \"12:0-23:0\", \"Thursday\": \"11:0-23:0\", \"Tuesday\": \"11:0-23:0\", \"Wednesday\": \"11:0-23:0\"}",
          "created_at": "2025-09-25T01:50:58.520808",
          "updated_at": "2025-09-25T01:50:58.522807"
        }
      ]
    },
    "query_processed": "If I want to have pizza, where do you recommend?",
    "reasoning_summary": "The user is asking for a pizza recommendation. I used the search_businesses tool to find businesses that serve pizza. I then used the get_business_info tool to get more information about the two businesses that were returned."
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