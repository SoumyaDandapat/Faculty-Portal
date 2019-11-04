import pymongo 

database_name="personal_profile"
collection_name="personal_profile"
database=0
collection=0
client=0




def ini_global_vars():
	global database,collection,client
	client = pymongo.MongoClient("mongodb://localhost:27017/") 
	database=client[database_name]
	collection=client[collection_name]

def clear_database():
	delete_from_db({})

def ins_to_db(input):
	global database,collection,client
	if(database.collection_name.find({"uid":input["uid"]}).count()==0):		
		if "name" in input.keys() and "contact" in input.keys() and "qualification" in input.keys() and "uid" in input.keys():
			database.collection_name.insert_one(input)
		else:
			print("some mandatory information missing")
	else:
		print("Same uid already exists so database would be updated")
		upd_db(input)

def upd_db(input):
	global database,collection,client
	input_temp={}
	input_temp["$set"]=input
	database.collection_name.update_one({"uid":input["uid"]},input_temp)

def print_all_data():
	global database,collection,client
	ans=database.collection_name.find()
	for res in ans:
		print(res)

def delete_from_db(input):
	global database,collection,client
	database.collection_name.delete_many(input)
	
def external_listener(input):
	global client
	ini_global_vars()
	if input["mode"]=="insert":
		ins_to_db(input["data"])
	elif input["mode"]=="update":
		upd_db(input["data"])
	elif input["mode"]=="print":
		print_all_data()
	elif input["mode"]=="delete":
		delete_from_db(input["data"])
	else:
		print("invalid option")

	client.close()	
	

