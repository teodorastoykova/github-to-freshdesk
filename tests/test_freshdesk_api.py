import unittest
from unittest.mock import patch, MagicMock
from routers.freshdesk_api import create_freshdesk_contact, update_freshdesk_contact  
from data.models import User

class FreshdeskAPI_Should(unittest.TestCase):
    
    @patch('routers.freshdesk_api.requests.post')
    @patch('routers.freshdesk_api.os.getenv')
    def test_missing_freshdesk_credentials(self, mock_getenv, mock_post):

        mock_getenv.side_effect = lambda key: {
            'FRESHDESK_TOKEN': None,
            'FRESHDESK_PASSWORD': None
        }[key]

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
        
        domain = 'example'

        with self.assertRaises(Exception) as context:
            create_freshdesk_contact(test_user_info, domain)
        
        self.assertEqual(str(context.exception), "Freshdesk credentials are not set in the environment variables.")
        mock_post.assert_not_called()
    
    @patch('routers.freshdesk_api.requests.post')
    @patch('routers.freshdesk_api.os.getenv')
    def test_success_create_freshdesk_contact(self, mock_getenv, mock_post):
        
        mock_getenv.side_effect = lambda key: {
            'FRESHDESK_TOKEN': 'test_token',
            'FRESHDESK_PASSWORD': 'test_password'
        }[key]

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.headers = {'Location': '/contacts/432'}
        mock_response.json.return_value = {
            "id": 432,
            "name": "New User",
            "email": "new_user@example.com",
            "description": "New bio",  
            "address": "New location" 
        }
        mock_post.return_value = mock_response

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
        
        test_domain = "yourdomain"

        expected_response = {
            "id": 432,
            "name": "New User",
            "email": "new_user@example.com",
            "description": "New bio",  
            "address": "New location"
        }
        
        actual_response = create_freshdesk_contact(test_user_info, test_domain)
        
        self.assertEqual(actual_response, expected_response)

    @patch('routers.freshdesk_api.requests.post')
    @patch('routers.freshdesk_api.os.getenv')
    def test_failure_create_freshdesk_contact(self, mock_getenv, mock_post):
        
        mock_getenv.side_effect = lambda key: {
            'FRESHDESK_TOKEN': 'test_token',
            'FRESHDESK_PASSWORD': 'test_password'
        }[key]
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = 'Invalid request'
        
        mock_post.return_value = mock_response
        
        test_user = User(
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
        domain = "yourdomain"

        with self.assertRaises(Exception) as context:
            create_freshdesk_contact(test_user, domain)
        
        self.assertIn("Failed to create contact.", str(context.exception))
        self.assertIn("Status Code: 400", str(context.exception))
        self.assertIn("Response: Invalid request", str(context.exception))
        
        
    
    @patch('routers.freshdesk_api.requests.put')
    @patch('routers.freshdesk_api.os.getenv')
    def test_missing_freshdesk_credentials_update(self, mock_getenv, mock_put):
        
        mock_getenv.side_effect = lambda key: {
            'FRESHDESK_TOKEN': None,
            'FRESHDESK_PASSWORD': None
        }[key]

        user = {
            "name": "Test User",
            "email": "test_user@example.com",
            "bio": "Test bio",
            "location": "Test location"
        }
        domain = 'example'
        contact_id = '432'

        with self.assertRaises(Exception) as context:
            update_freshdesk_contact(user, domain, contact_id)
        
        self.assertEqual(str(context.exception), "Freshdesk credentials are not set in the environment variables.")
        mock_put.assert_not_called()
        
    @patch('routers.freshdesk_api.requests.put')
    @patch('routers.freshdesk_api.os.getenv')
    def test_successful_contact_update(self, mock_getenv, mock_put):
        
        mock_getenv.side_effect = lambda key: {
            'FRESHDESK_TOKEN': 'test_token',
            'FRESHDESK_PASSWORD': 'test_password'
        }[key]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 432, "name": "Updated User", "email": "updated_user@example.com","bio": "Updated bio", "location": "Updated location"}
        mock_put.return_value = mock_response

        test_user = User(
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
        domain = 'example'
        contact_id = '432'

        expected_response = {"id": 432, "name": "Updated User", "email": "updated_user@example.com","bio": "Updated bio", "location": "Updated location"}
        actual_response = update_freshdesk_contact(test_user, domain, contact_id)
        
        self.assertEqual(actual_response, expected_response)
    
    @patch('routers.freshdesk_api.requests.put')
    @patch('routers.freshdesk_api.os.getenv')
    def test_failed_contact_update(self, mock_getenv, mock_put):

        mock_getenv.side_effect = lambda key: {
            'FRESHDESK_TOKEN': 'test_token',
            'FRESHDESK_PASSWORD': 'test_password'
        }[key]

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = 'Bad Request'
        mock_put.return_value = mock_response

        test_user = User(
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
        domain = 'example'
        contact_id = '432'

        with self.assertRaises(Exception) as context:
            update_freshdesk_contact(test_user, domain, contact_id)
        
        self.assertEqual(str(context.exception), "Failed to update the contact. Status Code: 400, Response: Bad Request")

if __name__ == '__main__':
    unittest.main()
