import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash
import geopandas as gpd

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


# Build App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#fafafa',
    'text': '#003366'}

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
                           hover_data={'Cases Per Thousand':True, 'Total Cases':True, 'Population (Millions)':True, 'Log(Cases)':False, 'District':False} ,
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
1. Map of [confirmed cases per district.](#district-cases)
2. Map of [confirmed cases per thousdand people.](#district-cases_pt)
'''

introduction = '''
An interactive exploration of Covid-19 data for Bangladesh.

Data source: [IEDCR](https://iedcr.gov.bd/).
Data on this page last updated: 12 August 2020.
'''

top = '''
[(top)](#top)'''

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, children=[
    html.H1("Bangladesh Covid-19 Data",
            style={
            'textAlign': 'center',
            'color': colors['text']}),
    html.Div([dcc.Markdown(children=introduction)], 
             style={
        'textAlign': 'center',
        #'font_size': '20vw',
        'color': colors['text']
    }),
    html.Div(children=[dcc.Markdown(children=table_contents)], id='top', style={
        'textAlign': 'left',
        'color': colors['text']
    }),
    
        
    dcc.Graph(id='district-cases', figure=fig, style={'width':'90vw'}),
    html.Div([dcc.Markdown(children=top)]),
        
    dcc.Graph(id='district-cases_pt', figure=fig_density, style={'width':'90vw'}),
    html.Div([dcc.Markdown(children=top)]),       
])

#app.run_server(debug=True)
