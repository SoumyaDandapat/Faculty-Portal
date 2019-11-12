import pymongo 

mongo_server="mongodb://localhost:27017/"


class nosql:

    def __init__(self):
        client = pymongo.MongoClient(mongo_server) 
        database=client["dbms"]
        self.pprofile=client["personal_profile"]        

    def get_data(self,input):
        ans=self.pprofile.find(input)
        result=[]
        for row in ans:
            result.append(row)
        return result
    
    def update_data(self,condition,new):
        new["$set"]=new
        self.pprofile.update_one(condition,new)
        return

    def delete_data(self, condition):
        self.pprofile.delete_one(condition)
        return

    def insert_data(self,input):
        self.pprofile.insert_one(input)
        return
        
    def clear_data(self):
        self.pprofile.delete_many({})    

