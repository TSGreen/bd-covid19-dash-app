"""
Build Dash app of COVID-19 data in Bangladesh.
Includes interactive Plotly visualizations of regional and national data.

Reads the processed regional data in a shapefile and the processed national 
time-series data in a csv.

To be deployed to GitHub and Heroku.
"""

import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

from textual_content import TextualContent

def plot_totalparameter(parameter, colour):

    lines.add_trace(go.Scatter(x=df['Date'], 
                                   y=df[parameter],
                                   name=parameter,
                                   line=dict(color=colour, width=3),
                                   hovertemplate = hoverform))

def calculate_percentage(dataframe, column):
    """Returns percentage rounded to one decimal place."""
    return (dataframe[column]*100/dataframe[column].sum()).round(1)


def add_daterange_buttons(figure_object):
    """Adds date range functionaity to any plot with date on x-axis."""
    figure_object.update_xaxes(
            rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=2, label="2m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        ))

def plot_dailyparameter(parameter, colour):

    if parameter == 'Daily Tests':
        columns = ['Newly tested', 'Daily Tests SMA7']
    elif parameter == 'Daily Cases':
        columns = ['New cases', 'Daily Cases SMA7']
    elif parameter == 'Daily Recoveries':
        columns = ['Newly recovered', 'Daily Recoveries SMA7']
    elif parameter == 'Daily Deaths':
        columns = ['New deaths', 'Daily Deaths SMA7']

    fig_daily.add_trace(go.Bar(x=df['Date'],
                               y=df[columns[0]],
                               name=parameter,
                               marker_color=colour,
                               hovertemplate=hoverform))

    fig_daily.add_trace(go.Scatter(x=df['Date'],
                                   y=df[columns[1]],
                                   name=f'{parameter}<br>(7-day rolling avg)',
                                   line=dict(color=colour, width=3),
                                   visible='legendonly',
                                   hovertemplate=hoverform))
    
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

df_districts_cv19_pop['Cases percent'] = calculate_percentage(df_districts_cv19_pop, 'Total Cases')

national_data = Path.cwd().joinpath('data', 'processed', 'national_data.csv')
df = pd.read_csv(national_data)
df.Date = pd.to_datetime(df.Date)

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

hoverform = "%{y:,.0f}"
hoverform_percent = "%{y:.1f} %"

latest_update = df.iloc[-1]['Date']

totalcases_regional = int(df_districts_cv19_pop['Total Cases'].sum())
totalcases_national = int(df['Total cases'].max())

colors = {'background': '#fafafa',
          'text': '#003366'}

fig_daily = go.Figure()
fig_daily_percent = go.Figure()

fig_daily_percent.add_trace(go.Bar(x=df['Date'], 
                           y=df['Positivity rate']*100,
                           name='Positivity rate',
                           marker_color='rgb(153, 102, 153)',
                           hovertemplate=hoverform_percent))
fig_daily_percent.add_trace(go.Scatter(x=df['Date'],
                            y=df['Positivity rate SMA7']*100,
                            name=f'Positivity rate<br>(7-day rolling avg)',
                            line=dict(color='rgb(153, 102, 153)', width=3),
                            hovertemplate=hoverform_percent))

fig_daily_percent.update_layout(
    legend_title_text='<b>Click to hide/show:</b><br>',
    barmode='overlay',
    hovermode='x unified',
    title='Daily Positivity Rate: (percentage of test results which are positive).',
    xaxis_title='Date',
    yaxis_title='Percent<br>(%)',
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    height=400)

   
add_daterange_buttons(fig_daily_percent)

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
    height=700,
    updatemenus=[
        dict(type="buttons",
            direction="left",
            active=0,
            x=0.7,
            y=1.2,
            buttons=list([
                dict(label="All",
                     method="update",
                     args=[{"visible": [True, True, True, True, True, True, True, True]},
                           {"title": "Daily Cases, Tests, Deaths and Recoveries"}]),
                dict(label="Tests",
                     method="update",
                     args=[{"visible": [True, True, False, False, False, False, False, False]},
                           {"title": "Tests"}]),
                dict(label="Cases",
                     method="update",
                     args=[{"visible": [False, False, True, True, False, False, False, False]},
                           {"title": "Cases"}]),
                dict(label="Recoveries",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, True, False, False]},
                           {"title": "Recoveries"}]),
                dict(label="Deaths",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, True, True]},
                           {"title": "Deaths"}]),
                dict(label="Bars Only",
                     method="update",
                     args=[{"visible": [True, False, True, False, True, False, True, False]},
                           {"title": "Daily Cases, Tests, Deaths and Recoveries"}]),
                 dict(label="Lines Only",
                     method="update",
                     args=[{"visible": [False, True, False, True, False, True, False, True]},
                           {"title": "Daily Cases, Tests, Deaths and Recoveries"}]),
                          ]),
            )
    ])

add_daterange_buttons(fig_daily)

lines = go.Figure()

plot_totalparameter('Total tested', 'rgb(49,130,189)')
plot_totalparameter('Total cases', 'green')
plot_totalparameter('Total recovered', 'rgb(235,186,20)')
plot_totalparameter('Total deaths', 'firebrick')

server = app.server

textual_content = TextualContent()
introduction = textual_content.introduction(latest_update)
daily_obs = textual_content.daily_data()
regional_obs = textual_content.regional_data(totalcases_regional, 
                                             totalcases_national)
credit = textual_content.page_credit()


center_text = {'textAlign': 'center', 'color': colors['text']}
left_text = {'textAlign': 'left', 'color': colors['text']}

app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
    html.H1("Bangladesh Covid-19 Data", style=center_text),
    html.Div([dcc.Markdown(children=introduction)], style=center_text), 
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-daily',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Daily Data',
                value='tab-daily',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Cumulative Data',
                value='tab-total',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Regional Data',
                value='tab-regional', className='custom-tab',
                selected_className='custom-tab--selected', 
            ),
        ]),
    html.Div(id='tabs-content-classes'),
    html.Div([dcc.Markdown(children=credit)], style=center_text)
])

#  Controls the tabs at the top
@app.callback(Output('tabs-content-classes', 'children'),
              [Input('tabs-with-classes', 'value')],)
def render_content(tab):
    if tab == 'tab-daily':
        return html.Div(style={'backgroundColor': colors['background']},
            children=[
            dcc.Graph(id='daily-data-graph', figure=fig_daily, style={'width':'90vw'}),
            dcc.Graph(id='daily-data-percent', figure=fig_daily_percent, style={'width':'90vw'}),
            html.Div([dcc.Markdown(children=daily_obs)], style=left_text),
        ])
    elif tab == 'tab-total':
        return html.Div(style={'backgroundColor': colors['background']},
            children=[
            dcc.RadioItems(
                    id='yaxis-scale',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}, 
                    style=center_text),
            dcc.Graph(id='total-data-graph', style={'width':'90vw'}),
                    ])
    elif tab == 'tab-regional':
        return html.Div(style={'backgroundColor': colors['background']},
            children=[
            dcc.Dropdown(id='regional-feature',
                        options=[{'label': i, 'value': j}
                                  for i, j in [('District: Confirmed Cases', 'Log(Cases)'),
                                              ('District: Cases Per Thousand', 'Cases Per Thousand')]],
                        value='Log(Cases)',
                        searchable=False, clearable=False,
                        style={'textAlign': 'center', 'color': colors['text'], 
                               'width': '60vw', 'margin-left': '10vw',
                              }),
            dcc.Graph(id='district-cases', style={'width':'90vw'}),
            html.Div([dcc.Markdown(children=regional_obs)], style=left_text),
        ])

#Create and update the cumulative national data plot
@app.callback(Output('total-data-graph', 'figure'),
              [Input('yaxis-scale', 'value')])
def update_graph(yaxis_type):
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
    add_daterange_buttons(lines)
    lines.update_yaxes(type='linear' if yaxis_type == 'Linear' else 'log') 
    return lines
    
#  Create and update the regional data visualisation map
@app.callback(Output('district-cases', 'figure'),
              [Input('regional-feature', 'value')])
def update_graph(propertytoplot):
    map_fig = px.choropleth_mapbox(df_districts_cv19_pop, geojson=df_districts_cv19_pop,
                            locations='District', color=propertytoplot,
                            hover_name='District',
                            hover_data={'Total Cases': True, 'Cases percent': True, 'Log(Cases)': False, 'District': False},
                            center={"lat": 23.7, "lon": 90.2},
                            featureidkey='properties.District',
                            mapbox_style="carto-positron",
                            zoom=6,
                            height=800,
                            opacity=0.65,
                            title=propertytoplot,
                            color_continuous_scale='OrRd',
                            range_color=[1, 5])
    map_fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])
    return map_fig


#app.run_server(debug=True, port=8092)
