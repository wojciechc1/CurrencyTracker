from currency_calculator import CurrencyCalculator
import argparse


def main(data_folder_dir: str):
    calc = CurrencyCalculator(f"{data_folder_dir}/nbp.xml", f"{data_folder_dir}/ecb.xml")
    diffs = calc.compute_difference()
    for d in diffs:
        print(d["date"], d["diff"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Currency Calculator")
    parser.add_argument("--data_folder", help="Directory where data is stored")
    args = parser.parse_args()

    main(args.data_folder)
    #python3 src/calc.py -data_folder data