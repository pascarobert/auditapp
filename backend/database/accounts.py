from pymongo import MongoClient
from bson.objectid import ObjectId

connection = MongoClient('localhost', 27017)

db = connection.Disertatie_Pasca_Robert
accounts = db.profiles

def get_account_by_id(id):
   objInstance = ObjectId(id)
   query = {'_id': objInstance}
   account = accounts.find_one(query)
   return account     

def get_account(value, attribute):
   query = {attribute: value}
   account = accounts.find_one(query)
   return account

def update_account(name, attribute, value):
   query = {"name": name} 
   data = {"$set": { attribute : value }}
   accounts.update_one(query, data)
          
def put_account(account):
   id = accounts.insert_one(account)
   if id.inserted_id:
      return id.inserted_id
   
def get_auditors():
   list = []
   auditors = accounts.find()
   for auditor in auditors:
      if auditor['type'] == 'auditor':
         list.append(auditor)
   return list

    
def delete_account(name):
   query = {"name": name}
   account = accounts.find_one(query)
   accounts.delete_one(account)
   

   

       
          
