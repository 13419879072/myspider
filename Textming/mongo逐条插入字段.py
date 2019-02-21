import pymongo
import time
from Textming import senti_python


senti_python.run('我喜欢你')
client = pymongo.MongoClient()['tests']['test']

lis = client.find()

for i in lis:
    print(i)
    print(type(i))
    if i['name'] == '老王':
        client.update_many({'name': {'$eq': i['name']}}, {'$set': {'chioce': 1}})
    elif i['name'] == '老李':
        client.update_many({'name': {'$eq': i['name']}}, {'$set': {'chioce': 0}})
    elif i['name'] == '老张':
        client.update_many({'name': {'$eq': i['name']}}, {'$set': {'chioce': -1}})
