#!/usr/bin/bash

cd /mnt

python3 src/main.py -from_date 2025-09-07 -to_date 2025-09-15 True >> logs/run.log 2>&1

python3 src/fetch.py -from_date 2025-09-07 -to_date 2025-09-15 -source NBP > data/nbp.xml
python3 src/fetch.py -from_date 2025-09-07 -to_date 2025-09-15 -source ECB > data/ecb.xml
