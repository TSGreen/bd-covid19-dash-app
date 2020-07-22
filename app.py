import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# Load Data
df = px.data.tips()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Build App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#111111',
    'text': '#7FDBFF'}

fig = px.scatter(df, x="total_bill", y="tip",
                 size='size')

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, children=[
    html.H1("Testing Dash Demo",
            style={
            'textAlign': 'center',
            'color': colors['text']}),
    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(id='testing_graph', figure=fig)
#     html.Label([
#         "colorscale",
#         dcc.Dropdown(
#             id='colorscale-dropdown', clearable=False,
#             value='plasma', options=[
#                 {'label': c, 'value': c}
#                 for c in px.colors.named_colorscales()
#             ])
    #]),
])

# Run app and display result inline in the notebook
app.run_server(debug=True)
