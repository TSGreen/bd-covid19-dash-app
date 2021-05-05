#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrape the national COVID-19 data from table on Wikipedia (which I help maintain).

Save two identical files: one dated for archive and one called "latest" for
processing.

@author: tim
"""

from datetime import date
from pathlib import Path
import pandas as pd
import requests
from scrapy import Selector

#url = "https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Bangladesh"
url = "https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_Bangladesh"

req = requests.get(url)
url_content = req.content
sel = Selector(text=url_content)
data_table = sel.xpath('//table[contains(@class, "wikitable sortable")]')
df = pd.read_html(data_table.extract_first())[0]

latest_update = df.iloc[-1][0]  # Checks the last date in the table

datedfile = Path.cwd().joinpath('data', 'raw',
                                f'Wikitable_{latest_update}.csv')
df.to_csv(datedfile)

latestfile = Path.cwd().joinpath('data', 'raw',
                                 f'Wikitable_latest.csv')
df.to_csv(latestfile)
