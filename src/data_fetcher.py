import os
import requests
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

class DataAPI:
    def __init__(self, url, name):
        self.url = url
        self.file_name = name
        self.save_dir = self.create_save_dir("data")

    @staticmethod
    def create_save_dir(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    def get_data(self):
        """Download the data from the API"""
        resp = requests.get(self.url, timeout=5)
        resp.raise_for_status()
        return resp.text

    def save_data(self, data):
        """Save the data to the file XML format"""
        file_path = os.path.join(self.save_dir, f"{self.file_name}.xml")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(data)
        print(f"Saved {file_path}")

    def merge_data(self, new_data):
        """Append the data to the file XML format"""
        file_path = os.path.join(self.save_dir, f"{self.file_name}.xml")

        tree = ET.parse(file_path)
        root = tree.getroot()

        existing_dates = {rate.find("Date").text for rate in root.findall("Rate")}

        new_root = ET.fromstring(new_data)

        for rate in new_root.findall("Rate"):
            date = rate.find("Date").text
            if date not in existing_dates:
                root.append(rate)

        # update file
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

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
        """Parse the data to simple XML format"""
        tree = ET.fromstring(data)
        results = []
        for rate in tree.findall(".//Rate"):
            date = rate.find("EffectiveDate").text
            value = float(rate.find("Mid").text)
            results.append(f"<Rate><Date>{date}</Date><Value>{value}</Value></Rate>")

        xml_parsed = "<Rates>\n" + "\n".join(results) + "\n</Rates>"
        return xml_parsed


class ECBDataAPI(DataAPI):
    def __init__(self, date_start, date_end):
        url = f"https://data-api.ecb.europa.eu/service/data/EXR/D.PLN.EUR.SP00.A?startPeriod={date_start}&endPeriod={date_end}&format=xml"
        name = "ecb"
        super().__init__(url=url, name=name)

    def parse_data(self, data):
        """Parse the data to simple XML format"""
        ns = {'gen': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic'}
        tree = ET.fromstring(data)
        results = []
        for obs in tree.findall(".//gen:Obs", ns):
            date = obs.find("gen:ObsDimension", ns).attrib['value']
            value = float(obs.find("gen:ObsValue", ns).attrib['value'])
            results.append(f"<Rate><Date>{date}</Date><Value>{value}</Value></Rate>")

        xml_parsed = "<Rates>\n" + "\n".join(results) + "\n</Rates>"
        return xml_parsed