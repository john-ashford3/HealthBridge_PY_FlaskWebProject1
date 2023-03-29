from flask import Flask, render_template, request
import os
import uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceExistsError

app = Flask(__name__)

# Get the Azure Blob Storage connection string from the Azure Key Vault
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://your-key-vault-name.vault.azure.net/", credential=credential)
connection_string = secret_client.get_secret(name="blob-connection-string").value

# Initialize the Azure Blob Storage client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get the Azure Blob Storage container client
container_name = "your-container-name"
container_client = blob_service_client.get_container_client(container_name)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['image']
        # Generate a unique ID for the file
        file_id = str(uuid.uuid4())
        # Save the file to Azure Blob Storage
        try:
            # Create a blob client and upload the file
            blob_client = container_client.get_blob_client(f"{file_id}_{file.filename}")
            blob_client.upload_blob(file, overwrite=True)
            # Get the URL of the uploaded file
            file_url = blob_client.url
            # Return the URL of the uploaded file
            return render_template('index.html', result=file_url)
        except ResourceExistsError:
            return render_template('index.html', error='File already exists.')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)