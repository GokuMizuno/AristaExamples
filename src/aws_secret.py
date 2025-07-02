import boto3
import requests
import json
from boto3 import SecretsManager
from botocore.exceptions import ClientError


class AWSSecrets():
    def __init__(self):
        pass
    # def create_aws_secret(*args, **kwargs) -> bool:
    #     # match kwargs via key, value in kwargs.item()
    #     # make the request
    #     try:
    #         response = client.create_secret(
    #         Name='string',
    #         ClientRequestToken='string',
    #         Description='string',
    #         KmsKeyId='string',
    #         SecretBinary=b'bytes',
    #         SecretString='string',
    #         Tags=[
    #             {
    #                 'Key': 'string',
    #                 'Value': 'string'
    #             },
    #         ],
    #         AddReplicaRegions=[
    #             {
    #                 'Region': 'string',
    #                 'KmsKeyId': 'string'
    #             },
    #         ],
    #         ForceOverwriteReplicaSecret=True|False
    #         )
    #     except Exception as e:
    #         print(f"Error creating secret for {project_id}: Exception {str(e)}")
    #         raise
    #     return True

    def add_aws_secret(self, secret_id: str, secret_value: str, region_name: str, description: str = "") -> str:
        """
        Creates a new secret in AWS Secrets Manager.

        Args:
            secret_id (str): The name for the new secret.
            secret_value (str): The value (payload) for the secret.
            region_name (str): The AWS region where the secret will be created.
            description (str, optional): A description for the secret. Defaults to "".

        Returns:
            str: The ARN of the created secret.

        Raises:
            ClientError: If there's an AWS-specific error (e.g., secret already exists, permissions issue).
            Exception: For other unexpected errors.
        """
        # check secret to make sure that the last seven characters are not -XXXXXX
        # AWS salts secrets with -XXXXXX
        if secret_value == "":
            print("Create secret failed, secret is blank")
            return False
        if len(secret_value > 6):
            last_seven = secret_value[-7:]
            if last_seven[0] == '-' and last_seven[1:].isalnum():
                print("Secrets string has an invalid last seven characters.")
                return False

        try:
            client = boto3.client("secretsmanager", region_name=region_name)
            response = client.create_secret(
                Name=secret_id,
                Description=description,
                SecretString=secret_value
            )
            print(f"Created secret: {response['ARN']}")
            return response["ARN"]

        except ClientError as e:
            print(f"AWS Client Error adding secret '{secret_id}': {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected Error adding secret '{secret_id}': {str(e)}")
            raise

    def get_aws_secret(self, secret_id: str, region_name: str) -> str:
        """
        Retrieves a secret from AWS Secrets Manager.

        Args:
            secret_id (str): The name or ARN of the secret to retrieve.
            region_name (str): The AWS region where the secret is stored (e.g., "us-east-1").

        Returns:
            str: The secret payload as a string.

        Raises:
            ClientError: If there's an AWS-specific error (e.g., secret not found, permissions issue).
            Exception: For other unexpected errors.
        """
        try:
            client = boto3.client("secretsmanager", region_name=region_name)
            get_secret_value_response = client.get_secret_value(SecretId=secret_id)

            # Decrypts secret using the associated KMS key.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if "SecretString" in get_secret_value_response:
                return get_secret_value_response["SecretString"]
            else:
                # For binary secrets, you might need to decode it differently based on its content type
                return get_secret_value_response["SecretBinary"].decode("utf-8")

        except ClientError as e:
            print(f"AWS Client Error retrieving secret '{secret_id}': {str(e)}")
            raise  # Re-raise the exception after printing
        except Exception as e:
            print(f"Unexpected Error retrieving secret '{secret_id}': {str(e)}")
            raise

    def update_aws_secret(self, secret_id: str, new_secret_value: str, region_name: str) -> str:
        """
        Updates an existing secret in AWS Secrets Manager by creating a new version.

        Args:
            secret_id (str): The name or ARN of the secret to update.
            new_secret_value (str): The new value (payload) for the secret.
            region_name (str): The AWS region where the secret is stored.

        Returns:
            str: The ARN of the updated secret.

        Raises:
            ClientError: If there's an AWS-specific error (e.g., secret not found, permissions issue).
            Exception: For other unexpected errors.
        """
        try:
            client = boto3.client("secretsmanager", region_name=region_name)
            response = client.put_secret_value(
                SecretId=secret_id,
                SecretString=new_secret_value
            )
            print(f"Updated secret '{secret_id}'. New version ID: {response['VersionId']}")
            return response["ARN"]

        except ClientError as e:
            print(f"AWS Client Error updating secret '{secret_id}': {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected Error updating secret '{secret_id}': {str(e)}")
            raise

    def delete_aws_secret(self, secret_id: str, region_name: str, recovery_window_in_days: int = 30) -> str:
        """
        Deletes a secret from AWS Secrets Manager.
        The secret is marked for deletion and cannot be recovered after the recovery window.

        Args:
            secret_id (str): The name or ARN of the secret to delete.
            region_name (str): The AWS region where the secret is stored.
            recovery_window_in_days (int, optional): The number of days to wait before
                                                    permanently deleting the secret.
                                                    Defaults to 30. Min 7, Max 30.

        Returns:
            str: The ARN of the deleted secret.

        Raises:
            ClientError: If there's an AWS-specific error (e.g., secret not found, permissions issue).
            Exception: For other unexpected errors.
        """
        try:
            client = boto3.client("secretsmanager", region_name=region_name)
            response = client.delete_secret(
                SecretId=secret_id,
                RecoveryWindowInDays=recovery_window_in_days
            )
            print(f"Secret '{secret_id}' marked for deletion. Deletion date: {response['DeletionDate']}")
            return response["ARN"]

        except ClientError as e:
            print(f"AWS Client Error deleting secret '{secret_id}': {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected Error deleting secret '{secret_id}': {str(e)}")
            raise
