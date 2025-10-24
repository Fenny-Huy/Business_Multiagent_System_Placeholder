from tools.review_search_tool import ReviewSearchTool
import json

tool = ReviewSearchTool()
results = tool.search_reviews("great service", k=3, business_id="eEOYSgkmpB90uNA7lDOMRA")

print(f"Search Results: \n {json.dumps(results, indent=2)}")


input = '''
```json
{
  "note": "I found business information and reviews for Vietnamese Food Truck in Tampa Bay, FL. The business has a 4-star rating with 10 reviews. The reviews mention their Pho, Banh mi, and egg rolls.",
  "result": {
    "tool_outputs": {
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
              "text": "Vietnamese Food Truck was a super perfect dinner for me tonight! I saw they were in the nearby neighborhood today, & I immediately went online to order.Since it is a chilly winter night, I knew that Pho was perfect for me. I ordered the beef and meatball pho and it was a great amount of meat to noodle ratio. It was super tasty. I also ordered the bbq Pork banh mi",
              "stars": 5.0,
              "date": "2021-12-01T00:06:58",
              "score": 0.259336
            },
            {
              "text": "I really really wanted to like this place. They came to our Food Truck Friday. Let me pre-qualify myself on VN food...I've been to Saigon 12 times and have a spouse born there. The pho broth didn't have much flavor or aroma and the beef was sliced wayyyy too thick. The sandwich had Chinese-style BBQ pork and cucumbers. Didn't taste any pate. The roll was decent. Chicken wings were excellent....I really don't get the fries and ketchup, however. The chicken strips were clearly store bought",
              "stars": 3.0,
              "date": "2021-10-02T01:23:08",
              "score": 0.17431830000000004
            },
            {
              "text": "I have traveled to Vietnam several times, love the countries food. Nothing is more disappointing to me than going to a Vietnamese restaurant in the US snd order pho and it either has no flavor, to much grease, or the nasty after taste of msg. That is NOT the case here. The pho broth is so aromatic and many levels of flavor you want to drink the whole bowl. That's not all! The egg rolls are so crispy and flavorful, easily can tell they are hand made and fresh",
              "stars": 5.0,
              "date": "2022-01-03T01:18:29",
              "score": 0.05934876
            },
            {
              "text": "Food was great. I ordered one of everything. Best pho I've had since visiting Vietnam. Egg rolls and Banh mi were great too!",
              "stars": 5.0,
              "date": "2018-07-25T14:35:33",
              "score": -0.0018617000000000772
            },
            {
              "text": "Good tasted good - but I'm a bit confused as to how a Vietnamese Good trick serves Vietnamese egg rolls with a mayo-like sauce?? I love Vietnamese food, and have always had fish sauce as one of the condiments. The egg rolls on their own was ok, I even tried the mayo sauce - (not great). Next time - I'll stick with authentic Vietnamese restaurants. But to be fair, the food was standard . I'd actually try it again...if they had the right sauces, of course!",
              "stars": 3.0,
              "date": "2019-10-18T18:01:29",
              "score": -0.06393929999999992
            }
          ]
        }
      ]
    },
    "query_processed": "Can you find some information about a business called Vietnamese Food Truck and some of its reviews?",
    "reasoning_summary": "I first used get_business_id to find the business ID for \"Vietnamese Food Truck\". Then, I used get_business_info to get the business information. Finally, I used search_reviews to find reviews related to the business."
  }
}
```
'''