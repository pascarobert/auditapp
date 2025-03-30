from pymongo import MongoClient
from bson.objectid import ObjectId

connection = MongoClient('localhost', 27017)
db = connection.Disertatie_Pasca_Robert
tickets = db.tickets
     

def get_ticket(id):
   obj = ObjectId(id)
   query = {"_id": obj}
   account = tickets.find_one(query)
   return account

def update_ticket(id, attribute, value):
   objInstance = ObjectId(id)
   query = {"_id": objInstance} 
   data = {"$set": { attribute : value }}
   tickets.update_one(query, data)
          
def put_ticket(ticket):
   resp = tickets.insert_one(ticket)
   print(resp) 

def delete_ticket(id):
   objInstance = ObjectId(id)
   query = {"_id": objInstance}
   tickets.delete_one(query)

def get_tickets(id, type):
   list = []
   for data in tickets.find():
      ticket = get_ticket(data['_id'])
      if str(ticket[type]) == str(id):
         list.append(ticket)
   return list                                           
   


   

       
          
