input = """
{
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
          "attributes": "{"AcceptsInsurance": None, "AgesAllowed": None, "Alcohol": ""none"", "Ambience": "{"divey": False, "hipster": False, "casual": None, "touristy": False, "trendy": None, "intimate": False, "romantic": False, "classy": False, "upscale": False}", "BYOB": None, "BYOBCorkage": None, "BestNights": None, "BikeParking": "False", "BusinessAcceptsBitcoin": None, "BusinessAcceptsCreditCards": "True", "BusinessParking": "{"garage": False, "street": True, "validated": False, "lot": False, "valet": False}", "ByAppointmentOnly": None, "Caters": "True", "CoatCheck": None, "Corkage": None, "DietaryRestrictions": None, "DogsAllowed": None, "DriveThr": None, "GoodForDancing": None, "GoodForKids": "True", "GoodForMeal": None, "HairSpecializesIn": None, "HappyHour": None, "HasTV": "True", "Music": None, "NoiseLevel": ""average"", "Open24Hours": None, "OutdoorSeating": "False", "RestaurantsAttire": ""casual"", "RestaurantsCounterService": None, "RestaurantsDelivery": "True", "RestaurantsGoodForGroups": "False", "RestaurantsPriceRange2": "1", "RestaurantsReservations": "False", "RestaurantsTableService": None, "RestaurantsTakeOut": "True", "Smoking": None, "WheelchairAccessible": None, "WiFi": ""no""}",
          "categories": "Restaurants, Pizza",
          "hours": "{"Friday": "11:0-23:30", "Monday": "11:0-22:30", "Saturday": "11:0-23:30", "Sunday": "12:0-22:0", "Thursday": "11:0-22:30", "Tuesday": "11:0-22:30", "Wednesday": "11:0-22:30"}",
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
          "hours": "{"Friday": "11:0-0:0", "Monday": "11:0-23:0", "Saturday": "11:0-0:0", "Sunday": "12:0-23:0", "Thursday": "11:0-23:0", "Tuesday": "11:0-23:0", "Wednesday": "11:0-23:0"}",     
          "created_at": "2025-09-25T01:50:58.520808",
          "updated_at": "2025-09-25T01:50:58.522807"
        }
      ]
    },
    "query_processed": "If I want to have pizza, where do you recommend?",
    "reasoning_summary": "The user is asking for a pizza recommendation. I used the search_businesses tool to find businesses that serve pizza. I then used the get_business_info tool to get more information about the two businesses that were returned."
  }"""