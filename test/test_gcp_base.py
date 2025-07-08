import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import os
import sys

# Assuming the provided code is in a file named 'google_base.py'
from google_base import GoogleBase


class TestGoogleBase(unittest.TestCase):
    def setUp(self):
        """Set up for test methods."""
        self.google_base = GoogleBase()
        self.mock_project_id = "test-project-123"
        self.mock_service_account_path = "/tmp/test-service-account.json"
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        """Clean up after test methods."""
        sys.stdout = sys.__stdout__  # Reset redirect

    @patch('os.path.exists')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_gcp_login_success_with_service_account(self, mock_from_service_account_file, mock_os_path_exists):
        """
        Test successful GCP login using a service account key path.
        """
        mock_os_path_exists.return_value = True
        mock_from_service_account_file.return_value = MagicMock()  # Simulate successful credential creation

        self.google_base.service_account_key_path = self.mock_service_account_path
        result = self.google_base.gcp_login(service_account_key_path=self.mock_service_account_path)

        self.assertTrue(result)
        mock_os_path_exists.assert_called_with(self.mock_service_account_path)
        mock_from_service_account_file.assert_called_with(
            self.mock_service_account_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        self.assertIn("Service account authentication successful!", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_gcp_login_service_account_file_not_found(self, mock_from_service_account_file, mock_os_path_exists):
        """
        Test GCP login when the service account key file does not exist.
        """
        mock_os_path_exists.return_value = False

        self.google_base.service_account_key_path = self.mock_service_account_path
        result = self.google_base.gcp_login(service_account_key_path=self.mock_service_account_path)

        self.assertFalse(result)
        mock_os_path_exists.assert_called_with(self.mock_service_account_path)
        mock_from_service_account_file.assert_not_called()  # Should not attempt to load credentials
        self.assertIn(f"Error: Service account key file not found at {self.mock_service_account_path}", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_gcp_login_service_account_creation_fails(self, mock_from_service_account_file, mock_os_path_exists):
        """
        Test GCP login when service account credential creation fails (e.g., returns None).
        """
        mock_os_path_exists.return_value = True
        mock_from_service_account_file.return_value = None  # Simulate failure to create credentials

        self.google_base.service_account_key_path = self.mock_service_account_path
        result = self.google_base.gcp_login(service_account_key_path=self.mock_service_account_path)

        self.assertFalse(result)
        mock_os_path_exists.assert_called_with(self.mock_service_account_path)
        mock_from_service_account_file.assert_called_with(
            self.mock_service_account_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        # No "Service account authentication successful!" message should be printed
        self.assertNotIn("Service account authentication successful!", self.captured_output.getvalue())

    @patch('os.path.exists')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file', side_effect=Exception("Test Exception"))
    def test_gcp_login_exception_handling(self, mock_from_service_account_file, mock_os_path_exists):
        """
        Test GCP login handles general exceptions during the authentication process.
        """
        mock_os_path_exists.return_value = True

        self.google_base.service_account_key_path = self.mock_service_account_path
        result = self.google_base.gcp_login(service_account_key_path=self.mock_service_account_path)

        self.assertFalse(result)
        mock_os_path_exists.assert_called_with(self.mock_service_account_path)
        mock_from_service_account_file.assert_called_with(
            self.mock_service_account_path,
            scopes=['httpsc://www.googleapis.com/auth/cloud-platform']
        )
        self.assertIn("Exception when logging in to gcp Test Exception", self.captured_output.getvalue())

    def test_gcp_login_no_service_account_path_set(self):
        """
        Test GCP login when no service account path is set on the instance,
        and no path is passed to the method.
        (Current implementation will return False immediately)
        """
        self.google_base.service_account_key_path = ""  # Ensure it's empty
        result = self.google_base.gcp_login()  # No service_account_key_path provided

        self.assertFalse(result)
        self.assertEqual("", self.captured_output.getvalue())  # No output expected from current logic

if __name__ == '__main__':
    unittest.main()
