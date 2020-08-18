from main import mongoConnect
from bson.objectid import ObjectId

collection = mongoConnect()

collection.delete_one({'_id': ObjectId("5dc2fd1a43a2e9c8c8603b91")})

getRes = collection.find_one({'_id': ObjectId("5dc295e780b3286d5ee8e1b2")})
setQuery = "spam" if getRes['result'] == "ham" else "ham" 
collection.update({'_id': ObjectId("5dc295e780b3286d5ee8e1b2") }, {'$set': {"result": setQuery}} )


res = collection.find()
for i in res:
    print (i)

