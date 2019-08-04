'''
This script shows the content of the database
'''


import pprint
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient


db = AsyncIOMotorClient('localhost', 27017).test


async def do_find():
    async for item in db.items.find({}):
        pprint.pprint(item)


loop = asyncio.get_event_loop()
loop.run_until_complete(do_find())
