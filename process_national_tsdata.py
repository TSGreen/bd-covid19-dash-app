"""
Process the raw national COVID data and perform operations.

Processing include:
    - cleaning the scraped data (stripping unwanted refs & notes etc)

Operations include:
    - calculate positivity ratio
    - calculate rolling averages for daily stats

"""

import pandas as pd
from datetime import datetime
from pathlib import Path


timeseries_data = Path.cwd().joinpath('data',
                                      'raw',
                                      'Wikitable_latest.csv')

df = pd.read_csv(timeseries_data, header=1)


def clean_data(df, column):
    """Return data in correct data type and strip refs and notes."""
    if column == 'Date':
        df = df[column].apply(lambda x: x[:10])
        df = pd.to_datetime(df)
    else:
        df = df[column].apply(lambda x: str(x).split('[')[0])
        df = df.apply(lambda x: str(x).split('*')[0])
        df = df.apply(lambda x: str(x).replace(',', ''))
        df = df.astype(float)
    return df

df.drop('Notes', axis=1, inplace=True)

cols = ('Date', 'Total Tested', 'Total Cases', 'Total Deaths',
       'Total Recovered', 'Newly Tested', 'New Cases', 'New Deaths',
       'Newly Recovered')
for col in cols:
    df[col] = clean_data(df, col)

june = datetime.strptime('2020-06-01', "%Y-%m-%d")
may = datetime.strptime('2020-05-01', "%Y-%m-%d")
april = datetime.strptime('2020-04-01', "%Y-%m-%d")
charge = datetime.strptime('2020-06-29', "%Y-%m-%d")
eid1 = datetime.strptime('2020-05-25', "%Y-%m-%d")
eid2 = datetime.strptime('2020-05-28', "%Y-%m-%d")

#df = df.fillna(0)

df['Positivity rate'] = df['New Cases']/df['Newly Tested']
df['Positivity rate SMA7'] = df['Positivity rate'].rolling(window=7).mean()
df['Death case ratio'] = df['Total Deaths']/df['Total Cases']
df['Cases Normalised'] = df['New Cases']/df['New Cases'].sum()
df['Tests Normalised'] = df['Newly Tested']/df['Newly Tested'].sum()
df['Daily Tests SMA3'] = df['Newly Tested'].rolling(window=3).mean()
df['Daily Cases SMA3'] = df['New Cases'].rolling(window=3).mean()
df['Daily Deaths SMA3'] = df['New Deaths'].rolling(window=3).mean()
df['Daily Tests SMA7'] = df['Newly Tested'].rolling(window=7).mean()
df['Daily Cases SMA7'] = df['New Cases'].rolling(window=7).mean()
df['Daily Deaths SMA7'] = df['New Deaths'].rolling(window=7).mean()
df['Daily Recoveries SMA7'] = df['Newly Recovered'].rolling(window=7).mean()


processed_data = Path.cwd().joinpath('data',
                                     'processed',
                                     'national_data.csv')
df.to_csv(processed_data)