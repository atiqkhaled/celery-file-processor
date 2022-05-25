from destination_handler.azure_storage_handler import AzureStorageHandler
from destination_handler.destination_enum import DestinationEnum
from destination_handler.local_storage_handler import LocalStorageHandler


class DestinationFactory:

    def create_destination(self, destination):
        if destination == DestinationEnum.AZURE.name:
            return AzureStorageHandler()
        elif destination == DestinationEnum.LOCAL.name:
            return LocalStorageHandler()
