"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def hello():
    """Renders a sample page."""
    return "Hello World!"

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)


import logging
import azure.functions as func
from azure.storage.blob import BlobClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Check if the request is a POST request
    if not req.method == 'POST':
        return func.HttpResponse(
             "This endpoint only accepts POST requests.",
             status_code=400
        )

    # Get the image file from the request
    file = req.files.get('image')

    # Upload the image to Azure Blob Storage
    blob_client = BlobClient.from_connection_string(
        "<your-connection-string>",
        "<your-container-name>",
        file.filename
    )
    blob_client.upload_blob(file.stream())

    # Return the URL of the uploaded image
    image_url = blob_client.url
    return func.HttpResponse(image_url, status_code=200)