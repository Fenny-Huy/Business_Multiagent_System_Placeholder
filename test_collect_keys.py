
import json

json_text = '''
{
      "get_business_id": [
        "eEOYSgkmpB90uNA7lDOMRA"
      ],
      "get_business_info": [
        {
          "eEOYSgkmpB90uNA7lDOMRA": {
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
          }
        }
      ],
      "search_reviews": [
        {
          "eEOYSgkmpB90uNA7lDOMRA": [
            {
              "text": ". Great food snd service, if they had a restaurant it would crush the others in Tampa Bay. Somebody give these folks some recognition for their pho!!",
              "stars": 5.0,
              "date": "2022-01-03T01:18:29",
              "score": -0.7078884999999999
            },
            {
              "text": ". So super simple and convenient. I'm super happy to have their leftovers tomorrow!! So so good.Thanks for coming out to the area! So nice not to go far and leave the neighborhood!",
              "stars": 5.0,
              "date": "2021-12-01T00:06:58",
              "score": -0.7772326
            },
            {
              "text": "Ordered the classic beef and meatball pho and it was delicious. I'm usually partial to the meatballs but THESE meatballs had so much flavor. Definitely keep an eye out for this truck. Also not over priced.",
              "stars": 4.0,
              "date": "2019-01-16T18:22:34",
              "score": -0.811483
            },
            {
              "text": "Ordered the chicken wings. They were hot, fresh, and super crispy. Drenched in a honey sauce, that surprisingly, tasted good on the fries that came with the wings. Fantastic!",
              "stars": 4.0,
              "date": "2019-03-29T19:09:43",
              "score": -0.8494377
            },
            {
              "text": ". The chicken strips were clearly store bought. Egg rolls were better than most, but they put turkey inside....that is clearly a first. They were doing booming business, so all good.",
              "stars": 3.0,
              "date": "2021-10-02T01:23:08",
              "score": -0.8513417999999999
            }
          ]
        }
      ]
    }
'''


# data = json.loads(json_text)

# def collect_keys(obj, path='', keys=None, paths=None):
#     if keys is None:
#         keys = set()
#     if paths is None:
#         paths = set()
#     if isinstance(obj, dict):
#         for k, v in obj.items():
#             keys.add(k)
#             new_path = f"{path}.{k}" if path else k
#             paths.add(new_path)
#             collect_keys(v, new_path, keys, paths)
#     elif isinstance(obj, list):
#         for i, item in enumerate(obj):
#             collect_keys(item, f"{path}[{i}]", keys, paths)
#     return keys, paths

# keys, paths = collect_keys(data)

# # Sort lists for stable output
# sorted_keys = sorted(keys)
# sorted_paths = sorted(paths)

# print(f"Found {len(sorted_keys)} unique key names.\n")
# print("Unique key names:")
# for k in sorted_keys:
#     print(" -", k)

# print("\n---\nFound {0} full paths (showing first 120 paths if many):\n".format(len(sorted_paths)))
# for p in sorted_paths[:120]:
#     print(" -", p)

# # Also provide example usage as functions for reuse
# def get_all_keys(json_obj):
#     """Return a sorted list of unique key names found anywhere in the JSON structure."""
#     ks, _ = collect_keys(json_obj)
#     return sorted(ks)

# def get_all_paths(json_obj):
#     """Return a sorted list of full key paths (dot + index notation)."""
#     _, ps = collect_keys(json_obj)
#     return sorted(ps)

# # expose results for potential further programmatic use
# result = {
#     "unique_keys": get_all_keys(data),
#     "full_paths": get_all_paths(data)
# }

# result


def get_root_keys(json_text):
    """Return the root field keys of a JSON string."""
    data = json.loads(json_text)
    if isinstance(data, dict):
        return list(data.keys())
    else:
        return []

root_keys = get_root_keys(json_text)
print("Root field keys:", root_keys)    

def get_field_content(json_text, field_key):
  """Return the value/content of a root field key from a JSON string."""
  data = json.loads(json_text)
  if isinstance(data, dict):
    return data.get(field_key)
  else:
    return None


business_content = get_field_content(json_text, "get_business_info")
print("\nContent for root key 'get_business_info':\n", json.dumps(business_content, indent=2))




# Utility: get the first dict from a list value for a root key, removing the outer array if present
def get_field_content_unwrapped(json_text, field_key):
  """Return the first dict (or value) from a root field key, unwrapping a single-item list if present."""
  data = json.loads(json_text)
  if isinstance(data, dict):
    value = data.get(field_key)
    if isinstance(value, list) and len(value) == 1 and isinstance(value[0], dict):
      return value[0]
    else:
      return value
  else:
    return None

# Example usage:
business_content_unwrapped = get_field_content_unwrapped(json_text, "get_business_info")
print("\nUnwrapped content for root key 'get_business_info':\n", json.dumps(business_content_unwrapped, indent=2))

get_name = next(iter(get_field_content_unwrapped(json_text, "get_business_info").values()))["name"]
print ("\nBusiness name extracted:", get_name)
# get_name = get_field_content(get_field_content_unwrapped(json_text, "get_business_info"), "eEOYSgkmpB90uNA7lDOMRA")


# Tools for analysis agent 

def extract_tool_results(json_text, tool_keys=("get_business_info", "search_reviews")):
  """Extract the values for specified tool keys from the root of the JSON."""
  data = json.loads(json_text)
  results = {}
  for key in tool_keys:
    value = data.get(key)
    if isinstance(value, list) and len(value) == 1 and isinstance(value[0], dict):
      results[key] = value[0]
    else:
      results[key] = value
  return results

def get_business_ids(business_info_dict):
  """Return a list of business ids from the unwrapped get_business_info dict."""
  if isinstance(business_info_dict, dict):
    return list(business_info_dict.keys())
  return []

def get_business_value(business_info_dict, business_id, field):
  """Return the value for a specific field of a business id."""
  if isinstance(business_info_dict, dict):
    info = business_info_dict.get(business_id)
    if isinstance(info, dict):
      return info.get(field)
  return None




# Example workflow

# Step 1: Extract tool results
tool_results = extract_tool_results(json_text)
get_business_info_result = tool_results["get_business_info"]
search_reviews_result = tool_results["search_reviews"]

# Step 2: Get business ids
business_ids = get_business_ids(get_business_info_result)
print("\nBusiness IDs in get_business_info:", business_ids)

# Step 3: Get a specific field value for a business id
if business_ids:
  first_id = business_ids[0]
  business_name = get_business_value(get_business_info_result, first_id, "name")
  print(f"Business name for {first_id}: {business_name}")

# Step 4: (Optional) Get all available fields for a business id
if business_ids:
  first_id = business_ids[0]
  fields = list(get_business_info_result[first_id].keys())
  print(f"All fields for {first_id}: {fields}")

