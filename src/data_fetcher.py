import os
import requests
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
import logging

# logger config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

class DataAPI:
    def __init__(self, url, name):
        self.url = url
        self.file_name = name
        self.save_dir = self.create_save_dir("data")

    @staticmethod
    def create_save_dir(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.info(f"Created folder: {folder_path}")
        return folder_path

    def get_data(self):
        """Download the data from the API"""
        logger.info(f"Downloading data from {self.url}")
        resp = requests.get(self.url, timeout=5)
        resp.raise_for_status()
        logger.info(f"Downloaded {len(resp.content)} bytes from {self.url}")
        return resp.text

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

        csv = ''
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
    def __init__(self, date_start, date_end):
        url = f"https://api.nbp.pl/api/exchangerates/rates/A/EUR/{date_start}/{date_end}/?format=xml"
        name = "nbp"
        super().__init__(url=url, name=name)

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
    def __init__(self, date_start, date_end):
        url = f"https://data-api.ecb.europa.eu/service/data/EXR/D.PLN.EUR.SP00.A?startPeriod={date_start}&endPeriod={date_end}&format=xml"
        name = "ecb"
        super().__init__(url=url, name=name)

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