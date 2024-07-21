from data.database import insert_query
          
def persist_user_info(user_info):
    sql = (
        "INSERT INTO users (github_username, name, email, bio, location, created_at, is_recorded_fd, freshdesk_contact_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    )
    params = (
        user_info.github_username,
        user_info.name, 
        user_info.email, 
        user_info.bio, 
        user_info.location, 
        user_info.created_at,
        0,  
        None
    )
    try:
        user_id = insert_query(sql, params)
        return user_id
    except Exception as e:
        raise Exception(f"Failed to persist user info: {e}")

 