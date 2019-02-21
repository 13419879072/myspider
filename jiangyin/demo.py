import pymongo

client = pymongo.MongoClient("192.168.1.170", 27017)["test"]["test1"]

client.delete_one({'name':'张三'})

client.insert({'name':'张三','age':25})