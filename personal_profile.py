from pymongo import MongoClient 

# global variables must be declared here only

database_name="personal_profile"
collection_name="personal_profile"
database=0
collection=0

client = MongoClient("mongodb://localhost:27017/") 

def ini_global_vars():
	global database,collection
	database=client[database_name]
	collection=client[collection_name]

def ins_to_db(input):
	ini_global_vars()
	if(database.collection_name.find({'uid':input['uid']}).count()==0):		
		if 'name' in input.keys() and 'contact' in input.keys() and 'qualification' in input.keys() and 'uid' in input.keys():
			database.collection_name.insert_one(input)
	else:
		print("Same uid already exists or some mandatory information missing")

def upd_db(input):
	
