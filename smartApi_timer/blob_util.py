from azure.storage.blob import BlobServiceClient
from datetime import datetime
import pytz
from .settings import Configuration as config


class BlobUtility:

    @staticmethod
    def get_blob_client(blob_name, container_name="logger"):
        blob_service_client = BlobServiceClient.from_connection_string(config.azure_storage_connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(f"{blob_name}.txt")
        is_blob_exist = blob_client.exists()
        if not is_blob_exist:
            blob_client.create_append_blob()
            blob_client.append_block("Date|Signal|Strength|Close|Change|OI|Vol|Rsi|{}".format("\n"))
        return blob_client

    @staticmethod
    def add_logging_to_azure_blob(message: str):
        date_now = datetime.now(pytz.timezone(config.time_zone)).strftime('%Y_%m_%d')
        blob_name = str(f"report_{date_now}")
        client = BlobUtility.get_blob_client(blob_name)
        client.append_block(message)
