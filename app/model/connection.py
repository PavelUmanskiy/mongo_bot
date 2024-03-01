import json

from motor.motor_asyncio import AsyncIOMotorClient

from config.constants import BASE_DIR

with open(BASE_DIR / 'app/config/config.json', 'r') as config:
    mongo_conf = json.load(config)['mongodb']
client = AsyncIOMotorClient(mongo_conf['uri'])
database = client[mongo_conf['db_name']]
collection = database[mongo_conf['collection_name']]
