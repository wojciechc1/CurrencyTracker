from data_fetcher import ECBDataAPI, NBPDataAPI
import argparse


def main(date_start: str, date_end: str, overwrite: str):

    # config
    date_start = "2025-09-10" if date_start is None else date_start
    date_end = "2025-09-20" if date_end is None else date_end


    nbp_api = NBPDataAPI(date_start, date_end)
    ecb_api = ECBDataAPI(date_start, date_end)

    # get data
    nbp_data = nbp_api.get_data()
    ecb_data = ecb_api.get_data()


    # parse to simple xml format
    nbp_rates = nbp_api.parse_data(nbp_data)
    ecb_rates = ecb_api.parse_data(ecb_data)

    if overwrite == "True":
        # save (overwrite) to the file
        nbp_api.save_data(nbp_rates)
        ecb_api.save_data(ecb_rates)
    elif overwrite == "False":
        # save (merge) to the file
        nbp_api.merge_data(nbp_rates)
        ecb_api.merge_data(ecb_rates)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Currency Tracker")
    parser.add_argument("-from_date", help="Date start in format: YYYY-MM-DD")
    parser.add_argument("-to_date", help="Date end in format: YYYY-MM-DD")
    parser.add_argument("overwrite", help="True if you want to overwrite files; False if you want to append data to existing files")
    args = parser.parse_args()

    main(args.from_date, args.to_date, args.overwrite)