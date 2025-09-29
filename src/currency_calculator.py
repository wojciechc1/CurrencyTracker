import os
import logging
from data_manager.manager_calc import ManagerCalc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


class CurrencyCalculator():
    def __init__(self, file_path):
        self.data_manager = ManagerCalc(file_path)
        self.data_by_date = self.data_manager.data

    def save_to_file(self, data, path):
        self.data_manager.save_to_file(data, path)

    def get_data(self):
        return self.data_manager.data

    def get_csv(self, data):
        return self.data_manager.get_csv(data)

    def get_xml(self, data):
        return self.data_manager.get_xml(data)

    def calculate_min_max(self):
        logger.info("Calculating min and max")
        result = []
        for date, rates in self.data_by_date.items():
            min_val = min(rates.values())
            max_val = max(rates.values())
            min_sources = [src for src, val in rates.items() if val == min_val]
            max_sources = [src for src, val in rates.items() if val == max_val]

            row = {
                'date': date,
                **rates,
                'min': min_val,
                'min_sources': ",".join(min_sources),
                'max': max_val,
                'max_sources': ",".join(max_sources)
            }
            result.append(row)
        self.data_manager.data = result
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
        self.data_manager.data = result
        return result