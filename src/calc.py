from currency_calculator import CurrencyCalculator
import argparse


def main(data_folder_dir: str, path: str, operation: int, out_format: str, ):
    cc = CurrencyCalculator(data_folder_dir)

    d = cc.calculate_percent_from_avg()
    m = cc.calculate_min_max()

    cc = CurrencyCalculator(data_folder_dir)

    operation = int(operation)
    if operation == 1:
        calc = cc.calculate_percent_from_avg()
    elif operation == 2:
        calc = cc.calculate_min_max()

    if out_format == "CSV":
        formatted = cc.get_csv(calc)
    elif out_format == "XML":
        formatted = cc.get_xml(calc)
    else:
        formatted = calc

    if path is not None:
        cc.save_to_file(formatted, path)
    else:
        print(formatted)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Currency Calculator")
    parser.add_argument("--data_folder", help="Directory where data is stored")
    parser.add_argument("--operation", help="Operation to perform. 1: percent from avg, 2: min and max")

    parser.add_argument("--path", required=False, help="Path where to save file")
    parser.add_argument("--out_format", required=False, help="Output format: CSV, XML or BLANK (default)")
    args = parser.parse_args()

    main(args.data_folder, args.path, args.operation, args.out_format)
    #python3 src/calc.py -data_folder data