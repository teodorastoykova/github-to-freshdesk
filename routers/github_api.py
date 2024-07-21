import os
from github import Github
from dotenv import load_dotenv
from data.models import User

load_dotenv()

def get_user_info_from_github(github_username):
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        raise Exception("Github token is not set in the environment variables.")
    
    try:
        g = Github(github_token)
        user = g.get_user(github_username)
        
        new_user = User.from_query_result(
            id=None,  
            github_username=user.login,
            name=user.name,
            email=user.email,
            bio=user.bio,
            location=user.location,
            created_at=user.created_at,
            is_recorded_fd=False, 
            freshdesk_contact_id=None 
        )
        return new_user
    except Exception as e:
        error_message = f"Error fetching user info from GitHub: {e}"
        raise Exception(error_message) from e