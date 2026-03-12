# To check mangoDB connection

from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://PavanBanoth:Pavan99@cluster0.l1uibzj.mongodb.net/?appName=Cluster0"

# Create MongoClient with exact same ServerApi settings as Node.js
server_api = ServerApi('1', strict=True, deprecation_errors=True)
client = MongoClient(uri, server_api=server_api)

def run():
    try:
        # Connect and ping (same as Node.js client.connect() + ping)
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    finally:
        client.close()

run()

