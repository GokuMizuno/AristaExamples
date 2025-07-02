# AWS
# if __name__ == "__main__":
#     # IMPORTANT: Replace with your actual AWS Region and desired Secret ID
#     my_aws_region = "us-east-1" # e.g., "us-west-2", "eu-central-1"
#     test_aws_secret_id = "my-test-aws-secret-123"

#     print("\n--- Adding a new AWS secret ---")
#     try:
#         add_aws_secret(test_aws_secret_id, "initial-aws-secret-value-123", my_aws_region)
#         print("AWS Secret added successfully.")
#     except ClientError as e:
#         if e.response['Error']['Code'] == 'ResourceExistsException':
#             print(f"Secret '{test_aws_secret_id}' already exists. Skipping add.")
#         else:
#             print(f"Failed to add AWS secret: {str(e)}")
#     except Exception as e:
#         print(f"Failed to add AWS secret: {str(e)}")


#     print("\n--- Retrieving the AWS secret ---")
#     try:
#         retrieved_aws_secret = get_aws_secret(test_aws_secret_id, my_aws_region)
#         print(f"Retrieved AWS secret: {retrieved_aws_secret}")
#     except Exception as e:
#         print(f"Failed to retrieve AWS secret: {str(e)}")

#     print("\n--- Updating the AWS secret (adding a new version) ---")
#     try:
#         update_aws_secret(test_aws_secret_id, "updated-aws-secret-value-456", my_aws_region)
#         print("AWS Secret updated successfully (new version added).")
#     except Exception as e:
#         print(f"Failed to update AWS secret: {str(e)}")

#     print("\n--- Retrieving the updated AWS secret ---")
#     try:
#         retrieved_updated_aws_secret = get_aws_secret(test_aws_secret_id, my_aws_region)
#         print(f"Retrieved AWS secret (latest after update): {retrieved_updated_aws_secret}")
#     except Exception as e:
#         print(f"Failed to retrieve updated AWS secret: {str(e)}")

#     print("\n--- Deleting the AWS secret ---")
#     # BE CAREFUL: This will mark the secret for deletion!
#     # Uncomment the following lines ONLY if you are sure you want to delete the secret.
#     # try:
#     #     delete_aws_secret(test_aws_secret_id, my_aws_region)
#     #     print("AWS Secret deleted successfully.")
#     # except Exception as e:
#     #     print(f"Failed to delete AWS secret: {str(e)}")

#     # print("\n--- Attempting to retrieve deleted AWS secret (should fail after recovery window) ---")
#     # try:
#     #     get_aws_secret(test_aws_secret_id, my_aws_region)
#     # except Exception as e:
#     #     print(f"As expected, failed to retrieve deleted AWS secret: {str(e)}")


# Azure
# if __name__ == "__main__":
#     # IMPORTANT: Replace with your actual Azure Key Vault URL and desired Secret Name
#     # Example: "https://my-unique-keyvault-name.vault.azure.net"
#     my_key_vault_url = "https://<your-key-vault-name>.vault.azure.net"
#     test_azure_secret_name = "my-test-azure-secret-123"

#     print("\n--- Adding a new Azure secret ---")
#     try:
#         add_azure_secret(my_key_vault_url, test_azure_secret_name, "initial-azure-secret-value-789")
#         print("Azure Secret added successfully.")
#     except Exception as e:
#         print(f"Failed to add Azure secret: {str(e)}")

#     print("\n--- Retrieving the Azure secret ---")
#     try:
#         retrieved_azure_secret = get_azure_secret(my_key_vault_url, test_azure_secret_name)
#         print(f"Retrieved Azure secret: {retrieved_azure_secret}")
#     except Exception as e:
#         print(f"Failed to retrieve Azure secret: {str(e)}")

#     print("\n--- Updating the Azure secret (creating a new version) ---")
#     try:
#         update_azure_secret(my_key_vault_url, test_azure_secret_name, "updated-azure-secret-value-abc")
#         print("Azure Secret updated successfully (new version created).")
#     except Exception as e:
#         print(f"Failed to update Azure secret: {str(e)}")

#     print("\n--- Retrieving the updated Azure secret ---")
#     try:
#         retrieved_updated_azure_secret = get_azure_secret(my_key_vault_url, test_azure_secret_name)
#         print(f"Retrieved Azure secret (latest after update): {retrieved_updated_azure_secret}")
#     except Exception as e:
#         print(f"Failed to retrieve updated Azure secret: {str(e)}")

#     print("\n--- Deleting the Azure secret ---")
#     # BE CAREFUL: This will delete the secret! If soft-delete is enabled on your Key Vault,
#     # it will be moved to a soft-delete state. Otherwise, it's permanently deleted.
#     # Uncomment the following lines ONLY if you are sure you want to delete the secret.
#     # try:
#     #     delete_azure_secret(my_key_vault_url, test_azure_secret_name)
#     #     print("Azure Secret deleted successfully.")
#     # except Exception as e:
#     #     print(f"Failed to delete Azure secret: {str(e)}")

#     # print("\n--- Attempting to retrieve deleted Azure secret (should fail) ---")
#     # try:
#     #     get_azure_secret(my_key_vault_url, test_azure_secret_name)
#     # except Exception as e:
#     #     print(f"As expected, failed to retrieve deleted Azure secret: {str(e)}")

# GCP
# if __name__ == "__main__":
#     # IMPORTANT: Replace with your actual GCP Project ID
#     my_project_id = "your-gcp-project-id"
#     test_secret_id = "my-test-secret-123"

#     print("\n--- Adding a new secret ---")
#     try:
#         add_gcp_secret(my_project_id, test_secret_id, "initial-secret-value-123")
#         print("Secret added successfully.")
#     except Exception as e:
#         print(f"Failed to add secret: {str(e)}")

#     print("\n--- Retrieving the secret ---")
#     try:
#         retrieved_secret = get_gcp_secret(my_project_id, test_secret_id)
#         print(f"Retrieved secret (latest): {retrieved_secret}")
#     except Exception as e:
#         print(f"Failed to retrieve secret: {str(e)}")

#     print("\n--- Updating the secret (adding a new version) ---")
#     try:
#         update_gcp_secret(my_project_id, test_secret_id, "updated-secret-value-456")
#         print("Secret updated successfully (new version added).")
#     except Exception as e:
#         print(f"Failed to update secret: {str(e)}")

#     print("\n--- Retrieving the updated secret ---")
#     try:
#         retrieved_updated_secret = get_gcp_secret(my_project_id, test_secret_id)
#         print(f"Retrieved secret (latest after update): {retrieved_updated_secret}")
#     except Exception as e:
#         print(f"Failed to retrieve updated secret: {str(e)}")

#     print("\n--- Deleting the secret ---")
#     # BE CAREFUL: This will mark the secret for deletion!
#     # Uncomment the following lines ONLY if you are sure you want to delete the secret.
#     # try:
#     #     delete_gcp_secret(my_project_id, test_secret_id)
#     #     print("Secret deleted successfully.")
#     # except Exception as e:
#     #     print(f"Failed to delete secret: {str(e)}")

#     # print("\n--- Attempting to retrieve deleted secret (should fail) ---")
#     # try:
#     #     get_gcp_secret(my_project_id, test_secret_id)
#     # except Exception as e:
#     #     print(f"As expected, failed to retrieve deleted secret: {str(e)}")
