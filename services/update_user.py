from data.database import update_query

def update_user_recorded_status(user_id, freshdesk_contact_id):
    update_sql = """
    UPDATE users
    SET is_recorded_fd = 1, freshdesk_contact_id = ?
    WHERE id = ?
    """
    update_params = (freshdesk_contact_id, user_id)
    update_query(update_sql, update_params)
    
def update_user_full_info(id, user):
    update_sql = """
    UPDATE users
    SET 
        name = ?, 
        email = ?, 
        bio = ?, 
        location = ? 
    WHERE id = ?
    """
    
    update_params = (
        user.name,
        user.email,
        user.bio,
        user.location,
        id
    )
    
    update_query(update_sql, update_params)