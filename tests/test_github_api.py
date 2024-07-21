import unittest
from unittest.mock import patch, MagicMock
from routers.github_api import get_user_info_from_github
from data.models import User
from datetime import datetime

class GitHubAPI_Should(unittest.TestCase):
    
    @patch('os.getenv')
    def test_github_token_not_set(self, mock_getenv):
        mock_getenv.return_value = None
        
        with self.assertRaises(Exception) as context:
            get_user_info_from_github('test_username')
        
        self.assertTrue('Github token is not set in the environment variables.' in str(context.exception))
    
    
    @patch('routers.github_api.Github')  
    def test_success_get_user_info_from_github(self, MockGithub):
        mock_user = MagicMock()
        mock_user.login = "Test"
        mock_user.name = "Test User"
        mock_user.email = "test_email@example.com"
        mock_user.bio = "Test bio"
        mock_user.location = "Test location"
        mock_user.created_at = datetime.strptime("2021-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")  
        mock_github_instance = MockGithub.return_value
        mock_github_instance.get_user.return_value = mock_user
        
        expected_user = User(
            id=None,
            github_username="Test",
            name="Test User",
            email="test_email@example.com",
            bio="Test bio",
            location="Test location",
            created_at=datetime.strptime("2021-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            is_recorded_fd=False,
            freshdesk_contact_id=None
        )
        
       
        test_github_username = "Test"
        actual_user_info = get_user_info_from_github(test_github_username)
        
        self.assertEqual(actual_user_info, expected_user)
        
        mock_github_instance.get_user.assert_called_once_with(test_github_username)



    @patch('routers.github_api.Github')  
    def test_failure_get_user_info_from_github(self, MockGithub):
       
        mock_github_instance = MockGithub.return_value
        mock_github_instance.get_user.side_effect = Exception("Error fetching user info")
        test_github_username = "Test User"
        
        with self.assertRaises(Exception) as context:
            get_user_info_from_github(test_github_username)
        
        self.assertEqual(str(context.exception), "Error fetching user info from GitHub: Error fetching user info")
        mock_github_instance.get_user.assert_called_once_with(test_github_username)

    
if __name__ == '__main__':
    unittest.main()
