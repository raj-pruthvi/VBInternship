from pymongo import MongoClient
from urllib import parse
import datetime
x = str(datetime.datetime.now())
# print(x[:10])

# connect to mongodb cloud and return the collection
def mongoConnect():
    client = MongoClient("mongodb+srv://scarydonut:" + parse.quote("YM7ZWNU5@mlab") +
                         "@cluster0-o1llq.mongodb.net/test?retryWrites=true&w=majority")

    db = client.SpamFiles
    collection = db.spams
    # print(collection)
    return collection
