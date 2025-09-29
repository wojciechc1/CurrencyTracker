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



class ManagerCalc(DataManager):
    def __init__(self, folder_path):
        self.extensions = ("xml", "csv")
        self.folder_path = folder_path


        self.files = self.get_files()
        self.content = self.load_files()
        self.data = self.parse_data_by_date()


    def get_files(self):
        """Zwraca listę plików z folderu z podanymi rozszerzeniami"""
        logger.info(f"Getting files from {self.folder_path}")
        files = []
        for ext in self.extensions:
            files.extend(glob.glob(os.path.join(self.folder_path, f"*.{ext}")))

        files.sort()  # uporządkowanie alfabetyczne

        # normalizacja separatorów
        files = [os.path.normpath(f) for f in files]
        logger.info(f"Found {len(files)} files")
        return files

    def load_csv(self, file_path):
        """Load CSV file and output list of dictionaries"""
        if not os.path.exists(file_path):
            logger.error(f"File {file_path} does not exist")
            raise FileNotFoundError(f"{file_path} does not exist")

        data = []
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({"date": row["date"], "value": float(row["value"])})
        logger.info(f"Loaded {len(data)} records from {file_path}")
        return data

    def load_xml(self, file_path):
        """Load XML file and output list of dictionaries"""
        if not os.path.exists(file_path):
            logger.error(f"File {file_path} does not exist")
            raise FileNotFoundError(f"{file_path} does not exist")

        logger.debug(f"Parsing XML file: {file_path}")
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = []
        for rate in root.findall(".//Rate"):
            date = rate.find("Date").text
            value = float(rate.find("Value").text)
            data.append({"date": date, "value": value})

        logger.info(f"Loaded {len(data)} records from {file_path}")
        return data

    def load_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".xml":
            return self.load_xml(file_path)
        elif ext == ".csv":
            return self.load_csv(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def load_files(self):
        files = self.get_files()

        files_content = {}
        for f in files:
            key = os.path.splitext(os.path.basename(f))[0]
            files_content[key] = (self.load_file(f))

        return files_content

    def parse_data_by_date(self):
        logging.info("Parsing data")
        data_by_date = {}

        for source, rates in self.content.items():
            for r in rates:
                date = r['date']
                value = r['value']
                if date not in data_by_date:
                    data_by_date[date] = {}
                data_by_date[date][source] = value
        logger.info(f"Parsed {len(data_by_date)} records")
        return data_by_date