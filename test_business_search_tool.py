from tools.business_search_tool import BusinessSearchTool
import os
import dotenv

dotenv.load_dotenv()

chroma_host = os.getenv("CHROMA_HOST", "localhost")

business_search_tool = BusinessSearchTool(host=chroma_host)

# fuzzy_search = business_search_tool.fuzzy_search(query="Vietnamese Food Truck")
# print(f"Fuzzy search result: {fuzzy_search}")

# get_business_id = business_search_tool.get_business_id("Vietnamese Food Truck")
# print(f"Get business ID result: {get_business_id}")

# search_business = business_search_tool.search_businesses("Vietnamese", k=3)
# print(f"Search business result: {search_business}")

get_business_info = business_search_tool.get_business_info(business_id="eEOYSgkmpB90uNA7lDOMRA")
print(f"Get business info result: {get_business_info}")