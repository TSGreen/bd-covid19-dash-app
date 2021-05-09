"""
Scrape the national COVID-19 data from Wikipedia table (which I help maintain).

The script outputs two identical CSV files: 
    (1) titled by date for archive
    (2) titled with "latest" for processing for web-app on that day.

@author: Tim Green
"""

from datetime import date
from pathlib import Path
import pandas as pd
import requests
from scrapy import Selector

url = "https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_Bangladesh"

req = requests.get(url)
url_content = req.content
sel = Selector(text=url_content)
data_table = sel.xpath('//table[contains(@class, "wikitable sortable")]')
df = pd.read_html(data_table.extract_first())[0]

latest_update = df.iloc[-1][0]  # Checks the last date in the table

data_filepath = Path.cwd().joinpath('data', 'raw')

dated_file = data_filepath.joinpath(f'Wikitable_{latest_update}.csv')
df.to_csv(dated_file)

latest_file = data_filepath.joinpath(f'Wikitable_latest.csv')
df.to_csv(latest_file)
