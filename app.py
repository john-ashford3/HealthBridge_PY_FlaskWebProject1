from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient
from azure.eventgrid import EventGridPublisherClient, EventGridEvent
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
import os

app = Flask(__name__)

# Azure Blob Storage configuration
blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
container_name = 'medical-records'

# Event Grid configuration
eventgrid_client = EventGridPublisherClient(
    endpoint=os.getenv('EVENT_GRID_ENDPOINT'),
    credential=AzureKeyCredential(os.getenv('EVENT_GRID_KEY'))
)

# Search Client configuration
search_client = SearchClient(
    endpoint=os.getenv('SEARCH_ENDPOINT'),
    index_name='medical-records',
    credential=AzureKeyCredential(os.getenv('SEARCH_KEY'))
)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Upload file to Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
    blob_client.upload_blob(file)
    
    # Send event to Event Grid
    event = EventGridEvent(
        subject="NewFileUploaded",
        event_type="FileUpload",
        data={"filename": file.filename},
        data_version="1.0"
    )
    eventgrid_client.send([event])
    
    return jsonify({'success': 'File uploaded successfully'})

@app.route('/api/search', methods=['GET'])
def search_records():
    query = request.args.get('q', '')
    results = search_client.search(search_text=query, query_type=QueryType.SIMPLE)
    return jsonify([result for result in results])

if __name__ == '__main__':
    app.run(debug=True)