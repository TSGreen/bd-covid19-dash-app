import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash
import geopandas as gpd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df_districts_cv19_pop = gpd.read_file('./data/data.shp')
df_districts_cv19_pop.rename(columns = dict(zip(df_districts_cv19_pop.columns, ['Shape_Length', 'Shape_Area', 'District', 'ADM2_PCODE', 'ADM2_REF',
       'ADM2ALT1EN', 'ADM2ALT2EN', 'ADM1_EN', 'ADM1_PCODE', 'ADM0_EN',
       'ADM0_PCODE', 'date', 'validOn', 'ValidTo', 'Division', 'Total Cases',
       'Log(Cases)', 'Abbr.', 'Status', 'Native', 'Adm.', 'Area', 'Population_1991',
       'Population_2001', 'Population_2011', 'Population_2016', 'Cases Per Thousand', 'geometry'])), inplace=True)
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
                          height=800, width=650,
                           opacity=0.7,
                          title='Confirmed cases per district',
                          color_continuous_scale='OrRd',
                          range_color=[1,5])

fig_density = px.choropleth_mapbox(df_districts_cv19_pop, geojson=df_districts_cv19_pop,
                           locations='District', color='Cases Per Thousand',
                           hover_name='District',
                           hover_data={'Cases Per Thousand':True, 'Total Cases':True, 'Population_2016':True, 'Log(Cases)':False, 'District':False} ,
                           center={"lat": 23.7, "lon": 90.2},
                           featureidkey='properties.District',
                           mapbox_style="carto-positron", 
                           zoom=6,
                          height=800, width=650,
                           opacity=0.7,
                          title='Confirmed cases per thousdand people per district',
                          color_continuous_scale='OrRd',
                          range_color=[0,4])

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])

fig_density.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])

server = app.server

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, children=[
    html.H1("Bangladesh Covid-19 Data",
            style={
            'textAlign': 'center',
            'color': colors['text']}),
    html.Div(children='An interactive exploration of Covid-19 data for Bangladesh. Hover over a district to see number of confirmed cases. (Data true as of July 18, 2020.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(id='district-cases', figure=fig),
    dcc.Graph(id='district-cases_pt', figure=fig_density)
])

#app.run_server(debug=True)
