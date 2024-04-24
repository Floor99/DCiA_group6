import pandas as pd
from dash import Input, Output, callback, Dash, html, dcc, State, no_update
import dash_cytoscape as cyto
from dash import callback_context
cyto.load_extra_layouts()
import json

# Run this app to run only the website
app = Dash(__name__)

# ################################# LOAD DATA ################################
grant_to_people_df = pd.read_csv('dcia/static/data/grants_to_people.csv')
people_to_people_df = pd.read_csv('dcia/static/data/people_to_people.csv')
people_att_table_df = pd.read_csv('dcia/static/data/people_att_table.csv', sep="\t")
people_att_table_df.set_index('Node', inplace = True)
to_att_df = pd.read_csv('dcia/static/data/grant_att_table.csv')
to_att_df.set_index('Node', inplace = True)

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

for index, edge in edge_data.iterrows():
    for node_key in ['from', 'to']:  # Process both 'from' and 'to' columns
        node_id = edge[node_key]


        if node_id not in nodes:
            nodes.add(node_id)
            node_data = {'id': str(node_id), 'label': str(node_id)}


            # Check if the node is in the people attributes table
            if node_id in people_att_table_df.index:
                node_attributes = people_att_table_df.loc[node_id].dropna().to_dict()
                node_data.update(node_attributes)
                node_data['type'] = "person"


            # Check if the node is in the grant attributes table
            elif node_id in to_att_df.index:
                node_attributes = to_att_df.loc[node_id].dropna().to_dict()
                node_data.update(node_attributes)
                node_data['type'] = "grant"

            cyto_nodes.append({'data': node_data})

    # Create edge
    cyto_edges.append({
        'data': {
            'source': str(edge['from']),
            'target': str(edge['to'])
        }
    })
  
default_elements = cyto_edges + cyto_nodes

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
    "json-output": {
        "overflow-y": "scroll",
        "height": "calc(50% - 25px)",
        "border": "thin lightgrey solid",
    },
    "tab": {"height": "calc(98vh - 115px)"},
}

# ############################## APP LAYOUT #############################

def collect_node_attributes():
    attributes = set()
    for node in cyto_nodes:
        attributes.update(node['data'].keys())
    # Exclude common keys like 'id' and 'label' that are not useful for filtering
    return list(attributes - {'id', 'label'})

node_attributes = collect_node_attributes()

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
                                        html.P("Node shape for persons:"),
                                        dcc.Dropdown(
                                            id="dropdown-node-shape-person",
                                            options=[
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
                                            value="ellipse", 
                                            clearable = False,
                                        ),
                                        html.P("Node shape for grants:"),
                                        dcc.Dropdown(
                                            id="dropdown-node-shape-grant",
                                            options=[
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
                                            value="diamond",
                                            clearable = False, 
                                        ),
                                        html.Div([
                                        dcc.Store(id='shape-store', 
                                                  data={'person_shape': 'ellipse', 'grant_shape': 'diamond'})])
                                        ],
                                ),
                                html.Div(
                                    style = {"margin": "10px 0px"},
                                    children = [
                                        html.P(children = "Color of persons:", 
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
                                        html.P(children = "Color of grants:", 
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
                                        html.Button("Reset", id = "bt-reset"),
                                        html.P(children = "Search for person or grant:", 
                                            style = {
                                                "marginLeft": "3px"
                                                }
                                            ),
                                        dcc.Input(
                                            id="search-input",
                                            type="text",
                                            placeholder = "Type to search..."
                                        ),
                                        dcc.Store(id = "filter-history-store"),
                                        html.Div(
                                            style = 
                                            styles['tab'],
                                            children= [
                                                html.Div([
                                                    html.Label('Select Node Attribute:'),
                                                    dcc.Dropdown(
                                                        id='node-attribute-dropdown',
                                                            options=[
                                                                {
                                                                    'label': attr,
                                                                    'value': attr} for attr in node_attributes],
                                                            value = None
                                                    ),
                                                    html.Label("Select Attribute Value:"),
                                                    dcc.Dropdown(id = "attribute-value-dropdown"),
                                                ]),
                                                html.Div(id = "filter-output",
                                                         style = {
                                                            'margin-top': '20px'
                                                        })
                                            ]
                                        )
                                        ]
                                    )
                                ]
                            ),
                            dcc.Tab(
                                label="Remove Nodes",
                                children=[
                                    html.Button("Remove Selected Node", id="remove-button"),
                                    html.Button("Reset", id = "bt-reset1"),
                                    html.Div(
                                        style=styles["tab"],
                                        children=[
                                            html.P("Node Data JSON:"),
                                            html.Pre(
                                                id="selected-node-data-json-output",
                                                style=styles["json-output"],
                                            ),
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
                    boxSelectionEnabled=True, 
                    userPanningEnabled=True
                )
            ],
        ),
    ]
)

def get_triggered_id():
    ctx = callback_context
    if not ctx.triggered:
        return None
    return ctx.triggered[0]['prop_id'].split('.')[0]


@callback(
    Output("cytoscape", "stylesheet"),
    [
        Input("dropdown-node-shape-person", "value"),
        Input("dropdown-node-shape-grant", "value"),
        Input("input-source-color", "value"),
        Input("input-target-color", "value"),
        Input("search-input", "value"),
        Input("cytoscape", "tapNode")
    ],   
)
def generate_stylesheet(person_shape, grant_shape, source_color, target_color, search_value, node):
    triggered_id = get_triggered_id()
    if triggered_id == "search-input":
        if not search_value:
            if not node:
                return default_stylesheet
    
            stylesheet = [
                {
                    "selector": 'node[type = "person"]', 
                    "style": {
                        "opacity": 0.9, 
                        "shape": person_shape
                        }
                },
                {
                    "selector": 'node[type = "grant"]', 
                    "style": {
                        "opacity": 0.9, 
                        "shape": grant_shape
                        }
                },
                {
                    "selector": "edge",
                    "style": {
                        "opacity": 0.9,
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
                            "style": {
                                "background-color": target_color, 
                                 "opacity": 0.9,
                                  "z-index": 9999},
                        }
                    )
                    stylesheet.append(
                        {
                            "selector": f'edge[id= "{edge["id"]}"]',
                            "style": {
                                # "mid-target-arrow-color": target_color,
                                # "mid-target-arrow-shape": "vee",
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
                                # "mid-target-arrow-color": source_color,
                                # "mid-target-arrow-shape": "vee",
                                "line-color": source_color,
                                "opacity": 1,
                                "z-index": 5000
                            },
                        }
                    ) 

        stylesheet = [
             {
            "selector": 'node[type = "person"]',
            "style": {
                "shape": person_shape,
                "opacity": 0.9,
                },
            },
            {
                "selector": 'node[type = "grant"]',
                "style": {
                    "shape": grant_shape,
                    "opacity": 0.9,
                },
            },
            {
                "selector": 'edge',
                "style": {
                    "opacity": 0.9, 
                    # "line-color": "bezier"
                }
            },
            {
                "selector": f'node[id *= "{search_value}"]', 
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
                    "z-index": 9999
                }
            }
        ]

        for edge in cyto_edges:
            if search_value in edge['data']['source'] or search_value in edge['data']['target']:
                if search_value in edge['data']['source']:
                    connected_node_id = edge['data']['target']
                # connected_node_id = edge['data']['target'] if search_value in edge['data']['source'] else edge['data']['source']
                    stylesheet.append({
                        "selector": f'node[id = "{connected_node_id}"]',
                        "style": {
                            # "mid-target-arrow-color": target_color,
                            "background-color": target_color,
                            "border-width": 2,
                            "border-color": target_color,
                            "opacity": 1,
                            "label": "data(label)",
                            "line-color": target_color,
                            "text-opacity": 1,
                            "font-size": 12,
                            "z-index": 9999
                        }
                    })
                    stylesheet.append({
                        "selector": f'edge[source = "{search_value}"][target = "{connected_node_id}"], edge[target = "{search_value}"][source = "{connected_node_id}"]',
                        "style": {
                            # "mid-target-arrow-color": source_color,
                            "background-color": target_color,
                            "line-color" : target_color,
                            "opacity": 0.9,
                            "z-index": 5000
                        }
                    })
                else:
                    connected_node_id = edge['data']['source']
                    stylesheet.append({
                        "selector": f'node[id = "{connected_node_id}"]',
                        "style": {
                            # "mid-target-arrow-color": source_color,
                            "background-color": source_color,
                            "border-width": 2,
                            "border-color": source_color,
                            "opacity": 1,
                            "label": "data(label)",
                            "line-color": source_color,
                            "text-opacity": 1,
                            "font-size": 12,
                            "z-index": 9999
                        }
                    })
                    stylesheet.append({
                        "selector": f'edge[source = "{search_value}"][target = "{connected_node_id}"], edge[target = "{search_value}"][source = "{connected_node_id}"]',
                        "style": {
                            # "mid-target-arrow-color": source_color,
                            "background-color": source_color,
                            "line-color" : source_color,
                            "opacity": 0.9,
                            "z-index": 5000
                        }
                    })

    else:
        if not node:
            return default_stylesheet
    
        stylesheet = [
            {
                "selector": 'node[type = "person"]', 
                "style": {
                    "opacity": 0.9, 
                    "shape": person_shape
                    }
            },
            {
                "selector": 'node[type = "grant"]', 
                "style": {
                    "opacity": 0.9, 
                    "shape": grant_shape
                    }
            },
            {
                "selector": "edge",
                "style": {
                    "opacity": 0.9,
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
                            # "mid-target-arrow-color": target_color,
                            # "mid-target-arrow-shape": "vee",
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
                            # "mid-target-arrow-color": source_color,
                            # "mid-target-arrow-shape": "vee",
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

@callback(
    Output("cytoscape", "elements", allow_duplicate=True),
    Input("remove-button", "n_clicks"),
    State("cytoscape", "elements"),
    State("cytoscape", "selectedNodeData"),
    prevent_initial_call=True
)
def remove_selected_nodes(_, elements, data):
    if elements and data:
        ids_to_remove = {ele_data["id"] for ele_data in data}
        print("Before:", elements)
        new_elements = [
            ele for ele in elements if ele["data"]["id"] not in ids_to_remove]
        print("After:", new_elements)
        return new_elements

    return elements

@callback(
    Output("cytoscape", "elements", allow_duplicate=True),
    Output("search-input", "value"),
    Output('filter-output', 'children', allow_duplicate=True),
   [Input("bt-reset", "n_clicks"), Input("bt-reset1", "n_clicks")],
    prevent_initial_call = True
)
def reset_layout(n_clicks_bt_reset, n_clicks_bt_reset1):
    return default_elements, "", ""

@callback(
    Output("selected-node-data-json-output", "children"),
    Input("cytoscape", "selectedNodeData"),
)
def displaySelectedNodeData(data):
    return json.dumps(data, indent=2)

@app.callback(
    Output('dropdown-node-shape-person', 'options'),
    Input('shape-store', 'data')
)
def update_person_options(data):
    grant_shape = data['grant_shape']
    available_shapes = [
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
    ]
    return [shape for shape in available_shapes if shape['value'] != grant_shape]

@app.callback(
    Output('dropdown-node-shape-grant', 'options'),
    Input('shape-store', 'data')
)
def update_grant_options(data):
    person_shape = data['person_shape']
    available_shapes = [
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
    ]
    return [shape for shape in available_shapes if shape['value'] != person_shape]

@app.callback(
    Output('shape-store', 'data'),
    Input('dropdown-node-shape-person', 'value'),
    Input('dropdown-node-shape-grant', 'value'),
    State('shape-store', 'data')
)
def update_store(person_shape, grant_shape, data):
    data['person_shape'] = person_shape
    data['grant_shape'] = grant_shape
    return data

@app.callback(
    Output('attribute-value-dropdown', 'options'),
    Input('node-attribute-dropdown', 'value'),
    State('cytoscape', 'elements')
)
def update_attribute_values(selected_attribute, elements):
    if not selected_attribute:
        return []  # Return an empty list of options if no attribute is selected
   
    unique_values = set()
    for element in elements:
        if 'source' not in element['data'] and selected_attribute in element['data']:
            unique_values.add(element['data'][selected_attribute])
   
    return [{'label': value, 'value': value} for value in unique_values]

@app.callback(
    [
        Output('cytoscape', 'elements'),
        Output('filter-output', 'children'),
        Output('node-attribute-dropdown', 'value'),
        Output('attribute-value-dropdown', 'value'),
        Output('filter-history-store', 'data')
    ],
    [
        Input('attribute-value-dropdown', 'value'),
        Input('node-attribute-dropdown', 'value')
    ],
    [
        State('cytoscape', 'elements'),
        State('filter-history-store', 'data')
    ]
)
def filter_nodes_by_attribute(selected_value, selected_attribute, elements, filter_history):
    if not selected_value or not selected_attribute:
        return no_update, no_update, no_update, no_update, no_update


    # Identify nodes that match the selected attribute and value
    matching_nodes = {
        el['data']['id'] for el in elements
        if 'source' not in el['data'] and el['data'].get(selected_attribute) == selected_value
    }


    # Include all nodes that are connected to the matching nodes
    connected_nodes = set()
    for el in elements:
        if 'source' in el['data']:
            if el['data']['source'] in matching_nodes or el['data']['target'] in matching_nodes:
                connected_nodes.update([el['data']['source'], el['data']['target']])
   
    filtered_elements = [
        el for el in elements
        if 'source' not in el['data'] and el['data']['id'] in connected_nodes
        or 'source' in el['data'] and (el['data']['source'] in connected_nodes or el['data']['target'] in connected_nodes)
    ]


    # Update filter history
    if filter_history is None:
        filter_history = []
    new_filter = f"{selected_attribute} = {selected_value}"
    filter_history.append(new_filter)
    filter_description = "Filters applied: " + "; ".join(filter_history)


    # Reset dropdowns and update store
    return filtered_elements, filter_description, None, None, filter_history

if __name__ == "__main__":
    app.run(debug=True, port=5003)

