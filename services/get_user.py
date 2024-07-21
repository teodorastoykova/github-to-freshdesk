from data.database import read_query

def get_user_info_from_db(github_username):
    sql = "SELECT id, is_recorded_fd, freshdesk_contact_id FROM users WHERE github_username = ?"
    params = (github_username,)
    result = read_query(sql, params)
    return result
