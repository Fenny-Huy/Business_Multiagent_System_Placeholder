
import json

json_text = '''
    {
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


