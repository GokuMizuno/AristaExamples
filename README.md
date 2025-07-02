A quick demo for Nautobot plugin that interacts with AWS, Azure, and gcp secrets manager.

Please note, this is

A> Not completed
B> Not tested
C> Not in classes
D> Does not deal with authentication

Please note:
For AwS:
# AWS Boto3 automatically handles authentication via:
# 1. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
# 2. Shared credential file (~/.aws/credentials)
# 3. AWS config file (~/.aws/config)
# 4. IAM roles for EC2 instances or ECS tasks
# Ensure your AWS credentials are configured for the region you are targeting.


For Azure:
# Azure authentication typically uses DefaultAzureCredential, which attempts
# a series of authentication methods including:
# 1. Environment variables (AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)
# 2. Managed Identity (for Azure-hosted applications)
# 3. Azure CLI (if logged in via `az login`)
# 4. Visual Studio Code
# Ensure your Azure environment is authenticated and has appropriate permissions
# to the Key Vault (e.g., Secret Get, Set, Delete permissions).


For Google Cloud:
# It's highly recommended to set up GOOGLE_APPLICATION_CREDENTIALS
# environment variable pointing to your service account key file,
# or use Workload Identity/other GCP native authentication methods.

