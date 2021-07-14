#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 21:09:50 2020

@author: tim
"""

import pandas as pd

df = pd.read_csv('data/processed/national_data.csv',
                 parse_dates=['Date'], index_col='Date')

#df['2020-08-01':]['Newly Tested'].fillna(0).astype('int').values

#df['2020-07-10':]['Total Deaths'].fillna(0).astype('int').values

# Aug-1 , Aug-2 , Aug-3 , Aug-4 , Aug-5 , Aug-6 , Aug-7 ,
# Aug-8 , Aug-9 , Aug-10 , Aug-11 , Aug-12 , Aug-13 , Aug-14 ,
# Aug-15 , Aug-16 , Aug-17 , Aug-18 , Aug-19 , Aug-20 ,
# Aug-21 , Aug-22 , Aug-23 , Aug-24 , Aug-25 , Aug-26 ,
# Aug-27 , Aug-28 , Aug-29 , Aug-30 , Aug-31,
# Sept-1 , Sept-2 , Sept-3 , Sept-4 , Sept-5 , Sept-6 ,
# Sept-7 , Sept-8 , Sept-9 , Sept-10 , Sept-11 , Sept-12 ,
# Sept-13 , Sept-14 , Sept-15 , Sept-16 , Sept-17 , Sept-18 ,
# Sept-19 , Sept-20 , Sept-21 , Sept-22 , Sept-23 , Sept-24 ,
# Sept-25 , Sept-26 , Sept-27 , Sept-28 , Sept-29 , Sept-30,
# Oct-1 , Oct-2 , Oct-3 , Oct-4 , Oct-5 , Oct-6 , Oct-7 

df['positivity'] = df['New Cases'].div(df['Newly Tested']).mul(100)



df['2020-04-01':].positivity.values

df['2020-04-01':]['Total Cases'].values

df['2020-04-01':]['New Cases'].values

df['2020-04-01':]['Total Recovered'].values

df['2020-04-01':]['Total Deaths'].values