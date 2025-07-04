import google.cloud
import os
# from google.cloud import storage
from google.oauth2 import service_account
# from google.auth.transport.requests import Request
# from google.auth.exceptions import DefaultCredentialsError
# import google.auth


class GoogleBase():
    def __init__(self):
        self.userName = ""
        self.pwd = ""
        self.service_account_key_path = ""
        self.GOOGLE_APPLICATION_CREDENTIALS = {}

    def getVMList(self, *args) -> list:
        """
        This gets all the VMs associated with a given GCP account

        Args:
            unk (unk)

        Returns:
            unk (unk)

        Raises:
            Exception if something goes wrong
        """
        # We use the gcp specific endpoints to get all VMs and statuses
        pass

    def gcp_login(self, project_id: str = None, service_account_key_path: str = None):
        """
        Authenticates with Google Cloud Platform and demonstrates access to a service.
        Application Default Credentials  automatically finds credentials in your environment
        (e.g., gcloud login, service account attached to a VM, GOOGLE_APPLICATION_CREDENTIALS environment variable).

        Args:
            project_id (str, optional): Your Google Cloud project ID. If not provided,
                                        it will try to infer it from the environment.
            service_account_key_path (str, optional): Path to your service account JSON key file.
                                                    If provided, this method will be used.

        Returns:
            bool: True if authentication was successful and a service could be accessed,
                False otherwise.
        """
        try:
            if self.service_account_key_path:
                # Method 1: Authenticate using a Service Account Key File
                print(f"Attempting to authenticate using service account key: {self.service_account_key_path}")
                if not os.path.exists(self.service_account_key_path):
                    print(f"Error: Service account key file not found at {self.service_account_key_path}")
                    return False

                credentials = service_account.Credentials.from_service_account_file(
                    service_account_key_path,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                if credentials:
                    return True
                print("Service account authentication successful!")
        except Exception as e:
            print(f"Exception when logging in to gcp {str(e)}")
        return False
