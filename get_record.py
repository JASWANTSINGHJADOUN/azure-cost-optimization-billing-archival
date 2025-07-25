from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import json, os

def get_record(record_id, partition_key):
    cosmos = CosmosClient(os.environ['COSMOS_ENDPOINT'], os.environ['COSMOS_KEY'])
    container = cosmos.get_database_client('billing').get_container_client('records')

    try:
        return container.read_item(record_id, partition_key=partition_key)
    except:
        blob_service = BlobServiceClient.from_connection_string(os.environ['BLOB_CONN_STRING'])
        blob_client = blob_service.get_blob_client(container='archive', blob=f"{record_id}.json")
        blob_data = blob_client.download_blob().readall()
        return json.loads(blob_data)
