import unittest
from unittest.mock import patch, MagicMock
from services.record_user import persist_user_info  
from data.models import User
from datetime import datetime

class Database_Should(unittest.TestCase):
    @patch('services.record_user.insert_query')
    def test_success_persist_user_info(self, mock_insert_query):
        
        mock_insert_query.return_value = 1
        
        test_user_info = User(
            id=None,  
            github_username="test",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=None,
            freshdesk_contact_id=None
        )
        user_id = persist_user_info(test_user_info)
        
        mock_insert_query.assert_called_once_with(
            (
                "INSERT INTO users (github_username, name, email, bio, location, created_at, is_recorded_fd, freshdesk_contact_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            ),
            (
                "test", 
                "Test User", 
                "test_user@example.com", 
                "Test bio", 
                "Test location", 
                None, 
                0,  
                None
            )
        )
        self.assertEqual(user_id, 1)

    @patch('services.record_user.insert_query')
    def test_persist_user_info_failure(self, mock_insert_query):
        
        mock_insert_query.side_effect = Exception("Database insertion error")
        
        test_user_info = User(
            id=None,  
            github_username="test",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=None,
            freshdesk_contact_id=None
        )
        
        with self.assertRaises(Exception) as context:
            persist_user_info(test_user_info)
        
        self.assertEqual(str(context.exception), "Failed to persist user info: Database insertion error")
        
if __name__ == '__main__':
    unittest.main()








    
    