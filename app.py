
"""

Build Dash app of COVID-19 data in Bangladesh. 
Includes interactive Plotly visualtions of regional and national data.

Reads the processed regional data in a shapefile and the processed national 
time-series data in a csv.

To be deployed to GitHub and Heroku.

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

regional_datafile = Path.cwd().joinpath('data', 'processed', 'regional_data.shp')

df_districts_cv19_pop = gpd.read_file(regional_datafile)
df_districts_cv19_pop.rename(columns=dict(zip(df_districts_cv19_pop.columns,
       ['Shape_Length', 'Shape_Area', 'District', 'ADM2_PCODE', 'ADM2_REF',
       'ADM2ALT1EN', 'ADM2ALT2EN', 'ADM1_EN', 'ADM1_PCODE', 'ADM0_EN',
       'ADM0_PCODE', 'date', 'validOn', 'ValidTo', 'Division', 'Updated Date',
       'Total Cases', 'Divisional Cases', 'Log(Cases)', 'Abbr.', 'Status', 
       'Native', 'Adm.', 'Area', 'Population_1991', 'Population_2001', 
       'Population_2011', 'Population_2016', 'Cases Per Thousand', 'geometry']))
                             , inplace=True)
df_districts_cv19_pop['Population (Millions)'] = df_districts_cv19_pop['Population_2016']/1E6
def calculate_percentage(dataframe, column):
    return (dataframe[column]*100/dataframe[column].sum()).round(1)

df_districts_cv19_pop['Cases percent'] = calculate_percentage(df_districts_cv19_pop, 'Total Cases')

national_data = Path.cwd().joinpath('data', 'processed', 'national_data.csv')
df = pd.read_csv(national_data)
df.Date = pd.to_datetime(df.Date)

# Build App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

hoverform = "%{y:,.0f}"

latest_update = df.iloc[-1]['Date']

colors = {'background': '#fafafa',
          'text': '#003366'}

fig_daily = go.Figure()

def plot_dailyparameter(parameter, colour):
    
    if parameter == 'Daily Tests':
        columns = ['Newly Tested', 'Daily Tests SMA7'] 
    elif parameter == 'Daily Cases':
        columns = ['New Cases', 'Daily Cases SMA7'] 
    elif parameter == 'Daily Recoveries':
        columns = ['Newly Recovered', 'Daily Recoveries SMA7'] 
    elif parameter == 'Daily Deaths':
        columns = ['New Deaths', 'Daily Deaths SMA7'] 
        
    fig_daily.add_trace(go.Bar(x=df['Date'], 
                               y=df[columns[0]],
                               name=parameter,
                               marker_color=colour,
                               hovertemplate = hoverform))
    
    fig_daily.add_trace(go.Scatter(x=df['Date'], 
                                   y=df[columns[1]],
                                   name=f'{parameter}<br>(7-day rolling avg)',
                                   line=dict(color=colour, width=3),
                                   visible='legendonly',
                                   hovertemplate = hoverform))
    

plot_dailyparameter('Daily Tests', 'rgb(49,130,189)')
plot_dailyparameter('Daily Cases', 'green')
plot_dailyparameter('Daily Recoveries', 'rgb(235,186,20)')
plot_dailyparameter('Daily Deaths', 'firebrick')

fig_daily.update_layout(
    legend_title_text='<b>Click to hide/show:</b><br>',
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
                     args=[{"visible": [True, True, False, False, False, False, False, False]},
                           {"title": "Tests"}
                            ]),
                dict(label="Cases",
                     method="update",
                     args=[{"visible": [False, False, True, True, False, False, False, False]},
                           {"title": "Cases"}
                            ]),
                dict(label="Recoveries",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, True, False, False]},
                           {"title": "Recoveries"}
                            ]),
                dict(label="Deaths",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, True, True]},
                           {"title": "Deaths"}
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

lines = go.Figure()

# lines.add_trace(go.Scatter(
#     x=[None], y=[None],
#     name='<b>Click to hide/show:</b>',
#     line={'color': 'rgba(0, 0, 0, 0)'}
# ))

def plot_totalparameter(parameter, colour):

    lines.add_trace(go.Scatter(x=df['Date'], 
                                   y=df[parameter],
                                   name=parameter,
                                   line=dict(color=colour, width=3),
                                   hovertemplate = hoverform))

plot_totalparameter('Total Tested', 'rgb(49,130,189)')
plot_totalparameter('Total Cases', 'green')
plot_totalparameter('Total Recovered', 'rgb(235,186,20)')
plot_totalparameter('Total Deaths', 'firebrick')


lines.update_layout(
    legend_title_text='<b>Click to hide/show:</b><br>',
    hovermode='x unified',
    title='Total Cumulative Cases, Tests, Deaths and Recoveries',
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
                     args=[{"visible": [True, True, True, True]},
                           {"title": "Total Cumulative Cases, Tests, Deaths and Recoveries"}
                          ]),
                dict(label="Tests",
                     method="update",
                     args=[{"visible": [True, False, False, False]},
                           {"title": "Total Tests"}
                            ]),
                dict(label="Cases",
                     method="update",
                     args=[{"visible": [False, True, False, False]},
                           {"title": "Cases"}
                            ]),
                dict(label="Recoveries",
                     method="update",
                     args=[{"visible": [False, False, True, False]},
                           {"title": "Recoveries"}
                            ]),
                dict(label="Deaths",
                     method="update",
                     args=[{"visible": [False, False, False, True]},
                           {"title": "Deaths"}
                            ]),
            ]),
        )
    ])

lines.update_xaxes(#rangeslider_visible=True,
        rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=2, label="2m", step="month", stepmode="backward"),
            dict(count=3, label="3m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(step="all")
        ])
    ))


##############################################################################
################          Maps                   #############################
##############################################################################

fig = px.choropleth_mapbox(df_districts_cv19_pop, geojson=df_districts_cv19_pop,
                           locations='District', color='Log(Cases)',
                           hover_name='District',
                           hover_data={'Total Cases': True, 'Cases percent': True, 'Log(Cases)': False, 'District': False},
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
2. Chart of [total cumulative cases, tests, recoveries & deaths.](#total-data-graph)
3. Map of [confirmed cases per district.](#district-cases)
4. Map of [confirmed cases per thousdand people.](#district-cases_pt)
'''

introduction = f'''
An interactive exploration of Covid-19 data for Bangladesh.

Data source: [IEDCR](https://iedcr.gov.bd/).
Data on this page last updated: {latest_update.day} {latest_update.month_name()} {latest_update.year}.
'''

daily_obs = """
#### Observations:
* The number of daily confirmed cases appeared to level out and decrease at the beggining of July, but this very closely maps the decrease in testing at this time, so it most likely to be due to insufficient testing. 
The rate of testing declined almost immediately after the government annouced on 29 June that a charge would be imposed for COVID tests (which had hiterheto been free at government run facilities).                                                                                     
* It is encouraging that by late August, despite the number of daily tests levelling out at a slightly higher rate than in July, there is modest decline in number of confirmed daily cases.
* The daily figures vary with day of the week, with lower numbers reported on weekends and higher numbers mid-week (Tues & Weds).
* Significant drops in the daily figures were observed around 26 May 2020 and 2 August 2020 because of Eid ul-Fitr and Eid al-Adha respectively.
* There is a spike in recoveries on 15 June due to a change in  reporting policy. The health ministry included recoveries at home (i.e. outside of hopsitals) from this date. 
"""
credit = '''
Page built in Python by [Timothy Green](https://github.com/TSGreen). 
[Source code](https://github.com/TSGreen/bd-covid19-dash-app).
'''

top = '''
[(top)](#top)'''

center_text = {'textAlign': 'center', 'color': colors['text']}
left_text = {'textAlign': 'left', 'color': colors['text']}
       
app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
    html.H1("Bangladesh Covid-19 Data", style=center_text),

    html.Div([dcc.Markdown(children=introduction)], style=center_text),

    html.Div(children=[dcc.Markdown(children=table_contents)], id='top', 
             style=left_text),
    
    dcc.Graph(id='daily-data-graph', figure=fig_daily, style={'width':'90vw'}),
    html.Div([dcc.Markdown(children=daily_obs)], style=left_text),
    html.Div([dcc.Markdown(children=top)]),

    dcc.Graph(id='total-data-graph', figure=lines, style={'width':'90vw'}),
    html.Div([dcc.Markdown(children=top)]),

    dcc.Graph(id='district-cases', figure=fig, style={'width':'90vw'}),
    html.Div([dcc.Markdown(children=top)]),

    dcc.Graph(id='district-cases_pt', figure=fig_density, style={'width':'90vw'}),
    html.Div([dcc.Markdown(children=top)]),    

    html.Div([dcc.Markdown(children=credit)], style=center_text),
    ])

app.run_server(debug=True, port=8095)
