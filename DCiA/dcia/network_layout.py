import pandas as pd
from dash import Input, Output, callback, Dash, html, dcc
import dash_cytoscape as cyto
cyto.load_extra_layouts()

# Run this app to run only the website
app = Dash(__name__)

# ################################# LOAD DATA ################################
grant_to_people_df = pd.read_csv('dcia/static/network_visualisations/grants_to_people.csv')

# ############################## PREPROCESS DATA #############################
# Drop druplicates
edge_data = grant_to_people_df.drop_duplicates(keep="first").reset_index(drop=True)
# Remove self-edges(edges where the source and target nodes are the same)
edge_data = edge_data[edge_data['from'] != edge_data['to']].reset_index(drop=True)

edges = edge_data.copy()
nodes = set()

# Data looks like this
# From          To 
# People        Grant
# Source        Target

cyto_edges = []
cyto_nodes = []

for index, edge in edges.iterrows():
    source, target = edge['from'], edge['to']

    if source not in nodes:
        nodes.add(source)
        cyto_nodes.append({
            "data": {
                "id": str(source), 
                "label": str(source)
            }
        })
    if target not in nodes:
        nodes.add(target)
        cyto_nodes.append({
            "data": {
                "id": str(target), 
                "label": str(target)
            }
        })
        
    cyto_edges.append({
        "data": {
            "source": str(source), 
            "target": str(target)
            }
        })
  
# ############################## MAKE DEFAULT STYLESHEET #############################
    
default_stylesheet = [
    {
        "selector": "node",
        "style": {
            "opacity": 0.65
        },
    },
    {
        "selector": "edge", 
        "style": {
            "curve-style": "bezier", 
            "opacity": 0.65
        }
    }
]

styles = {
    "tab": {"height": "calc(98vh - 105px)"},
}

# ############################## APP LAYOUT #############################

app.layout = html.Div(
    style = {
        'display' : 'flex'
        },
    children =[
        html.Div(
               className = "settings",
               children = [
                   dcc.Tabs(
                    id="tabs",
                    children=[
                        dcc.Tab(
                            label="Layout",
                            children=[
                                html.Div( 
                                    children = [
                                        html.P(children = "Graph layout:", 
                                                style={
                                                    "marginLeft": "3px"
                                                    }
                                                ),
                                        dcc.Dropdown(
                                            id = "dropdown-layout",
                                            options = [
                                                {'label': 'Breadth-first', 'value': 'breadthfirst'},
                                                {'label': 'Circle', 'value': 'circle'},
                                                {'label': 'Concentric', 'value': 'concentric'},
                                                #{'label': 'Cose', 'value': 'cose'},
                                                {'label': 'Cose-bilkent', 'value': 'cose-bilkent'},
                                                {'label': 'Grid', 'value': 'grid'},
                                                {'label': 'Random', 'value': 'random'}
                                                ],
                                            value = "cose-bilkent",
                                            clearable = False,
                                        ),
                                    ],
                                ),
                                html.Div( 
                                    children = [
                                        html.P(children = "Node shape:", 
                                                style={
                                                    "marginLeft": "3px"
                                                    }
                                                ),
                                        dcc.Dropdown(
                                            id = "dropdown-node-shape",
                                            options = [
                                                {'label': 'Diamond', 'value': 'diamond'},
                                                {'label': 'Ellipse', 'value': 'ellipse'},
                                                {'label': 'Heptagon', 'value': 'heptagon'},
                                                {'label': 'Hexagon', 'value': 'hexagon'},
                                                {'label': 'Octagon', 'value': 'octagon'},
                                                {'label': 'Pentagon', 'value': 'pentagon'},
                                                {'label': 'Polygon', 'value': 'polygon'},
                                                {'label': 'Rectangle', 'value': 'rectangle'},
                                                {'label': 'Star', 'value': 'star'},
                                                {'label': 'Triangle', 'value': 'triangle'}
                                                ],
                                            value = "ellipse",
                                            clearable = False,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    style = {"margin": "10px 0px"},
                                    children = [
                                        html.P(children = "Color of persons linked to grant:", 
                                            style ={
                                                "marginLeft": "3px"
                                                }
                                            ),
                                        dcc.Input(
                                            id="input-source-color",
                                            type="text",
                                            value="#0074D9",
                                            style = {
                                                "color": "#0074D9"
                                                }
                                        ),
                                    ],
                                    ),
                                html.Div(
                                    style = {"margin": "10px 0px"},
                                    children = [
                                        html.P(children = "Color of grants linked to person:", 
                                            style = {
                                                "marginLeft": "3px"
                                                }
                                            ),
                                        dcc.Input(
                                            id="input-target-color",
                                            type="text",
                                            value="#FF4136",
                                            style = {
                                                "color": "#FF4136"
                                                }
                                        ),
                                    ],
                                    ),       
                                ],
                            ),
                        dcc.Tab(
                            label="Filters",
                            children=[
                                html.Div(
                                    style = styles["tab"],
                                    children=[
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
          html.Div(
            className = "graph",
            style = {'display' : 'contents'},
            children = [
                cyto.Cytoscape(
                    id = "cytoscape",
                    elements = cyto_edges + cyto_nodes,
                    stylesheet = default_stylesheet,
                    style = {
                        "height": "95vh",
                        "width": "80%"
                    },
                    layout = {
                        "name": "cose-bilkent",
                        },
                )
            ],
        ),
    ]
)                        


@callback(
    Output("cytoscape", "stylesheet"),
    [
        Input("cytoscape", "tapNode"),
        Input("input-source-color", "value"),
        Input("input-target-color", "value"),
        Input("dropdown-node-shape", "value"),
    ],
)
def generate_stylesheet(node, source_color, target_color, node_shape):
    if not node:
        return default_stylesheet
    
    stylesheet = [
        {"selector": "node", "style": {"opacity": 0.3, "shape": node_shape}},
        {
            "selector": "edge",
            "style": {
                "opacity": 0.2,
                "curve-style": "bezier",
            },
        },
        {
            "selector": f'node[id = "{node["data"]["id"]}"]',
            "style": {
                "background-color": "#B10DC9",
                "border-color": "purple",
                "border-width": 2,
                "border-opacity": 1,
                "opacity": 1,
                "label": "data(label)",
                "color": "#B10DC9",
                "text-opacity": 1,
                "font-size": 12,
                "z-index": 9999,
            },
        },
    ]

    for edge in node["edgesData"]:
        if edge["source"] == node["data"]["id"]:
            stylesheet.append(
                {
                    "selector": f'node[id = "{edge["target"]}"]',
                    "style": {"background-color": target_color, "opacity": 0.9},
                }
            )
            stylesheet.append(
                {
                    "selector": f'edge[id= "{edge["id"]}"]',
                    "style": {
                        "mid-target-arrow-color": target_color,
                        "mid-target-arrow-shape": "vee",
                        "line-color": target_color,
                        "opacity": 0.9,
                        "z-index": 5000,
                    },
                }
            )

        if edge["target"] == node["data"]["id"]:
            stylesheet.append(
                {
                    "selector": f'node[id = "{edge["source"]}"]',
                    "style": {
                        "background-color": source_color,
                        "opacity": 0.9,
                        "z-index": 9999,
                    },
                }
            )
            stylesheet.append(
                {
                    "selector": f'edge[id= "{edge["id"]}"]',
                    "style": {
                        "mid-target-arrow-color": source_color,
                        "mid-target-arrow-shape": "vee",
                        "line-color": source_color,
                        "opacity": 1,
                        "z-index": 5000
                    },
                }
            )

    return stylesheet

@app.callback(
    Output("input-source-color", "style"), Input("input-source-color", "value"))
@app.callback(
    Output("input-target-color", "style"),  Input("input-target-color", "value"))
def update_input_color(input_value):
    return {"color": input_value}

@callback(Output("cytoscape", "layout"), Input("dropdown-layout", "value"))
def update_cytoscape_layout(layout):
    return {"name": layout}

if __name__ == "__main__":
    app.run(debug=True, port=5001)
