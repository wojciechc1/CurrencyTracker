import os
import requests
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
import logging
from data_manager.manager_fetch import ManagerFetch

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
        self.data_manager = ManagerFetch(out_format)


    def get_data_formatted(self, data):
        return self.data_manager.get_data_formatted(data)

    def save_to_file(self, data, path):
        self.data_manager.save_to_file(data, path)


    def get_data(self):
        """Download the data from the API"""
        logger.info(f"Downloading data from {self.url}")
        resp = requests.get(self.url, timeout=5)
        resp.raise_for_status()
        logger.info(f"Downloaded {len(resp.content)} bytes from {self.url}")
        return resp.text


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