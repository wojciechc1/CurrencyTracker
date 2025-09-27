# Currency Tracker with Linux

Currency Tracker is a Python project that fetches historical and current exchange rates from multiple sources (NBP and ECB), parses the data, and stores it in XML format. It also allows calculating differences between sources.

## Features
- Download exchange rates from NBP and ECB APIs
- Parse and store data in structured XML
- Merge new data without overwriting existing entries
- Calculate differences between sources


## Usage
1. Set the desired date range.
2. Run 
```bash
  # 1. create folder
  python3 src/main.py -from_date 2025-09-07 -to_date 2025-09-15 True
  
  # 2. merge data
  python3 src/main.py -from_date 2025-09-07 -to_date 2025-09-15 False
```


## Requirements
- Python 3.12+
- requests
