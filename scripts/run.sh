#!/usr/bin/bash

cd /mnt

python3 src/fetch.py --from_date 2025-09-07 --source NBP --out_format CSV --path nbp.csv 2> logs/run.log
python3 src/fetch.py --from_date 2025-09-07 --source ECB --out_format CSV --path ecb.csv 2> logs/run.log
