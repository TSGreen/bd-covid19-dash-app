"""

Build dash app of COVID-19 data in Bangladesh.

Requires access to regional data in a shapefile and national time-series data
in a csv.

Will be deployed to GitHub and Heroku.
"""


import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df_districts_cv19_pop = gpd.read_file('./data/data.shp')
df_districts_cv19_pop.rename(columns=dict(zip(df_districts_cv19_pop.columns, 
       ['Shape_Length', 'Shape_Area', 'District', 'ADM2_PCODE', 'ADM2_REF',
       'ADM2ALT1EN', 'ADM2ALT2EN', 'ADM1_EN', 'ADM1_PCODE', 'ADM0_EN',
       'ADM0_PCODE', 'date', 'validOn', 'ValidTo', 'Division', 'Updated Date',
       'Total Cases', 'Divisional Cases', 'Log(Cases)', 'Abbr.', 'Status', 
       'Native', 'Adm.', 'Area', 'Population_1991', 'Population_2001', 'Population_2011',
       'Population_2016', 'Cases Per Thousand', 'geometry'])), inplace=True)
df_districts_cv19_pop['Population (Millions)']=df_districts_cv19_pop['Population_2016']/1E6

national_data = Path.cwd().joinpath('data', 'processed_data.csv')
df = pd.read_csv(national_data)
df.Date = pd.to_datetime(df.Date)

# Build App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

hoverform = "%{y:,.0f}"

colors = {
    'background': '#fafafa',
    'text': '#003366'}


fig_daily = go.Figure()
fig_daily.add_trace(go.Bar(x=df['Date'], y=df['Newly Tested'], name='Daily Tests',
                         marker_color='rgb(49,130,189)',    
                         hovertemplate = hoverform))
fig_daily.add_trace(go.Scatter(x=df['Date'], y=df['Daily Tests SMA7'], name='Daily Tests (7-day rolling avg)',
                         line=dict(color='rgb(49,130,189)', width=3), visible='legendonly', 
                         hovertemplate = hoverform))

fig_daily.add_trace(go.Bar(x=df['Date'], y=df['New Cases'], name='Daily Cases',
                         marker_color='green', hovertemplate = hoverform))
fig_daily.add_trace(go.Scatter(x=df['Date'], y=df['Daily Cases SMA7'], name='Daily Cases (7-day rolling avg)',
                         line=dict(color='green', width=3), visible='legendonly',
                         hovertemplate = hoverform))

fig_daily.add_trace(go.Bar(x=df['Date'], y=df['Newly Recovered'], name='Daily Recoveries',
                         marker_color='rgb(235,186,20)', hovertemplate = hoverform))
fig_daily.add_trace(go.Scatter(x=df['Date'], y=df['Daily Recoveries SMA7'], name='Daily Recoeries (7-day rolling avg)',
                         line=dict(color='rgb(235,186,20)', width=3), visible='legendonly',
                         hovertemplate = hoverform))

fig_daily.add_trace(go.Bar(x=df['Date'], y=df['New Deaths'], name='Daily Deaths',
                         marker_color='firebrick', hovertemplate = hoverform))
fig_daily.add_trace(go.Scatter(x=df['Date'], y=df['Daily Deaths SMA7'], name='Daily Deaths (7-day rolling avg)',
                         line=dict(color='firebrick', width=3), visible='legendonly', 
                         hovertemplate = hoverform))

fig_daily.update_layout(
    barmode='overlay',
    hovermode='x unified',
    title='Daily Cases, Tests, Deaths and Recoveries',
    xaxis_title='Date',
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    height=750,
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            active=0,
            x=0.7,
            y=1.2,
            buttons=list([
                dict(label="All",
                     method="update",
                     args=[{"visible": [True, True, True, True, True, True, True, True]},
                           {"title": "Daily Cases, Tests, Deaths and Recoveries"}
                          ]),
                dict(label="Tests",
                     method="update",
                     args=[{"visible": [True, True, False, False, False, False,  False, False]},
                           {"title": "Tests",}
                            ]),
                dict(label="Cases",
                     method="update",
                     args=[{"visible": [False, False, True, True, False, False,  False, False]},
                           {"title": "Cases",}
                            ]),
                dict(label="Recoveries",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, True, False, False]},
                           {"title": "Recoveries",}
                            ]),
                dict(label="Deaths",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, True, True]},
                           {"title": "Deaths",}
                            ]),
                dict(label="Bars Only",
                     method="update",
                     args=[{"visible": [True, False, True, False, True, False, True, False]},
                           {"title": "Daily Cases, Tests, Deaths and Recoveries"}
                            ]),
                 dict(label="Lines Only",
                     method="update",
                     args=[{"visible": [False, True, False, True, False, True, False, True]},
                           {"title": "Daily Cases, Tests, Deaths and Recoveries"}
                            ]),           
            ]),
        )
    ])

fig_daily.update_xaxes(#rangeslider_visible=True,
        rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=2, label="2m", step="month", stepmode="backward"),
            dict(count=3, label="3m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(step="all")
        ])
    ))


fig = px.choropleth_mapbox(df_districts_cv19_pop, geojson=df_districts_cv19_pop,
                           locations='District', color='Log(Cases)',
                           hover_name='District',
                           hover_data={'Total Cases': True, 'Log(Cases)': False, 'District': False},
                           center={"lat": 23.7, "lon": 90.2},
                           featureidkey='properties.District',
                           mapbox_style="carto-positron",
                           zoom=6,
                           height=800, 
                           opacity=0.7,
                           title='Confirmed cases per district',
                           color_continuous_scale='OrRd',
                           range_color=[1, 5])

fig_density = px.choropleth_mapbox(df_districts_cv19_pop, geojson=df_districts_cv19_pop,
                           locations='District', color='Cases Per Thousand',
                           hover_name='District',
                           hover_data={'Cases Per Thousand':True, 'Total Cases':True, 'Population (Millions)':True, 'Log(Cases)':False, 'District':False},
                           center={"lat": 23.7, "lon": 90.2},
                           featureidkey='properties.District',
                           mapbox_style="carto-positron", 
                           zoom=6,
                           height=800, 
                           opacity=0.7,
                           title='Confirmed cases per thousdand people per district',
                           color_continuous_scale='OrRd',
                           range_color=[0, 5])


fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])

fig_density.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])

server = app.server

table_contents = '''
1. Chart of [daily cases, tests, recoveries & deaths.](#daily-data-graph)
2. Map of [confirmed cases per district.](#district-cases)
3. Map of [confirmed cases per thousdand people.](#district-cases_pt)
'''

introduction = '''
An interactive exploration of Covid-19 data for Bangladesh.

Data source: [IEDCR](https://iedcr.gov.bd/).
Data on this page last updated: 25 August 2020.
'''

credit = '''
Page built in Python by [Timothy Green](https://github.com/TSGreen). 
[Source code](https://github.com/TSGreen/bd-covid19-dash-app).
'''

top = '''
[(top)](#top)'''

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, 
    children=[
    html.H1("Bangladesh Covid-19 Data",
            style={
            'textAlign': 'center',
            'color': colors['text']}),
           
    html.Div([dcc.Markdown(children=introduction)], 
             style={
        'textAlign': 'center',
        'color': colors['text']}),
           
    html.Div(children=[dcc.Markdown(children=table_contents)], id='top', style={
        'textAlign': 'left',
        'color': colors['text']}),
           
    dcc.Graph(id='daily-data-graph', figure=fig_daily, style={'width':'90vw'}),
    html.Div([dcc.Markdown(children=top)]),
        
    dcc.Graph(id='district-cases', figure=fig, style={'width':'90vw'}),
    html.Div([dcc.Markdown(children=top)]),
        
    dcc.Graph(id='district-cases_pt', figure=fig_density, style={'width':'90vw'}),
    html.Div([dcc.Markdown(children=top)]),    
    
    html.Div([dcc.Markdown(children=credit)], 
       style={'textAlign': 'center',
              'color': colors['text']}),
])

#app.run_server(debug=True, port=8090)
