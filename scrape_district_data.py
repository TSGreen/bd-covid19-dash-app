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

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQgQAWwlQYF4XTxVT8sYP5wwqz_KxaWfVNQk9B0FlyPPpDphAIv1cRIMV4ve_1gNbewGjcbkKNpi3Wm/pub?gid=624602850&"

req = requests.get(url)
url_content = req.content
sel = Selector(text=url_content)
data_table = sel.xpath('//table')
df = pd.read_html(data_table.extract_first())[0]

today = date.today()

datedfile = Path.cwd().joinpath('data', 'district-wise', f'DistrictWise_Distribution_{today.month}-{today.day}.csv')
df.to_csv(datedfile)

latestfile = Path.cwd().joinpath('data', 'district-wise', f'DistrictWise_Distribution_Latest.csv')
df.to_csv(latestfile)
