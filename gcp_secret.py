# import os
from google.cloud import secretmanager


def create_gcp_secret(project_id: str, secret_id: str, secret_value: str) -> str:
    """
    Creates a new secret in Google Cloud Secret Manager with an initial version

    Args:
        project_id (str): Your Google Cloud project ID.
        secret_id (str): The ID for the new secret.
        secret_value (str): The initial value (payload) for the secret.

    Returns:
        str: The full resource name of the created secret.

    Raises:
        Exception: If there's an error creating the secret.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()

        parent = f"projects/{project_id}"

        # Create the secret itself
        secret = client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        print(f"Created secret: {secret.name}")

        # Add the initial secret version
        version = client.add_secret_version(
            request={"parent": secret.name, "payload": {"data": secret_value.encode("UTF-8")}}
        )
        print(f"Added secret version: {version.name}")
        return secret.name

    except Exception as e:
        print(f"Error creating secret '{secret_id}' in project '{project_id}': {str(e)}")
        raise


def delete_gcp_secret(project_id: str, secret_id: str) -> None:
    """
    Deletes a secret from Google Cloud Secret Manager.
    Note: Deleting a secret marks it for destruction and it cannot be recovered
    after a certain period (default 30 days).

    Args:
        project_id (str): Your Google Cloud project ID.
        secret_id (str): The ID of the secret to delete.

    Raises:
        Exception: If there's an error deleting the secret.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret.
        name = f"projects/{project_id}/secrets/{secret_id}"

        # Delete the secret.
        client.delete_secret(request={"name": name})
        print(f"Deleted secret: {secret_id}")

    except Exception as e:
        print(f"Error deleting secret '{secret_id}' from project '{project_id}': {str(e)}")
        raise


def get_gcp_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Retrieves a secret from Google Cloud Secret Manager.

    Args:
        project_id (str): Your Google Cloud project ID.
        secret_id (str): The ID of the secret to retrieve.
        version_id (str): The version of the secret to retrieve (e.g., "latest" or a specific version number).
                            Defaults to "latest".

    Returns:
        str: The secret payload as a string.

    Raises:
        Exception: If there's an error retrieving the secret.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret version.
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        return payload

    except Exception as e:
        print(f"Error retrieving secret '{secret_id}' from project '{project_id}': {str(e)}")
        raise  # Re-raise the exception after printing


def update_gcp_secret(project_id: str, secret_id: str, new_secret_value: str) -> str:
    """
    Adds a new version to an existing secret in Google Cloud Secret Manager.
    In Secret Manager, updating a secret means adding a new version.

    Args:
        project_id (str): Your Google Cloud project ID.
        secret_id (str): The ID of the secret to update.
        new_secret_value (str): The new value (payload) for the secret.

    Returns:
        str: The full resource name of the newly created secret version.

    Raises:
        Exception: If there's an error adding a new secret version.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret.
        secret_name = f"projects/{project_id}/secrets/{secret_id}"

        # Add the new secret version
        version = client.add_secret_version(
            request={"parent": secret_name, "payload": {"data": new_secret_value.encode("UTF-8")}}
        )
        print(f"Added new secret version: {version.name}")
        return version.name

    except Exception as e:
        print(f"Error updating secret '{secret_id}' in project '{project_id}': {str(e)}")
        raise
