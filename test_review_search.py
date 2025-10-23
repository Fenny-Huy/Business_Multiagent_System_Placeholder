from tools.review_search_tool import ReviewSearchTool
import json

tool = ReviewSearchTool()
results = tool.search_reviews("great service", k=3, business_id="eEOYSgkmpB90uNA7lDOMRA")

print(f"Search Results: \n {json.dumps(results, indent=2)}")


input = '''
```json
{
  "note": "I found business information and reviews for the Vietnamese Food Truck in Tampa Bay. The business has a 4.0-star rating with 10 reviews. The reviews mention the pho, chicken wings, and egg rolls.",
  "result": {
    "tool_outputs": {
      "get_business_id": [
        "eEOYSgkmpB90uNA7lDOMRA"
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
        }
      ],
      "search_reviews": [
        [
          {
            "text": ". Great food snd service, if they had a restaurant it would crush the others in Tampa Bay. Somebody give these folks some recognition for their pho!!",
            "stars": 5.0,
            "business_id": "eEOYSgkmpB90uNA7lDOMRA",
            "date": "2022-01-03T01:18:29",
            "score": -0.7078884999999999
          },
          {
            "text": ". So super simple and convenient. I'm super happy to have their leftovers tomorrow!! So so good.Thanks for coming out to the area! So nice not to go far and leave the neighborhood!",
            "stars": 5.0,
            "business_id": "eEOYSgkmpB90uNA7lDOMRA",
            "date": "2021-12-01T00:06:58",
            "score": -0.7772326
          },
          {
            "text": "Ordered the classic beef and meatball pho and it was delicious. I'm usually partial to the meatballs but THESE meatballs had so much flavor. Definitely keep an eye out for this truck. Also not over priced.",
            "stars": 4.0,
            "business_id": "eEOYSgkmpB90uNA7lDOMRA",
            "date": "2019-01-16T18:22:34",
            "score": -0.811483
          },
          {
            "text": "Ordered the chicken wings. They were hot, fresh, and super crispy. Drenched in a honey sauce, that surprisingly, tasted good on the fries that came with the wings. Fantastic!",
            "stars": 4.0,
            "business_id": "eEOYSgkmpB90uNA7lDOMRA",
            "date": "2019-03-29T19:09:43",
            "score": -0.8494377
          },
          {
            "text": ". The chicken strips were clearly store bought. Egg rolls were better than most, but they put turkey inside....that is clearly a first. They were doing booming business, so all good.",
            "stars": 3.0,
            "business_id": "eEOYSgkmpB90uNA7lDOMRA",
            "date": "2021-10-02T01:23:08",
            "score": -0.8513417999999999
          }
        ]
      ]
    },
    "query_processed": "can you tell me some information about a business called Vietnamese Food Truck and some of its reviews? There is only one business called Vietnamese Food Truck so do not give or suggest others with similar names",
    "reasoning_summary": "I first identified the business_id for \"Vietnamese Food Truck\". Then, I used the business_id to retrieve business information and reviews. I have provided the business information and the top 5 reviews."
  }
}
```'''