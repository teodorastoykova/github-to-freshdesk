import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
    
def create_freshdesk_contact(new_user, domain):
    freshdesk_token = os.getenv('FRESHDESK_TOKEN')
    freshdesk_password =  os.getenv('FRESHDESK_PASSWORD')
    
    if not freshdesk_token or not freshdesk_password:
        raise Exception("Freshdesk credentials are not set in the environment variables.")

    contact_info = {
            "name": new_user.name,
            "email": new_user.email,
            "description": new_user.bio,    
            "address": new_user.location
        }
    headers = { "Content-Type" : "application/json" }
    
    try:
        response  = requests.post("https://"+ domain +".freshdesk.com/api/v2/contacts", auth = (freshdesk_token, freshdesk_password), data = json.dumps(contact_info), headers = headers)
        
        if response.status_code == 201:
                return response.json()
        else:
                error_message = (
                f"Failed to create contact. "
                f"Status Code: {response.status_code}, "
                f"Response: {response.text}"
            )
                raise Exception(error_message)
   
    except Exception as e:
                 raise Exception(f"{str(e)}") from e
             
             
def update_freshdesk_contact(user, domain, contact_id):
    freshdesk_token = os.getenv('FRESHDESK_TOKEN')
    freshdesk_password =  os.getenv('FRESHDESK_PASSWORD')
    contact_id_str = str(contact_id)
    if not freshdesk_token or not freshdesk_password:
        raise Exception("Freshdesk credentials are not set in the environment variables.")

    contact_info = {
            "name": user.name,
            "email": user.email,
            "description": user.bio,    
            "address": user.location
        }
    headers = { "Content-Type" : "application/json" }
    
    try: 
        response = requests.put("https://"+ domain +".freshdesk.com/api/v2/contacts/"+contact_id_str, auth = (freshdesk_token, freshdesk_password), data = json.dumps(contact_info), headers = headers)

        if response.status_code == 200:
            return response.json()
        else:
            error_message = (
                f"Failed to update the contact. "
                f"Status Code: {response.status_code}, "
                f"Response: {response.text}"
            )
            raise Exception(error_message)
    
    except Exception as e:
                 raise Exception(f"{str(e)}") from e
        