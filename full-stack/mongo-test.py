import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:8000/")
mydb = myclient["database"]
mycol = mydb["customers"]
mydict = { "name": "John", "address": "Highway 37" }
x = mycol.insert_one(mydict)
mylist = [
#   { "_id": 1, "name": "Amy", "address": "Apple st 652"},
#   { "_id": 2, "name": "Hannah", "address": "Mountain 21"},
#   { "_id": 3, "name": "Michael", "address": "Valley 345"},
  { "name": "Sandy", "address": "Ocean blvd 2"},
  { "name": "Betty", "address": "Green Grass 1"},
  { "name": "Richard", "address": "Sky st 331"},
  { "name": "Susan", "address": "One way 98"},
  { "name": "Vicky", "address": "Yellow Garden 2"},
  { "name": "Ben", "address": "Park Lane 38"},
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"}
]
y = mycol.insert_many(mylist)

print(myclient.list_database_names())
print(mydb.list_collection_names())
print(x.inserted_id)
print(y.inserted_ids)
for x in mycol.find({"address":"One way 298"}):
    print(x)
print("-----")
for x in mycol.find().sort("name", -1):
    print(x)
print((mycol.find()))

z = mycol.delete_many({})
# print(z.deleted_count, "deleted")