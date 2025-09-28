import os
import requests
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
import logging

# logger config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

class DataAPI:
    def __init__(self, url, out_format):
        self.url = url
        self.out_format = out_format

    #@staticmethod
    def save_to_file(self, path, data):
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


    def get_data(self):
        """Download the data from the API"""
        logger.info(f"Downloading data from {self.url}")
        resp = requests.get(self.url, timeout=5)
        resp.raise_for_status()
        logger.info(f"Downloaded {len(resp.content)} bytes from {self.url}")
        return resp.text

    def get_data_formatted(self, data):
        if self.out_format == "CSV":
            formatted = self.get_csv(data)
        elif self.out_format == "XML":
            formatted = self.get_xml(data)
        else:
            formatted = data # defalt format

        logger.info(f"Successfully converted.")
        return formatted

    @staticmethod
    def get_xml(data):
        """Convert the data to XML"""
        logger.info(f"Converting data to XML")

        xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xml += '<Rates>'
        for item in data:
            date = item.get("Date", "")
            value = str(item.get("Value", ""))
            xml += f"<Rate><Date>{date}</Date>"
            xml += f"<Value>{value}</Value></Rate>"
        xml += f'</Rates>'
        return xml

    @staticmethod
    def get_csv(data):
        """Convert the data to CSV"""
        logger.info(f"Converting data to CSV")

        csv = 'date,value\n'
        for item in data:
            date = item.get("Date", "")
            value = str(item.get("Value", ""))
            csv += f"{date},{value}\n"

        return csv

    @abstractmethod
    def parse_data(self, data):
        """To overwrite"""
        raise NotImplementedError


class NBPDataAPI(DataAPI):
    def __init__(self, date_start, date_end, out_format):
        url = f"https://api.nbp.pl/api/exchangerates/rates/A/EUR/{date_start}/{date_end}/?format=xml"
        super().__init__(url=url, out_format=out_format)

    def parse_data(self, data):
        """Parse the data to list of dictionaries"""
        tree = ET.fromstring(data)
        results = []
        for rate in tree.findall(".//Rate"):
            date = rate.find("EffectiveDate").text
            value = float(rate.find("Mid").text)
            results.append({'Date': date, 'Value': value})

        return results


class ECBDataAPI(DataAPI):
    def __init__(self, date_start, date_end, out_format):
        url = f"https://data-api.ecb.europa.eu/service/data/EXR/D.PLN.EUR.SP00.A?startPeriod={date_start}&endPeriod={date_end}&format=xml"
        super().__init__(url=url, out_format=out_format)

    def parse_data(self, data):
        """Parse the data to list of dictionaries"""
        ns = {'gen': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic'}
        tree = ET.fromstring(data)
        results = []
        for obs in tree.findall(".//gen:Obs", ns):
            date = obs.find("gen:ObsDimension", ns).attrib['value']
            value = float(obs.find("gen:ObsValue", ns).attrib['value'])
            results.append({'Date': date, 'Value': value})

        return results