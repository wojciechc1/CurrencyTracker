from data_fetcher import ECBDataAPI, NBPDataAPI
import argparse
import datetime


def main(date_start: str, date_end: str, source, file_name: str, out_format: str):

    date_end = datetime.date.today() if date_end is None else date_end


    if source == "NBP":
        bank_api = NBPDataAPI(date_start, date_end)
    elif source == "ECB":
        bank_api = ECBDataAPI(date_start, date_end)


    # get data
    data = bank_api.get_data()

    # parse to list of dicts
    rates = bank_api.parse_data(data)


    if out_format == "CSV":
        formatted = bank_api.get_csv(rates)
    elif out_format == "XML":
        formatted = bank_api.get_xml(rates)

    if file_name is not None:
        print('test')
    else:
        print(formatted)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Currency Tracker")
    parser.add_argument("--from_date", required=True, help="Date start in format: YYYY-MM-DD")
    parser.add_argument("--to_date", required=False, help="Date end in format: YYYY-MM-DD")
    parser.add_argument("--source", required=True, help="Source of data: NBP or ECB")

    parser.add_argument("--file_name", required=False, help="Output file name. If not given then prints output")
    parser.add_argument("--out_format", required=False, default="CSV", help="Output format: CSV (default) or XML.")
    args = parser.parse_args()

    main(args.from_date, args.to_date, args.source, args.file_name, args.out_format) #!TODO SAVE FOLDERS DIRS