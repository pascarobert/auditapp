import backend.database.tickets as tickets
import backend.database.accounts as accounts
from datetime import date
from bson.objectid import ObjectId

def get_auditor_fullname(id):
    auditor = accounts.get_account_by_id(id)
    if auditor:
        return auditor['fullname']
    else:
        return 'missing'

def get_auditor_mail(id):
    auditor = accounts.get_account_by_id(id)
    if auditor:
        return auditor['email']
    else:
        return 'missing'

def get_auditor_name(id):
    auditor = accounts.get_account_by_id(id)
    if auditor:
        return auditor['fullname']
    else:
        return 'missing'    

def update_ticket_state(id, status):
    tickets.update_ticket(id,'status', status)

def delete_ticket(id):
    tickets.delete_ticket(id)

def get_auditors():
    auditors_list = accounts.get_auditors()
    return auditors_list

def push_minutes(name, client, hours, independante, auditor, BM):
    ticket = {"name":name, "client":client, "hours":hours, "independante":independante,  "auditor":auditor, "procedure":'minutes', "BM":BM, "date":str(date.today()), 'status':'New'}
    tickets.put_ticket(ticket) 
    return True 

def push_custom(name, client, hours, independante, auditor, custom):
    ticket = {"name":name, "client":client, "hours":hours, "independante":independante,  "auditor":auditor, "procedure":'custom', "custom":custom, "date":str(date.today()), 'status':'New'}
    tickets.put_ticket(ticket) 
    return True 

def push_cash(name, client, hours, independante, auditor, financial_statement, portofolio, materiality, bank_confirmation, fx ):
    ticket = {"name":name, "client":client, "hours":hours, "independante":independante,  "auditor":auditor, "procedure":'cash', "financial_statement":financial_statement, "portofolio":portofolio, "materiality":materiality, "bank_confirmation":bank_confirmation, "fx":fx, "date":str(date.today()), 'status':'New'}
    tickets.put_ticket(ticket) 
    return True 

def push_depositary(name, client, hours, independante, auditor, financial_statement, portofolio, materiality, bank_confirmation,):
    ticket = {"name":name, "client":client, "hours":hours, "independante":independante,  "auditor":auditor, "procedure":'depositary', "financial_statement":financial_statement, "portofolio":portofolio, "materiality":materiality, "bank_confirmation":bank_confirmation, "date":str(date.today()), 'status':'New'}
    tickets.put_ticket(ticket) 
    return True 

def push_fs(name, client, hours, independante, auditor, financial_statement):
    ticket = {"name":name, "client":client, "hours":hours, "independante":independante,  "auditor":auditor, "procedure":'fs', "financial_statement":financial_statement, "date":str(date.today()), 'status':'New'}
    tickets.put_ticket(ticket) 
    return True 

def push_kcw(name, client, hours, independante, auditor, engagement_letter, san ):
    ticket = {"name":name, "client":client, "hours":hours, "independante":independante,  "auditor":auditor, "procedure":'kcw', "engagement_letter":engagement_letter, "san":san, "date":str(date.today()), 'status':'New'}
    tickets.put_ticket(ticket) 
    return True

def push_leads(name, client, hours, independante, auditor, financial_statement, portofolio, materiality, bank_confirmation, fx, mapping):
    ticket = {"name":name, "client":client, "hours":hours, "independante":independante,  "auditor":auditor, "procedure":'leads', "financial_statement":financial_statement, "portofolio":portofolio, "materiality":materiality, "bank_confirmation":bank_confirmation, "fx":fx, "mapping":mapping, "date":str(date.today()), 'status':'New'}
    tickets.put_ticket(ticket) 
    return True 

def push_sr(name, client, hours, independante, auditor, financial_statement, prospectus, materiality):
    ticket = {"name":name, "client":client, "hours":hours, "independante":independante,  "auditor":auditor, "procedure":'sr', "financial_statement":financial_statement, "prospectus":prospectus, "materiality":materiality, "date":str(date.today()), 'status':'New'}
    tickets.put_ticket(ticket) 
    return True 

def push_swaps(name, client, hours, independante, auditor, financial_statement, portofolio, materiality, bank_confirmation):
    ticket = {"name":name, "client":client, "hours":hours, "independante":independante,  "auditor":auditor, "procedure":'swaps', "financial_statement":financial_statement, "portofolio":portofolio, "materiality":materiality, "bank_confirmation":bank_confirmation, "date":str(date.today()), 'status':'New'}
    tickets.put_ticket(ticket) 
    return True

def is_client(value, attribute):
    profile = accounts.get_account(value, attribute)
    if profile['type'] == 'client':
        return True 
    else: 
        return False
    
def sign_user(username, password):
    profile = accounts.get_account(username,'username')
    if profile: 
        if profile['password'] == password:
            return profile


def create_user(username, password, email, fullname):
    id = accounts.put_account({"fullname": fullname, "email": email, "username": username, "password":password, "type": 'client'})
    return id

def retrive_tickets(id, type):
    ticket_list = tickets.get_tickets(id, type)
    if ticket_list: 
        return ticket_list
    else: 
        return []

