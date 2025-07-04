from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError


def get_azure_secret(key_vault_url: str, secret_name: str) -> str:
    """
    Retrieves a secret from Azure Key Vault.

    Args:
        key_vault_url (str): The URL of your Azure Key Vault (e.g., "https://my-key-vault.vault.azure.net").
        secret_name (str): The name of the secret to retrieve.

    Returns:
        str: The secret value as a string.

    Raises:
        ResourceNotFoundError: If the secret is not found.
        HttpResponseError: For other Azure service errors.
        Exception: For unexpected errors.
    """
    try:
        # Create a SecretClient using DefaultAzureCredential
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)

        # Get the secret
        retrieved_secret = client.get_secret(secret_name)
        print(f"Successfully retrieved secret '{secret_name}'.")
        return retrieved_secret.value

    except ResourceNotFoundError:
        print(f"Error: Secret '{secret_name}' not found in Key Vault '{key_vault_url}'.")
        raise
    except HttpResponseError as e:
        print(f"Azure HTTP Error retrieving secret '{secret_name}': {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected Error retrieving secret '{secret_name}': {str(e)}")
        raise


def add_azure_secret(key_vault_url: str, secret_name: str, secret_value: str) -> str:
    """
    Creates a new secret in Azure Key Vault. If a secret with the same name already exists,
    it will create a new version of that secret.

    Args:
        key_vault_url (str): The URL of your Azure Key Vault.
        secret_name (str): The name for the new secret.
        secret_value (str): The value for the secret.

    Returns:
        str: The ID of the created or updated secret version.

    Raises:
        HttpResponseError: For Azure service errors.
        Exception: For unexpected errors.
    """
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)

        # Set the secret. If it exists, it creates a new version.
        set_secret = client.set_secret(secret_name, secret_value)
        print(f"Secret '{secret_name}' created/updated. Version ID: {set_secret.id}")
        return set_secret.id

    except HttpResponseError as e:
        print(f"Azure HTTP Error adding secret '{secret_name}': {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected Error adding secret '{secret_name}': {str(e)}")
        raise


def update_azure_secret(key_vault_url: str, secret_name: str, new_secret_value: str) -> str:
    """
    Updates an existing secret in Azure Key Vault by creating a new version.
    This is effectively the same operation as 'add_azure_secret' for existing secrets.

    Args:
        key_vault_url (str): The URL of your Azure Key Vault.
        secret_name (str): The name of the secret to update.
        new_secret_value (str): The new value for the secret.

    Returns:
        str: The ID of the newly created secret version.

    Raises:
        HttpResponseError: For Azure service errors.
        Exception: For unexpected errors.
    """
    # In Azure Key Vault, updating a secret is done by setting a new value,
    # which automatically creates a new version.
    return add_azure_secret(key_vault_url, secret_name, new_secret_value)


def delete_azure_secret(key_vault_url: str, secret_name: str) -> None:
    """
    Deletes a secret from Azure Key Vault.
    The secret is moved to a soft-delete state (if soft-delete is enabled on the Key Vault)
    and can be recovered within a retention period.

    Args:
        key_vault_url (str): The URL of your Azure Key Vault.
        secret_name (str): The name of the secret to delete.

    Raises:
        ResourceNotFoundError: If the secret is not found.
        HttpResponseError: For other Azure service errors.
        Exception: For unexpected errors.
    """
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)

        # Begin deleting the secret. This returns a poller.
        # If soft-delete is enabled, the secret will be in a "deleted" state
        # and can be recovered. Otherwise, it's permanently deleted.
        poller = client.begin_delete_secret(secret_name)
        deleted_secret = poller.wait()  # Wait for the deletion operation to complete

        if deleted_secret:
            print(f"Secret '{secret_name}' deleted (or marked for deletion).")
            # If soft-delete is enabled, deleted_secret.id will contain the ID of the deleted secret.

    except ResourceNotFoundError:
        print(f"Error: Secret '{secret_name}' not found for deletion in Key Vault '{key_vault_url}'.")
        raise
    except HttpResponseError as e:
        print(f"Azure HTTP Error deleting secret '{secret_name}': {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected Error deleting secret '{secret_name}': {str(e)}")
        raise
