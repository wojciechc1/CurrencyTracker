from data_fetcher import ECBDataAPI, NBPDataAPI
import argparse
import datetime


def main(date_start: str, date_end: str, source, path: str, out_format: str):

    date_end = datetime.date.today() if date_end is None else date_end


    if source == "NBP":
        bank_api = NBPDataAPI(date_start, date_end, out_format)
    elif source == "ECB":
        bank_api = ECBDataAPI(date_start, date_end, out_format)
    else:
        return

    # get data
    data = bank_api.get_data()

    # parse to list of dicts
    rates = bank_api.parse_data(data)


    formatted = bank_api.get_data_formatted(rates)

    if path is not None:
        bank_api.save_to_file(path, formatted)
    else:
        print(formatted)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Currency Tracker")
    parser.add_argument("--from_date", required=True, help="Date start in format: YYYY-MM-DD")
    parser.add_argument("--to_date", required=False, help="Date end in format: YYYY-MM-DD")
    parser.add_argument("--source", required=True, help="Source of data: NBP or ECB")

    parser.add_argument("--path", required=False, help="Path where to save file")
    parser.add_argument("--out_format", required=False, help="Output format: CSV, XML or BLANK (default)")
    args = parser.parse_args()

    main(args.from_date, args.to_date, args.source, args.path, args.out_format)