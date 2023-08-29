import asyncio
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
MONGO_DB_URI="mongodb+srv://hevc:sucks@cluster0.mdnim6a.mongodb.net/?retryWrites=true&w=majority"
print("[INFO]: STARTING MONGO DB CLIENT")
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.aniwatch

votedb = db.votes

# vote

async def is_voted(id,user): 
    id = "a" + str(id)
    votes = await votedb.find_one({"id":id})
    if votes == None :
        return 0
    if user not in votes["users"]:
        return 0
    return 1

async def save_vote(id,user):
    id = "a" + str(id)
    data = await votedb.update_one({"id": id},{"$addToSet": {"users": user}},upsert=True)
    return
