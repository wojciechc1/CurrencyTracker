import os
import xml.etree.ElementTree as ET


class CurrencyCalculator:
    def __init__(self, nbp_file, ecb_file):
        self.nbp_file = nbp_file
        self.ecb_file = ecb_file
        self.nbp_data = self.load_xml(self.nbp_file)
        self.ecb_data = self.load_xml(self.ecb_file)

    def load_xml(self, file_path):
        """Load XML file and output list of dictionaries"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist")
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = []
        for rate in root.findall(".//Rate"):
            date = rate.find("Date").text
            value = float(rate.find("Value").text)
            data.append({"date": date, "value": value})
        return data

    def compute_difference(self):
        """Computes difference NBP - ECB"""
        ecb_dict = {d['date']: d['value'] for d in self.ecb_data}
        results = []
        for d in self.nbp_data:
            date = d['date']
            nbp_val = d['value']
            ecb_val = ecb_dict.get(date)
            if ecb_val is not None:
                diff = round(nbp_val - ecb_val, 4)
                results.append({"date": date, "diff": diff})
        return results



calc = CurrencyCalculator("data/nbp.xml", "data/ecb.xml")
diffs = calc.compute_difference()
for d in diffs:
    print(d["date"], d["diff"])
