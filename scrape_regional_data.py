#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrape the regional COVID-19 data from the online IEDCR Google sheet.

Save two identical files: one dated for archive and one called "latest" for
processing.

@author: tim
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

today = date.today()

datedfile = Path.cwd().joinpath('data', 'raw', f'regional_covid19_data_{today}.csv')
df.to_csv(datedfile)

latestfile = Path.cwd().joinpath('data', 'raw', f'regional_covid19_data_latest.csv')
df.to_csv(latestfile)
