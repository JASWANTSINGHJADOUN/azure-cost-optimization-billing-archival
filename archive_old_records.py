from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
from datetime import datetime, timedelta
import json
import os

COSMOS_ENDPOINT = os.environ['COSMOS_ENDPOINT']
COSMOS_KEY = os.environ['COSMOS_KEY']
DATABASE_NAME = 'billing'
CONTAINER_NAME = 'records'

BLOB_CONN_STRING = os.environ['BLOB_CONN_STRING']
BLOB_CONTAINER = 'archive'

def archive_old_records():
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    db = client.get_database_client(DATABASE_NAME)
    container = db.get_container_client(CONTAINER_NAME)

    blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STRING)
    blob_container = blob_service.get_container_client(BLOB_CONTAINER)

    cutoff = datetime.utcnow() - timedelta(days=90)
    query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff.isoformat()}'"

    for record in container.query_items(query, enable_cross_partition_query=True):
        blob_name = f"{record['id']}.json"
        blob_container.upload_blob(blob_name, json.dumps(record), overwrite=True)
        container.delete_item(record, partition_key=record['partitionKey'])
