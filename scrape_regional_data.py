"""
Scrape the regional COVID-19 data from a Google sheet hosted by IEDCR .

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

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQgQAWwlQYF4XTxVT8sYP5wwqz_KxaWfVNQk9B0FlyPPpDphAIv1cRIMV4ve_1gNbewGjcbkKNpi3Wm/pub?gid=624602850&"

req = requests.get(url)
url_content = req.content
sel = Selector(text=url_content)
data_table = sel.xpath('//table')
df = pd.read_html(data_table.extract_first())[0]

data_filepath = Path.cwd().joinpath('data', 'raw')

dated_file = data_filepath.joinpath(f'regional_covid19_data_{date.today()}.csv')
df.to_csv(dated_file)

latest_file = data_filepath.joinpath('regional_covid19_data_latest.csv')
df.to_csv(latest_file)
