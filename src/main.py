from data_fetcher import ECBDataAPI, NBPDataAPI

# config
DATE_START = "2025-09-10"
DATE_END = "2025-09-11"


nbp_api = NBPDataAPI(DATE_START, DATE_END)
ecb_api = ECBDataAPI(DATE_START, DATE_END)

# get data
nbp_data = nbp_api.get_data()
ecb_data = ecb_api.get_data()


# parse to simple xml format
nbp_rates = nbp_api.parse_data(nbp_data)
ecb_rates = ecb_api.parse_data(ecb_data)

# save (overwrite) to the file
#nbp_api.save_data(nbp_rates)
#ecb_api.save_data(ecb_rates)

# save (merge) to the file
nbp_api.merge_data(nbp_rates)
ecb_api.merge_data(ecb_rates)