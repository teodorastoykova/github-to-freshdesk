import unittest
from unittest.mock import patch, MagicMock
import sys
import io
from main import main
from services.get_user import get_user_info_from_db
from services.record_user import  persist_user_info
from services.update_user import update_user_recorded_status
from data.models import User
from datetime import datetime
from routers.github_api import get_user_info_from_github
from routers.freshdesk_api import create_freshdesk_contact, update_freshdesk_contact

class Main_Should(unittest.TestCase):
    
    def test_main_invalid_args(self):
        with self.assertRaises(SystemExit):
            main()
    
    @patch('main.get_user_info_from_github')
    @patch('sys.argv', ['main.py', 'test_github_user', 'test_subdomain'])
    def test_main_github_failure(self, mock_get_user_info_from_github):
        mock_get_user_info_from_github.side_effect = Exception("GitHub API Error")

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit):
                main()
            printed_output = mock_stdout.getvalue()
            self.assertIn("Error: GitHub API Error", printed_output)

    @patch('main.get_user_info_from_github')
    @patch('main.get_user_info_from_db')
    @patch('sys.argv', ['main.py', 'test_github_user', 'test_subdomain'])
    def test_main_db_failure(self, mock_get_user_info_from_github, mock_get_user_info_from_db):
        
        test_user_info = User(
            id=None,
            github_username="new_github_user",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=False,
            freshdesk_contact_id=None
        )
        
        mock_get_user_info_from_github.return_value = test_user_info
        
        mock_get_user_info_from_db.side_effect = Exception("Database Error")

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit):
                main()
            printed_output = mock_stdout.getvalue()
            self.assertIn("Error: Database Error", printed_output)
           
    @patch('sys.argv', ['main.py', 'new_github_user', 'freshdesk_subdomain'])
    @patch('main.get_user_info_from_github')
    @patch('main.get_user_info_from_db')
    @patch('main.create_freshdesk_contact')
    @patch('main.update_user_recorded_status')
    @patch('main.persist_user_info')
    def test_main_user_creation(self, mock_persist_user_info, mock_update_user_recorded_status, mock_create_freshdesk_contact, mock_get_user_info_from_db, mock_get_user_info_from_github):
        
        test_user_info = User(
            id=None,
            github_username="new_github_user",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=False,
            freshdesk_contact_id=None
        )

        mock_get_user_info_from_github.return_value = test_user_info
        mock_get_user_info_from_db.return_value = None
        mock_persist_user_info.return_value = 1  
        mock_create_freshdesk_contact.return_value = {'id': 432}
        
        
        with patch('builtins.print') as mock_print:
            main()


        mock_get_user_info_from_github.assert_called_once_with('new_github_user')
        mock_get_user_info_from_db.assert_called_once_with('new_github_user')
        mock_persist_user_info.assert_called_once_with(test_user_info)
        mock_create_freshdesk_contact.assert_called_once_with(
            new_user=test_user_info,
            domain='freshdesk_subdomain'
        )
        mock_update_user_recorded_status.assert_called_once_with(1, 432)
        mock_print.assert_any_call('New db user created successfully.')
        mock_print.assert_any_call('New freshdesk contact created successfully.')

    @patch('sys.argv', ['main.py', 'new_github_user', 'freshdesk_subdomain'])
    @patch('main.get_user_info_from_github')
    @patch('main.get_user_info_from_db')
    @patch('main.create_freshdesk_contact')
    @patch('main.update_user_recorded_status')
    @patch('main.persist_user_info')
    def test_main_user_creation_db_error(self, mock_persist_user_info, mock_update_user_recorded_status, mock_create_freshdesk_contact, mock_get_user_info_from_db, mock_get_user_info_from_github):
 
        test_user_info = User(
            id=None,
            github_username="new_github_user",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=False,
            freshdesk_contact_id=None
        )
        
        mock_get_user_info_from_github.return_value = test_user_info
        mock_get_user_info_from_db.return_value = None
        mock_persist_user_info.side_effect = Exception("Database error")
        
        
        with patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit) as cm:
                main()

    
        self.assertEqual(cm.exception.code, 1)
        
        mock_get_user_info_from_github.assert_called_once_with('new_github_user')
        mock_get_user_info_from_db.assert_called_once_with('new_github_user')
        mock_persist_user_info.assert_called_once_with(test_user_info)
    
        mock_create_freshdesk_contact.assert_not_called()
        mock_update_user_recorded_status.assert_not_called()
    
        mock_print.assert_any_call('Error: Database error')
        
    @patch('sys.argv', ['main.py', 'new_github_user', 'freshdesk_subdomain'])
    @patch('main.get_user_info_from_github')
    @patch('main.get_user_info_from_db')
    @patch('main.create_freshdesk_contact')
    @patch('main.update_user_recorded_status')
    @patch('main.persist_user_info')
    def test_main_user_creation_create_freshdesk_contact_error(self, mock_persist_user_info, mock_update_user_recorded_status, mock_create_freshdesk_contact, mock_get_user_info_from_db, mock_get_user_info_from_github):

        test_user_info = User(
            id=None,
            github_username="new_github_user",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=False,
            freshdesk_contact_id=None
        )
        mock_get_user_info_from_github.return_value = test_user_info
        mock_get_user_info_from_db.return_value = None
        mock_persist_user_info.return_value = 1
        mock_create_freshdesk_contact.side_effect = Exception("Freshdesk API error")
        

        with patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit) as cm:
                main()

            
        self.assertEqual(cm.exception.code, 1)
        mock_get_user_info_from_github.assert_called_once_with('new_github_user')
        mock_get_user_info_from_db.assert_called_once_with('new_github_user')
        mock_persist_user_info.assert_called_once_with(test_user_info)
        mock_create_freshdesk_contact.assert_called_once_with(
                new_user=test_user_info,
                domain='freshdesk_subdomain'
            )
        mock_update_user_recorded_status.assert_not_called()
        mock_print.assert_any_call('Error: Freshdesk API error')
    
    @patch('sys.argv', ['main.py', 'new_github_user', 'freshdesk_subdomain'])
    @patch('main.get_user_info_from_github')
    @patch('main.get_user_info_from_db')
    @patch('main.create_freshdesk_contact')
    @patch('main.update_user_recorded_status')
    @patch('main.persist_user_info')
    def test_main_user_creation_update_status_error(self, mock_persist_user_info, mock_update_user_recorded_status, mock_create_freshdesk_contact, mock_get_user_info_from_db, mock_get_user_info_from_github):
        
        test_user_info = User(
            id=None,
            github_username="new_github_user",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=False,
            freshdesk_contact_id=None
        ) 
        mock_get_user_info_from_github.return_value = test_user_info
        mock_get_user_info_from_db.return_value = None
        mock_persist_user_info.return_value = 1  
        mock_create_freshdesk_contact.return_value = {'id': 432}

        mock_update_user_recorded_status.side_effect = Exception("Database update error")
        
        with patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit) as cm:
                main()

            
        self.assertEqual(cm.exception.code, 1)
        
        mock_get_user_info_from_github.assert_called_once_with('new_github_user')
        mock_get_user_info_from_db.assert_called_once_with('new_github_user')
        mock_persist_user_info.assert_called_once_with(test_user_info)
        mock_create_freshdesk_contact.assert_called_once_with(
                new_user=test_user_info,
                domain='freshdesk_subdomain'
            )
        mock_update_user_recorded_status.assert_called_once_with(1, 432)
        mock_print.assert_any_call('Error: Database update error')
    
    @patch('sys.argv', ['main.py', 'existing_github_user', 'freshdesk_subdomain'])
    @patch('main.get_user_info_from_github')
    @patch('main.get_user_info_from_db')
    @patch('main.update_freshdesk_contact')
    def test_main_existing_user_updated(self, mock_update_freshdesk_contact, mock_get_user_info_from_db, mock_get_user_info_from_github):
        
        test_user_info = User(
            id=None,
            github_username="existing_github_user",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=False,
            freshdesk_contact_id=None
        )
         
        mock_get_user_info_from_github.return_value = test_user_info
        mock_get_user_info_from_db.return_value = [(1, True, 432)]  
        

        with patch('builtins.print') as mock_print:
            main()


        mock_get_user_info_from_github.assert_called_once_with('existing_github_user')
        mock_get_user_info_from_db.assert_called_once_with('existing_github_user')
        mock_update_freshdesk_contact.assert_called_once_with(
                user=test_user_info,
                domain='freshdesk_subdomain',
                contact_id=432
            )

        mock_print.assert_any_call('Contact updated successfully.')

    @patch('sys.argv', ['main.py', 'existing_github_user', 'freshdesk_subdomain'])
    @patch('main.get_user_info_from_github')
    @patch('main.get_user_info_from_db')
    @patch('main.update_freshdesk_contact')
    @patch('main.update_user_full_info')
    def test_main_existing_user_update_freshdesk_contact_error(self, mock_update_user_full_info, mock_update_freshdesk_contact, mock_get_user_info_from_db, mock_get_user_info_from_github):
       
        test_user_info = User(
            id=None,
            github_username="existing_github_user",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=False,
            freshdesk_contact_id=None
        )
        
        mock_get_user_info_from_github.return_value = test_user_info
        mock_get_user_info_from_db.return_value = [(1, True, 432)]  
        mock_update_freshdesk_contact.side_effect = Exception("Freshdesk API error")
        
        with patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit) as cm:
                main()

        self.assertEqual(cm.exception.code, 1)
        
        mock_get_user_info_from_github.assert_called_once_with('existing_github_user')
        mock_get_user_info_from_db.assert_called_once_with('existing_github_user')
        mock_update_freshdesk_contact.assert_called_once_with(
            user=test_user_info,
            domain='freshdesk_subdomain',
            contact_id=432
        )
        mock_update_user_full_info.assert_not_called()

        mock_print.assert_any_call('Error: Freshdesk API error')


    @patch('sys.argv', ['main.py', 'existing_github_user', 'freshdesk_subdomain'])
    @patch('main.get_user_info_from_github')
    @patch('main.get_user_info_from_db')
    @patch('main.update_freshdesk_contact')
    @patch('main.update_user_full_info')
    def test_main_existing_user_update_user_error(self, mock_update_user_full_info, mock_update_freshdesk_contact, mock_get_user_info_from_db, mock_get_user_info_from_github):
        
        test_user_info = User(
            id=None,
            github_username="existing_github_user",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=False,
            freshdesk_contact_id=None
        )
        
        mock_get_user_info_from_github.return_value = test_user_info
        mock_get_user_info_from_db.return_value = [(1, True, 432)]  
        mock_update_freshdesk_contact.return_value = None
        mock_update_user_full_info.side_effect = Exception("Update user info error")
        
        with patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit) as cm:
                main()

        self.assertEqual(cm.exception.code, 1)
        
        mock_get_user_info_from_github.assert_called_once_with('existing_github_user')
        mock_get_user_info_from_db.assert_called_once_with('existing_github_user')
        mock_update_freshdesk_contact.assert_called_once_with(
            user=test_user_info,
            domain='freshdesk_subdomain',
            contact_id=432
        )
        
        mock_update_user_full_info.assert_called_once_with(id=1, user=test_user_info)
        mock_print.assert_any_call('Error: Update user info error')
        
        
    @patch('sys.argv', ['main.py', 'existing_github_user_not_recorded', 'freshdesk_subdomain'])
    @patch('main.get_user_info_from_github')
    @patch('main.get_user_info_from_db')
    @patch('main.create_freshdesk_contact')
    @patch('main.update_user_recorded_status')
    def test_main_existing_user_not_recorded(self, mock_update_user_recorded_status, mock_create_freshdesk_contact, mock_get_user_info_from_db, mock_get_user_info_from_github):
       
        test_user_info = User(
            id=None,
            github_username="existing_github_user_not_recorded",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=False,
            freshdesk_contact_id=None
        )
        
        mock_get_user_info_from_github.return_value = test_user_info
        mock_get_user_info_from_db.return_value = [(1, False, None)]  
        mock_create_freshdesk_contact.return_value = {'id': 432}
        
        with patch('builtins.print') as mock_print:
            main()

        mock_get_user_info_from_github.assert_called_once_with('existing_github_user_not_recorded')
        mock_get_user_info_from_db.assert_called_once_with('existing_github_user_not_recorded')
        mock_create_freshdesk_contact.assert_called_once_with(
                new_user=test_user_info,
                domain='freshdesk_subdomain'
            )
        mock_update_user_recorded_status.assert_called_once_with(1, 432)
        mock_print.assert_any_call('New freshdesk contact created successfully.')

    @patch('sys.argv', ['main.py', 'existing_github_user_not_recorded', 'freshdesk_subdomain'])
    @patch('main.get_user_info_from_github')
    @patch('main.get_user_info_from_db')
    @patch('main.create_freshdesk_contact')
    @patch('main.update_user_recorded_status')
    def test_main_existing_user_not_recorded_create_contact_error(self, mock_update_user_recorded_status, mock_create_freshdesk_contact, mock_get_user_info_from_db, mock_get_user_info_from_github):
       
        test_user_info = User(
            id=None,
            github_username="existing_github_user_not_recorded",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=False,
            freshdesk_contact_id=None
        )
        
        mock_get_user_info_from_github.return_value = test_user_info
        mock_get_user_info_from_db.return_value = [(1, False, None)]  
        
        mock_create_freshdesk_contact.side_effect = Exception("Freshdesk API error")
        
        with patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit) as cm:
                main()

        self.assertEqual(cm.exception.code, 1)
        
        mock_get_user_info_from_github.assert_called_once_with('existing_github_user_not_recorded')
        mock_get_user_info_from_db.assert_called_once_with('existing_github_user_not_recorded')
        mock_create_freshdesk_contact.assert_called_once_with(
            new_user=test_user_info,
            domain='freshdesk_subdomain'
        )
        
        mock_update_user_recorded_status.assert_not_called()
        
        mock_print.assert_any_call('Error: Freshdesk API error')

    @patch('sys.argv', ['main.py', 'existing_github_user_not_recorded', 'freshdesk_subdomain'])
    @patch('main.get_user_info_from_github')
    @patch('main.get_user_info_from_db')
    @patch('main.create_freshdesk_contact')
    @patch('main.update_user_recorded_status')
    def test_update_user_recorded_status_error(self, mock_update_user_recorded_status, mock_create_freshdesk_contact, mock_get_user_info_from_db, mock_get_user_info_from_github):

        test_user_info = User(
            id=None,  
            github_username="existing_github_user_not_recorded",
            name="Test User",
            email="test_user@example.com",
            bio="Test bio",
            location="Test location",
            created_at=None,
            is_recorded_fd=None,
            freshdesk_contact_id=None
        )

        mock_get_user_info_from_github.return_value = test_user_info
        mock_get_user_info_from_db.return_value = [(1, False, None)]  
        mock_create_freshdesk_contact.return_value = {'id': 432}
        mock_update_user_recorded_status.side_effect = Exception("Database update error")
        
        with patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit) as cm:
                main()

            
        self.assertEqual(cm.exception.code, 1)
        
        mock_get_user_info_from_github.assert_called_once_with('existing_github_user_not_recorded')
        mock_get_user_info_from_db.assert_called_once_with('existing_github_user_not_recorded')
        mock_create_freshdesk_contact.assert_called_once_with(
            new_user=test_user_info,
            domain='freshdesk_subdomain'
        )
        mock_update_user_recorded_status.assert_called_once_with(1, 432)
        
        mock_print.assert_any_call('Error: Database update error')
        
if __name__ == '__main__':
    unittest.main()