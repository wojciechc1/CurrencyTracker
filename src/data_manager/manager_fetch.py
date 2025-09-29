from .data_manager import DataManager
import os
import xml.etree.ElementTree as ET
import csv
import logging
import glob

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)



class ManagerFetch(DataManager):
    def __init__(self, out_format):
        #.folder_path = folder_path
        self.out_format = out_format


    def get_data_formatted(self, data):
        if self.out_format == "CSV":
            formatted = self.get_csv(data)
        elif self.out_format == "XML":
            formatted = self.get_xml(data)
        else:
            formatted = data  # defalt format

        logger.info(f"Successfully converted.")
        return formatted