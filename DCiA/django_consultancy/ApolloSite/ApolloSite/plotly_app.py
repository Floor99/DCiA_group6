# ApolloSite/visualization.py
import dash
from dash import html, dcc  # Add dcc import
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
from django_plotly_dash import DjangoDash



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash("Network", external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H2("Example Dash Network Visualization", style={'font-size': '15px'}),
    dcc.Location(id = 'url', refresh = False),
    html.Div(id='page-content', style= {'width': '1vw', 'height': '1vh'}),
    cyto.Cytoscape(
        id='cytoscape',
        layout={'name': 'circle'}, style = {'width': '100vw', 'height': '100vh'},
        #style={'width': '100%', 'height': '350px'},
        elements=[
            {'data': {'id': 'A', 'label': 'Node A'}},
            {'data': {'id': 'B', 'label': 'Node B'}},
            {'data': {'id': 'C', 'label': 'Node C'}},
            {'data': {'source': 'A', 'target': 'B'}},
            {'data': {'source': 'B', 'target': 'C'}}
        ]
    )
])
@app.callback(
Output('cytoscape', 'elements'),
[Input('url', 'pathname')]
)

def update_elements(pathname):
    # Here you can put your logic to update the elements based on the pathname or any other input property
    updated_elements = [
        {'data': {'id': 'A', 'label': 'Node A'}},
        {'data': {'id': 'B', 'label': 'Node B'}},
        {'data': {'id': 'C', 'label': 'Node C'}},
        {'data': {'source': 'A', 'target': 'B'}},
        {'data': {'source': 'B', 'target': 'C'}}
    ]
    return updated_elements