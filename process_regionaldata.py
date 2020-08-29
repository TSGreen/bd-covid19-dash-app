#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Combine datasets, perform some operations and output data file for app deployment. 

The datasets involved are:
    - administrative geodata (contains polygons of district boundaries for mapping)
    - population data (bangladeshi population stats by district)
    - COVID-19 data (distrist wise confirmed cases of covid-19)
    

@author: tim
"""


import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import difflib
import math
from pathlib import Path

def rename_ctg(dataframe):
    """
    Change incidences of "Chittagong" in specified dataframe with
    "Chattogram".
    
    Justification: The city, district and division of Chittagong officially 
    changed its name to Chattogram in 2018. But old name common in data files.
    """
    dataframe.replace({'Chittagong': 'Chattogram'}, inplace=True)
    
def combine_datasets(df1, district_col1, df2, district_col2):
    """
    Combine dataframes on the district name feature.
    This includes a feature to match names which can vary in spelling when 
    translated to English
    """
    # Corrects for small variations in English spelling of district names 
    # between data frames (e.g Comilla and Cumilla) in preparation for joining
    df1[district_col1] = df1[district_col1].apply(
    lambda x: difflib.get_close_matches(x, df2[district_col2], n=1)[0])
    # Combines the data frames of Covid dataset and district coord dataset
    return df1.join(df2.set_index(district_col2), on=district_col1, how = 'outer') 


import numpy as np
def aggregate_dhaka(dataframe):
    """
    Govt covid data separates cases numbers for Dhaka city and Dhaka district (outside of the city). 
    This function sums the two numbers to get total cases in Dhaka district.

    Parameters
    ----------
    dataframe : pandas dataframe to be executed on

    Returns
    -------
    Dataframe

    """
    dataframe['District/City'].replace({'Dhaka City': 'Dhaka', 'Dhaka (District)': 'Dhaka'}, inplace=True)
    temp1 = dataframe.groupby(by='District/City', as_index=False).agg(''.join)
    #testdict = {k:(print if k in {'Division', 'Updated Date','Divisional Cases'} else np.sum) for k in dataframe.columns if k not in {'District/Ciy'}}
    temp2 = dataframe.groupby(by='District/City', as_index=False).agg(sum)
    dataframe = temp1.merge(temp2, on='District/City')
    dataframe['Division'].replace({'DhakaDhaka':'Dhaka'}, inplace=True)
    return dataframe


geodata_file = Path.cwd().joinpath('data', 'raw', 'bgd_admbnda_adm2_bbs_20180410.shp')
district_geodata = gpd.read_file(geodata_file)
rename_ctg(district_geodata)

districtwise_data = Path.cwd().joinpath('data', 'raw', 'regional_covid19_data_latest.csv')
cv19_dist = pd.read_csv(districtwise_data, header=1)
cv19_dist = cv19_dist.iloc[1:-1]
cv19_dist.rename(columns={'Unnamed: 2': 'Division', 'Total': 'Divisional Cases'}, inplace=True)
cv19_dist.drop(columns=['0', '1.0', 'Unnamed: 7'], inplace=True)
cv19_dist = aggregate_dhaka(cv19_dist)

#  Corrects for the major differences in english naming of some districts
cv19_dist['District/City'].replace({'B. Baria': 'Brahamanbaria',
                                    'Khagrachari': 'Khagrachhari',
                                    'Chapainawabganj': 'Nawabganj'}, inplace=True)


df_districts_cv19 = combine_datasets(district_geodata, 'ADM2_EN', cv19_dist, 'District/City')


df_districts_cv19 = df_districts_cv19.iloc[:,:19]

df_districts_cv19['Log(Cases)'] = df_districts_cv19['Total Cases in District'].apply(lambda x: math.log10(x) if x > 0 else 1E-2)  

population_datafile = Path.cwd().joinpath('data', 'raw', 'population_district_wise.csv')
populations_df = pd.read_csv(population_datafile)
rename_ctg(populations_df)

df_districts_cv19_pop = combine_datasets(df_districts_cv19, 'ADM2_EN', populations_df, 'Name')
df_districts_cv19_pop['Confirmed Cases pt'] = 1000*df_districts_cv19_pop['Total Cases in District']/df_districts_cv19_pop['Population_2016']                                    
df_districts_cv19_pop.rename(columns={'ADM2_EN': 'District'}, inplace=True)

cleandatafile = Path.cwd().joinpath('data', 'processed', 'regional_data.shp')

df_districts_cv19_pop.to_file(driver='ESRI Shapefile', filename=cleandatafile)
