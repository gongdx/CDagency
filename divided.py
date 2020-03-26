from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['CDagency']

unified_col = db['unified'].find()

for item in unified_col:
    coll_name = item['col_name']
    db[coll_name].update({'title': item['title']}, {'$set': dict(item)}, True, True)