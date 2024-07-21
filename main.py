import sys
from routers.github_api import get_user_info_from_github
from routers.freshdesk_api import create_freshdesk_contact, update_freshdesk_contact
from services.record_user import persist_user_info
from services.update_user import update_user_recorded_status, update_user_full_info
from services.get_user import get_user_info_from_db


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <github_username> <freshdesk_subdomain>")
        sys.exit(1)

    github_username = sys.argv[1]
    freshdesk_subdomain = sys.argv[2]

    try:
        user_info = get_user_info_from_github(github_username)
        
        user_exists = get_user_info_from_db(user_info.github_username)
        
        if user_exists:
            user_id, is_recorded_fd, freshdesk_contact_id = user_exists[0]
            
            if is_recorded_fd:
                update_freshdesk_contact(user=user_info, domain=freshdesk_subdomain, contact_id=freshdesk_contact_id)
                update_user_full_info(id=user_id, user=user_info)
                print(f"Contact updated successfully.")
            else: 
                new_contact = create_freshdesk_contact(new_user=user_info, domain=freshdesk_subdomain)
                update_user_recorded_status(user_id, new_contact['id'])
                print(f"New freshdesk contact created successfully.")
        else:
            user_id = persist_user_info(user_info)
            print(f"New db user created successfully.")
            new_contact = create_freshdesk_contact(new_user=user_info, domain=freshdesk_subdomain)
            update_user_recorded_status(user_id, new_contact['id'])
            print(f"New freshdesk contact created successfully.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
