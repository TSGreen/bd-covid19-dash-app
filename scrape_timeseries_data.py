#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 21:52:44 2020

@author: tim
"""

from datetime import date
from pathlib import Path
import pandas as pd
import requests
from scrapy import Selector

url = "https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Bangladesh"

req = requests.get(url)
url_content = req.content
sel = Selector(text=url_content)
data_table = sel.xpath('//table[contains(@class, "wikitable sortable")]')
df = pd.read_html(data_table.extract_first())[0]

latest_update = df.iloc[-1][0]  # Checks the last date in the table

datedfile = Path.cwd().joinpath('data', 'time-series', 
                                f'Wikitable_{latest_update}.csv')
df.to_csv(datedfile)

latestfile = Path.cwd().joinpath('data', 'time-series', 
                                 f'Wikitable_latest.csv')
df.to_csv(latestfile)
