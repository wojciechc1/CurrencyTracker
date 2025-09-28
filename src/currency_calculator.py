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


class Data_Manager:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.extensions = ("xml", "csv")

        self.files = self.get_files()
        self.content = self.load_files()
        self.data_by_date =  self.parse_data_by_date()


    def get_files(self):
        """Zwraca listę plików z folderu z podanymi rozszerzeniami"""
        logger.info(f"Getting files from {self.folder_path}")
        files = []
        for ext in self.extensions:
            files.extend(glob.glob(os.path.join(self.folder_path, f"*.{ext}")))

        files.sort()  # uporządkowanie alfabetyczne / chronologiczne

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



class CurrencyCalculator(Data_Manager):
    def __init__(self, file_path):
        super().__init__(file_path)

    def calculate_min_max(self):
        logger.info("Calculating min and max")
        result = []
        for date, rates in self.data_by_date.items():
            min_val = min(rates.values())
            max_val = max(rates.values())
            min_sources = [src for src, val in rates.items() if val == min_val]
            max_sources = [src for src, val in rates.items() if val == max_val]

            # wiersz płaski do CSV/XML
            row = {
                'date': date,
                **rates,  # kolumny dla każdego źródła
                'min': min_val,
                'min_sources': ",".join(min_sources),
                'max': max_val,
                'max_sources': ",".join(max_sources)
            }
            result.append(row)
        return result

    def calculate_percent_from_avg(self):
        logger.info("Calculating percent from avg rate.")
        result = []
        for date, rates in self.data_by_date.items():
            values = list(rates.values())
            avg_val = sum(values) / len(values) if values else 0
            percent_diffs = {
                f'percent_{src}': round((val - avg_val) / avg_val * 100, 2) if avg_val != 0 else 0
                for src, val in rates.items()
            }

            row = {
                'date': date,
                **rates,
                'avg_val': round(avg_val, 4),
                **percent_diffs
            }
            result.append(row)
        return result


cc = CurrencyCalculator("../data")

d = cc.calculate_percent_from_avg()
m = cc.calculate_min_max()
print(d)
