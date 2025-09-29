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



class DataManager:

    @staticmethod
    def get_csv(data):
        """Convert list of dicts to CSV string"""
        if not data:
            return ""

        headers = list(data[0].keys())
        csv_str = ",".join(headers) + "\n"

        for item in data:
            row = [str(item.get(h, "")) for h in headers]
            csv_str += ",".join(row) + "\n"

        return csv_str

    @staticmethod
    def get_xml(data):
        """Convert list of dicts to XML string """
        logger.info(f"Converting data to XML")

        if not data:
            return ""

        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<Rates>\n'

        for item in data:
            xml += '  <Rate>\n'
            for key, value in item.items():
                xml += f'    <{key}>{value}</{key}>\n'
            xml += '  </Rate>\n'

        xml += '</Rates>'
        return xml

    @staticmethod
    def save_to_file(data, path):
        # checking if path exists and if not then creating one
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            ans = input(f"Folder '{folder}' does not exist. Create? [y/N]: ").strip().lower()
            if ans == "y":
                os.makedirs(folder, exist_ok=True)
                logger.info(f"Created folder: {folder}")
            else:
                logger.warning("Saving to file cancelled by user.")
                return

        # saving data to the file
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
        logger.info(f"Saved to {path}")
