## This script imports the tinytweets.json file into your mongo database
## It will work for any json file containing a single array of objects
## There's nothing specific to llamaindex going on here
## You can get your data into mongo any way you like.

json_file = 'tinytweets.json'

# Load environment variables from local .env file
from dotenv import load_dotenv
load_dotenv()

import os
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import json_util
from datetime import datetime
# Load the tweets from a local file
# with open(json_file, 'r') as f:
#     tweets = json.load(f)

# Create a new client and connect to the server
client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))
db = client[os.getenv("MONGODB_DATABASE")]
collection = db[os.getenv("MONGODB_COLLECTION")]

count = 0

# for doc in client.sample_supplies.sales.find().limit(10):
#     i = collection.insert_one(doc).inserted_id
#     print(i)

for doc in client.sample_supplies.sales.find().limit(10):
    sale_date = str(doc["saleDate"])
    store_location = doc["storeLocation"]
    items = list(doc["items"])
    products = ""
    for item in items:
        products += item["name"] + " with price of " + "$" + str(item["price"])  + " and quantity of " + str(item["quantity"]) + ", "
    customer_gender = "male" if doc["customer"]["gender"] == "M" else "female"
    customer_age = doc["customer"]["age"]
    customer_email = doc["customer"]["email"]
    customer_satisfaction = doc["customer"]["satisfaction"]
    purchase_method = doc["purchaseMethod"]
    temp = f"sale date is {sale_date}, store location is {store_location}, items are {products}, customer age is {customer_age}, customer email is {customer_email}, customer satisfaction number out of 10 is {customer_satisfaction}, purchase method is {purchase_method}"
    doc["text"] = temp
    inserted_id = collection.insert_one(doc).inserted_id
    if not inserted_id:
        print("Insertion Failed")
        break
    else:
        count += 1
print("number of files inserted: ", count)
    

# Insert the tweets into mongo
# for doc in client["sample_supplies"]["sales"]:
    # print(doc["storeLocation"])
# collection.insert_many(tweets)
