# ################################# IMPORT PACKAGES ################################
import pandas as pd
from dash import Input, Output, callback, Dash, html, dcc, State,callback_context, no_update
import dash_cytoscape as cyto
from dash import callback_context
cyto.load_extra_layouts()
import json
from feature_table import feature_table
from dash.exceptions import PreventUpdate
from f_load_data import load_data
from f_colors import check_data_types,get_colors,get_colors2
import random

# Run this app to run only the website
app = Dash(__name__)

# ################################# MAKE COLORS ################################

colorlist=['#e9b497', '#01f55b', '#269d2b', '#12d16d', '#b06d68', '#a1c07e', '#40b244', '#dd1462', '#efc646', '#ea03b9', '#77f109', '#ed3176', '#cd0361', '#4c84f5', '#287b5e', '#c34fc8', '#0c8bcb', '#b0deaf', '#cf1e3b', '#08c99e', '#028b6e', '#1015c5', '#f16e26', '#1a71f0', '#5c3fd1', '#3b7a20', '#fdb152', '#ee93e4', '#cda688', '#6dd905', '#63acbc', '#5dc0d4', '#655a9d', '#e67844', '#23a032', '#fd7f1c', '#06dbd9', '#dd7755', '#af71ef', '#e1839a', '#3d1a49', '#bce2d5', '#2de0f2', '#5f1c73', '#4f13ef', '#61995d', '#ae49e5', '#fcb7b2', '#ac255a', '#b31585', '#84a814', '#5c82f1', '#c6d703', '#91421b', '#67bf2b', '#d190dc', '#47e918', '#83b0b2', '#d380c8', '#dd2f12', '#1c4b0b', '#d414d2', '#d937cd', '#82c78e', '#a1a8d9', '#2a75a8', '#8e2e14', '#2e408d', '#fd3251', '#b1c4d8', '#e78f09', '#5e3e9d', '#f1c0ca', '#b3a799', '#793aad', '#fe9a90', '#c24d85', '#b8c639', '#bdf1ad', '#81bda4', '#fac533', '#f3e076', '#3a6a27', '#58c6ad', '#e52f2f', '#7dbdbb', '#3fd4b3', '#2384c7', '#03cfa1', '#4482c0', '#c2e8b5', '#316d6b', '#f3e342', '#6471dc', '#8c9f6b', '#03a308', '#bd9a0d', '#2ba27a', '#c5b45a', '#e3b5e3', '#79d449', '#18ddc4', '#d62088', '#d9ca7f', '#feb296', '#76de2f', '#6c7199', '#2557c4', '#d9f5ee', '#dbf0e4', '#f69d32', '#6cbf8e', '#fa0cf1', '#69e196', '#95e46b', '#0e1e96', '#ccd891', '#7b9b4a', '#d80c3c', '#ead2e0', '#a4756f', '#25a085', '#a4bde0', '#f4cde1', '#3656d9', '#026ef5', '#0ee3aa', '#fbe3bc', '#e0dabf', '#2e20a2', '#caaf46', '#cc1595', '#4ee55d', '#0bf29c', '#bb09b9', '#5ab0b7', '#6d6711', '#632285', '#92fb8e', '#3b08c2', '#ec6a3a', '#a3e0cc', '#051c9b', '#ad3778', '#ad0845', '#b57679', '#517589', '#0e07a3', '#29a5af', '#9e9ad0', '#d9f706', '#b1ad4e', '#905b62', '#7db8b2', '#f2763c', '#f37ee7', '#f2564a', '#bdbe1a', '#efb1aa', '#f46c2b', '#037dff', '#e08bf7', '#5ca409', '#e1e30b', '#7c53dc', '#7b9f6c', '#df8f51', '#44cb7e', '#40fd5e', '#fca24b', '#f6f935', '#f6f271', '#1f0f4d', '#18d781', '#a101b1', '#6c5b9f', '#3dc3a1', '#bbf03f', '#aa9aeb', '#fd54d8', '#e7af70', '#7855b0', '#f8f90e', '#6aa236', '#7a7612', '#c23318', '#3cc79e', '#9b730e', '#9cf4ed', '#a43c17', '#d0a4f5', '#cf98d0', '#57919f', '#6cd0f0', '#bc538e', '#cf78f8', '#d0f7db', '#07fe4b', '#5ccaf7', '#b2817d', '#f2e3a9', '#7a90f2', '#88b1f7', '#558bdf', '#7e69f9', '#ee44e1', '#68f3e9', '#c0cd29', '#a64aee', '#f6d241', '#31750c', '#0d570d', '#1c17dc', '#ed5c0b', '#46c87b', '#91aaf9', '#671eac', '#808883', '#5f1084', '#f052ee', '#b03fa4', '#56c17e', '#204572', '#2c54da', '#96a5ec', '#90fbf2', '#c69aa0', '#ce562f', '#e3e472', '#e4a649', '#aa4e5d', '#d0832d', '#75480e', '#e1fb61', '#3e1850', '#dbf7e2', '#ad7e36', '#76ab9c', '#b9be1c', '#cab6f2', '#71f028', '#93e5c0', '#4be41f', '#f9b178', '#7be8dc', '#59e10c', '#8d9f8e', '#5dfc8c', '#e1ab07', '#d75cc3', '#0d2c59', '#cd49ee', '#5186e4', '#e76ed1', '#0ed3ff', '#bdf671', '#9f1464', '#8b3143', '#18f881', '#30569b', '#9ad0ab', '#dab8b9', '#81ecff', '#16b579', '#ff8ac8', '#e5d6d2', '#36428c', '#63749e', '#a7598b', '#1a62ec', '#8f4e99', '#f5e7cf', '#7ccf5a', '#d00f8a', '#82e42f', '#31d924', '#c7c593', '#8e24cd', '#a73d3b', '#4acfd7', '#e3467f', '#9ab8e9', '#5eaf40', '#6a7d7d', '#e91b28', '#a49d38', '#5d047d', '#2fafe6', '#d26aa5', '#3726ec', '#9d0d02', '#e57f1f', '#e21d36', '#c1febf', '#7584d5', '#e7fe5e', '#90a3f1', '#73f77f', '#e460bc', '#79d255', '#8aefeb', '#1a5a1c', '#15a623', '#fb650d', '#cff157', '#d9b6c2', '#d8b82c', '#2d1ad0', '#dcc07c', '#529da9', '#174b85', '#5d8ef0', '#f0be63', '#036f30', '#e9f7b4', '#7f3d26', '#d48db5', '#17b354', '#fdab86', '#032a2a', '#c4d876', '#04a28a', '#cf9f55', '#756e3b', '#f9e0e7', '#ea68bb', '#e2441c', '#8c64b4', '#c3615a', '#ef4f76', '#f929b5', '#4c6897', '#f3de6b', '#078160', '#2f2ee6', '#9e8657', '#14f47b', '#70e228', '#e40f94', '#0c88bc', '#fbf2f3', '#2d69dc', '#c31a2b', '#b8f64d', '#ed5e68', '#d91cd4', '#3febd0', '#63e0db', '#e18f3d', '#034089', '#cad6d1', '#fd5a4b', '#8a65f0', '#e14b0c', '#a1ee72', '#ac3a1d', '#a4cfc8', '#3c52c3', '#fd4dbf', '#bc3fe8', '#4b41c3', '#d28589', '#07f07f', '#4ab140', '#ff7911', '#8c2364', '#fb8cfb', '#4fcac4', '#2a36df', '#f6f67e', '#fd60f3', '#848cb5', '#6f6e7d', '#d953fc', '#c7d2fd', '#a70e36', '#2a6ce8', '#2bbed0', '#adcfdd', '#6742e7', '#f2f85a', '#88784b', '#15f539', '#fb4a81', '#01a7d5', '#c52017', '#41afac', '#e54d19', '#23ac43', '#d320a3', '#7841bc', '#08fd1a', '#22e4b5', '#1cd675', '#1d4cd5', '#d2d9c7', '#f9cda1', '#f4f3cc', '#7a4bc2', '#3eddd6']

# ################################# LOAD DATA ################################
people_to_people_df, grant_to_people_df,from_att_df,to_att_df=load_data()
data_types = check_data_types(from_att_df)
data_types2 = check_data_types(to_att_df)
first_key, first_value = next(iter(data_types.items()))
second_key, second_value = next(iter(data_types.items()))

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
    for node_key in ['from','to']:  # Process both 'from' and 'to' columns
        node_id = edge[node_key]

        if node_id not in nodes:
            nodes.add(node_id)
            node_data = {'id': str(node_id), 'label': str(node_id)}

            # Check if the node is in the people attributes table
            if node_id in from_att_df.index:
                size_node=from_att_df[from_att_df['Node']==node_id].reset_index(drop=True).loc[0,'Node_Size']
                node_attributes = from_att_df.loc[node_id].dropna().to_dict()
                node_data.update(node_attributes)
                node_data['type'] = "person"
                node_data['size'] = str(15+25*size_node) +'px'
                node_data['color'] ='FF0000'
                
            if node_id in to_att_df.index:
                size_node=to_att_df[to_att_df['Node']==node_id].reset_index(drop=True).loc[0,'Node_Size']
                node_attributes = to_att_df.loc[node_id].dropna().to_dict()
                node_data.update(node_attributes)
                node_data['type'] = "grant"
                node_data['size'] = str(15+25*size_node) +'px'
                node_data['color'] ='#0000FF'     

            cyto_nodes.append({'data': node_data})

    cyto_edges.append({
        'data': {
            'source': str(edge['from']),
            'target': str(edge['to'])
        }
    })
# Create an empty list to collect the filtered data
filtered_data = []
filtered_data2 = []

# Iterate over each dictionary in the list
for item in cyto_nodes:
    # Check if the color is either 'red' or 'blue'
    if item['data']['color'] in ['#0000FF']:
        # Append the dictionary to the filtered_data list
        filtered_data.append(item['data'])
    else:
        filtered_data2.append(item['data'])
        
# Create a DataFrame from the filtered data
to_df = pd.DataFrame(filtered_data)
from_df=pd.DataFrame(filtered_data2)

# Select the first key-value pair
default_elements = cyto_edges + cyto_nodes

# ############################## MAKE DEFAULT STYLESHEET #############################

default_stylesheet = [
    {
            'selector': f'node[type = "person"]',
            'style': {
                'background-color': 'FF0000',
                 "opacity": 0.55,
            'width': 'data(size)',
            'height': 'data(size)',
            "shape": 'ellipse',# Generate a unique random color for each node
            }
        },
    {
        "selector": f'node[type = "grant"]', 
        "style": {
            "opacity": 0.55,
            'width': 'data(size)',
            'height': 'data(size)',
            "shape": 'diamond',
            'background-color': '#0000FF'
        }
    },
    {
        "selector": "edge",
        "style": {
            "curve-style": "bezier", 
            'opacity': 0.2,
            'width': "2",
        }
    }
]
styles = {
    "json-output": {
        "overflow-y": "scroll",
        "overflow-x": "scroll",
        "height": "calc(90% - 25px)",
        "width": "350px",
        "border": "thin lightgrey solid",
    },
    "tab": {"height": "calc(98vh - 115px)"},
}

style_buttons = {"backgroundColor": "#f8f9fa",
        "border": "1px solid #dfe0e1",
        "borderRadius": "4px",
        "color": "#3c4043",
        "cursor": "pointer",
        "fontFamily": "alegreya sans, sans-serif",
        "fontSize": "14px",
        "height": "36px",
        "lineHeight": "27px",
        "minWidth": "54px",
        "padding": "0 16px",
        "textAlign": "center",
        "userSelect": "none",
        "-webkit-user-select": "none",
        "touchAction": "manipulation",
        "whiteSpace": "pre"}

style_tabs = {"backgroundColor": "#f8f9fa",
        "border": "1px solid #adaeaf",
        "borderRadius": "4px",
        "color": "#3c4043",
        "cursor": "pointer",
        "fontFamily": "alegreya sans, sans-serif",
        "fontSize": "14px",
        "lineHeight": "55px",
        "minWidth": "10px",
        "padding": "0 16px",
        "textAlign": "center",
        "userSelect": "none",
        "-webkit-user-select": "none",
        "touchAction": "manipulation",
        "whiteSpace": "pre",
        'width': 'auto'}

def collect_node_attributes():
    attributes = set()
    for node in cyto_nodes:
        attributes.update(node['data'].keys())
    # Exclude common keys like 'id' and 'label' that are not useful for filtering
    return list(attributes - {'id', 'label', 'Node_Size', 'size', 'type', 'color', 'Node', 'Connected nodes', 'size index', 'index'})

node_attributes = collect_node_attributes()

# ############################## APP LAYOUT #############################

app.layout = html.Div(
    style = {
        'display' : 'flex'
        },
    children =[
        dcc.Store(id='current-stylesheet', data=default_stylesheet),
        html.Div(
               className = "settings",
               children = [
                   dcc.Tabs(
                    id="tabs",
                    style = {"fontFamily": "alegreya sans, sans-serif",
                             'width': 'auto'},
                    children=[
                        dcc.Tab(
                            label="Layout",
                            style = style_tabs,
                            children=[
                                html.Div(
                                    children = [
                                        html.Button("Deselect Node", id="bt-undo", style = style_buttons),
                                        html.P("Graph layout:", style = {"fontFamily": "alegreya sans, sans-serif"}),
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
                                            style = {"fontFamily": "alegreya sans, sans-serif"} 
                                        ),
                                    ],
                                ),
                                html.Div( 
                                    children = [
                                        html.P("Node shape for persons:", style = {"fontFamily": "alegreya sans, sans-serif"} ),
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
                                            style = {"fontFamily": "alegreya sans, sans-serif"} 
                                        ),
                                        html.P("Node shape for grants:", style = {"fontFamily": "alegreya sans, sans-serif"}),
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
                                            style = {"fontFamily": "alegreya sans, sans-serif"} 
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
                                                "marginLeft": "3px",
                                                "fontFamily": "alegreya sans, sans-serif"
                                                }
                                            ),
                                        dcc.Input(
                                            id="input-source-color",
                                            type="text",
                                            value="#0074D9",
                                            style = {
                                                "color": "#0074D9",
                                                "fontFamily": "alegreya sans, sans-serif"
                                                }
                                        ),
                                    ],
                                    ),
                                html.Div(
                                    style = {"margin": "10px 0px"},
                                    children = [
                                        html.P(children = "Color of grants:", 
                                            style = {
                                                "marginLeft": "3px",
                                                "fontFamily": "alegreya sans, sans-serif"
                                                }
                                            ),
                                        dcc.Input(
                                            id="input-target-color",
                                            type="text",
                                            value="#FF4136",
                                            style = {
                                                "color": "#FF4136",
                                                "fontFamily": "alegreya sans, sans-serif"
                                                }
                                        ),
                                    ],
                                    ),
                                ],
                            ),
                        dcc.Tab(
                            label="Filters",
                            style = style_tabs,
                            children=[
                                html.Div(
                                    style = styles["tab"],
                                    children=[
                                        html.Button("Reset", id = "bt-reset", style = style_buttons,),
                                        html.Button("Deselect Node", id="bt-undo1", style = style_buttons),
                                        html.P(children = "Search for person or grant:", 
                                            style = {
                                                "marginLeft": "3px",
                                                "fontFamily": "alegreya sans, sans-serif"
                                                }
                                            ),
                                        dcc.Input(
                                            id="search-input",
                                            type="text",
                                            placeholder = "Type to search..."
                                        ),
                                        html.P(children = "Graph Color Filters:",
                                                style={
                                                    "marginLeft": "3px",
                                                    "fontWeight": "bold",
                                                    "fontFamily": "alegreya sans, sans-serif"
                                                    }
                                                ),
                                        html.P("Node filter for persons:" , style = {"fontFamily": "alegreya sans, sans-serif"}),
                                        dcc.Dropdown(
                                        id='color-dropdown',
                                        options=[
                                                                {
                                                                    'label': key,
                                                                    'value': key} for key,value in data_types.items()],
                                        value=None, # Default color selection
                                        style = {"fontFamily": "alegreya sans, sans-serif"} 
                                        ),
                                        html.P("Node filter for grants:", style = {"fontFamily": "alegreya sans, sans-serif"}),
                                        dcc.Dropdown(
                                        id='color-dropdown2',
                                        options=[
                                                                {
                                                                    'label': key,
                                                                    'value': key} for key,value in data_types2.items()],
                                        value=None ,  # Default color selection
                                        style = {"fontFamily": "alegreya sans, sans-serif"}
                                        ),
                                        html.P(children = "Graph Filters:",
                                                style={
                                                    "marginLeft": "3px",
                                                    "fontWeight": "bold",
                                                    "fontFamily": "alegreya sans, sans-serif"
                                                    }
                                                ),
                                        html.P(children = "Select Node Attribute:",
                                                style={
                                                    "marginLeft": "3px",
                                                    "fontFamily": "alegreya sans, sans-serif"
                                                    }
                                                ),
                                        dcc.Store(id = "filter-history-store"),
                                        html.Div(
                                            style = 
                                            styles['tab'],
                                            children= [
                                                html.Div([
                                                    dcc.Dropdown(
                                                        id='node-attribute-dropdown',
                                                            options= [
                                                                {
                                                                    'label': attr,
                                                                    'value': attr} for attr in node_attributes],
                                                                    
                                                            value = None,
                                                            style = {"fontFamily": "alegreya sans, sans-serif"} 
                                                    ),
                                        html.P(children = "Select Attribute value:",
                                                style={
                                                    "marginLeft": "3px",
                                                    "fontFamily": "alegreya sans, sans-serif"
                                                    }
                                                ),
                                                    dcc.Dropdown(id = "attribute-value-dropdown", style = {"fontFamily": "alegreya sans, sans-serif"} ),
                                                ]),
                                                html.Div(id = "filter-output",
                                                         style = {
                                                            'margin-top': '20px',
                                                            "fontFamily": "alegreya sans, sans-serif"
                                                        }),
                                        html.P("Information of Selected Nodes:", style = {"fontFamily": "alegreya sans, sans-serif"} ),
                                            html.Pre(
                                                id="selected-node-data-json-output-filter",
                                                style=styles["json-output"],
                                            )
                                            ]
                                        )
                                        ]
                                    ),
                                
                                ]
                            ),
                            dcc.Tab(
                                label="Remove Nodes",
                                style = style_tabs,
                                children=[
                                    html.Button("Remove Selected Node", id="remove-button", style = style_buttons,),
                                    html.Button("Reset", id = "bt-reset1", style = style_buttons),
                                    html.Div(
                                        style=styles["tab"],
                                        children=[
                                            html.P("Information of Selected Nodes:", style = {"fontFamily": "alegreya sans, sans-serif"} ),
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
            style={
                'display': 'flex',
                'flexDirection': 'row',  
                'alignItems': 'flex-start',  
                'width': '100%',            
            },
            children = [
                html.Div(style={
                        'position': 'absolute',
                        'top' : 0,
                        'right' : 0
                    },
                         children=[
                    html.P("Legend:", style = {"fontFamily": "alegreya sans, sans-serif"} ),
                    html.Legend(id='legend', style={'order': 1, 'marginRight' : ' 5px'}),
                    html.Legend(id='legend2',  style={'order': 2, 'marginRight' : ' 5px'}),   
                ]),
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

@callback([
    Output("cytoscape", "stylesheet"),
    Output("legend", "children"),
    Output("legend2", "children")],
    [
        Input("dropdown-node-shape-person", "value"),
        Input("dropdown-node-shape-grant", "value"),
        Input("input-source-color", "value"),
        Input("input-target-color", "value"),
        Input("search-input", "value"),
        Input("cytoscape", "tapNode"),
        Input('color-dropdown', 'value'),
        Input('color-dropdown2', 'value'),
        State("cytoscape", "selectedNodeData")
    ],   
)
def generate_stylesheet(person_shape, grant_shape, source_color, target_color, search_value, node, color_dropdown, color_dropdown2, selected_nodes):
    triggered_id = get_triggered_id()
    legend = []
    legend2 = []

    if ((color_dropdown) or (color_dropdown2)) and not node:
        new_stylesheet = []
        if color_dropdown:
            drop_down_type = data_types.get(color_dropdown)
            first_df = get_colors(from_df, color_dropdown, drop_down_type)
            new_stylesheet += [
                {
                    'selector': f'node[id="{row["id"]}"]',
                    'style': {
                    "opacity": 0.55,
                        'width': 'data(size)',
                        'height': 'data(size)',
                        "shape": person_shape,
                        'background-color': row['color'],  # Set a random color for each node of type "person"
                    }
                }
                for index, row in first_df.iterrows()  # Iterate over the values in the "ID" column of the DataFrame
            ]
            
            # Generate legend based on unique colors in 'first_df'
            unique_colors = first_df[[color_dropdown, 'color']].drop_duplicates().sort_values(by=color_dropdown)
            legend_items = [
                html.Li(f"{color_dropdown}: {filtered_column}", style={'color': color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"})
                for filtered_column, color in unique_colors.itertuples(index=False)]
            legend = html.Ul(legend_items)
        
        if color_dropdown2:
            
            drop_down_type2 = data_types2.get(color_dropdown2)
            second_df=get_colors2(to_df,color_dropdown2,drop_down_type2)
            new_stylesheet += [
                {
                    'selector': f'node[id="{row["id"]}"]',
                    'style': {
                    "opacity": 0.55,
                        'width': 'data(size)',
                        'height': 'data(size)',
                        "shape": grant_shape,
                        'background-color': row['color'],  # Set a random color for each node of type "person"
                    }
                }
                for index, row in second_df.iterrows()  # Iterate over the values in the "ID" column of the DataFrame
            ]
            
            # Generate legend based on unique colors in 'second_df'
            unique_colors2 = second_df[[color_dropdown2, 'color']].drop_duplicates().sort_values(by=color_dropdown2)
            legend_items2 = [
                html.Li(f"{color_dropdown2}: {filtered_column}", style={'color': color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"})
                for filtered_column, color in unique_colors2.itertuples(index=False)]
            legend2 = html.Ul(legend_items2)
        
        new_stylesheet += [
            {
                    "selector": "edge",
                    "style": {
                        "opacity": 0.2,
                        "curve-style": "bezier",
                    }}]
        
        return new_stylesheet, legend, legend2
    
    if triggered_id == "search-input":
        if search_value == None and selected_nodes == []:
            stylesheet = [
                {
                    "selector": 'node[type="person"]',
                    "style": {
                        "background-color": source_color,
                        "shape": person_shape,
                        "width": "data(size)",
                        "height": "data(size)",
                        "opacity": 0.55
                    }
                },
                {
                    "selector": 'node[type="grant"]',
                    "style": {
                        "background-color": target_color,
                        "shape": grant_shape,
                        "width": "data(size)",
                        "height": "data(size)",
                        "opacity": 0.55
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "curve-style": "bezier",
                        "opacity": 0.2,
                        "width": "2"
                    }
                }
                ]
            legend_items = [
                html.Li(f"Person", style={'color': source_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"}),
                html.Li(f"Grant", style={'color': target_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"})
                ]
            legend = html.Ul(legend_items)
            return stylesheet, legend, []
        elif not search_value:
            if not node:
                stylesheet = [
                        {
                            "selector": 'node[type="person"]',
                            "style": {
                                "background-color": source_color,
                                "shape": person_shape,
                                "width": "data(size)",
                                "height": "data(size)",
                                "opacity": 0.55
                            }
                        },
                        {
                            "selector": 'node[type="grant"]',
                            "style": {
                                "background-color": target_color,
                                "shape": grant_shape,
                                "width": "data(size)",
                                "height": "data(size)",
                                "opacity": 0.55
                            }
                        },
                        {
                            "selector": "edge",
                            "style": {
                                "curve-style": "bezier",
                                "opacity": 0.2,
                                "width": "2"
                            }
                        }
                    ]
                legend_items = [
                    html.Li(f"Person", style={'color': source_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"}),
                    html.Li(f"Grant", style={'color': target_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"})
                    ]
                legend = html.Ul(legend_items)
                return stylesheet, legend, []                
            stylesheet = [
                {
                    "selector": 'node[type = "person"]', 
                    "style": {
                        "opacity": 0.55,'width': 'data(size)',
                        'height': 'data(size)',
                        "shape": person_shape
                        }
                },
                {
                    "selector": 'node[type = "grant"]', 
                    "style": {
                        "opacity": 0.55,'width': 'data(size)',
                        'height': 'data(size)',
                        "shape": grant_shape
                        }
                },
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
                        
                        "text-opacity": 0.8,
                    "font-size": 12,
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
                                "line-color": source_color,
                                "opacity": 1,
                                "z-index": 5000
                            },
                        }
                    )
            legend_items = [
                html.Li(f"Person", style={'color': source_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"}),
                html.Li(f"Grant", style={'color': target_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"})
                ]
            legend = html.Ul(legend_items)
            return stylesheet, legend, []

        stylesheet_search_value = [
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
                    stylesheet_search_value.append({
                        "selector": f'node[id = "{connected_node_id}"]',
                        "style": {
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
                    stylesheet_search_value.append({
                        "selector": f'edge[source = "{search_value}"][target = "{connected_node_id}"], edge[target = "{search_value}"][source = "{connected_node_id}"]',
                        "style": {
                            "background-color": target_color,
                            "line-color" : target_color,
                            "opacity": 0.9,
                            "z-index": 5000
                        }
                    })
                else:
                    connected_node_id = edge['data']['source']
                    stylesheet_search_value.append({
                        "selector": f'node[id = "{connected_node_id}"]',
                        "style": {
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
                    stylesheet_search_value.append({
                        "selector": f'edge[source = "{search_value}"][target = "{connected_node_id}"], edge[target = "{search_value}"][source = "{connected_node_id}"]',
                        "style": {
                            "background-color": source_color,
                            "line-color" : source_color,
                            "opacity": 0.9,
                            "z-index": 5000
                        }
                    })
        legend_items = [
            html.Li(f"Person", style={'color': source_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"}),
            html.Li(f"Grant", style={'color': target_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"})
            ]
        legend = html.Ul(legend_items)
        return stylesheet_search_value, legend, []

    else:
        if not node:
            stylesheet = [
                        {
                            "selector": 'node[type="person"]',
                            "style": {
                                "background-color": source_color,
                                "shape": person_shape,
                                "width": "data(size)",
                                "height": "data(size)",
                                "opacity": 0.55
                            }
                        },
                        {
                            "selector": 'node[type="grant"]',
                            "style": {
                                "background-color": target_color,
                                "shape": grant_shape,
                                "width": "data(size)",
                                "height": "data(size)",
                                "opacity": 0.55
                            }
                        },
                        {
                            "selector": "edge",
                            "style": {
                                "curve-style": "bezier",
                                "opacity": 0.2,
                                "width": "2"
                            }
                        }
                    ]
            legend_items = [
                html.Li(f"Person", style={'color': source_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"}),
                html.Li(f"Grant", style={'color': target_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"})
                ]
            legend = html.Ul(legend_items)
            return stylesheet, legend, []
    
        stylesheet = [
            {
                "selector": 'node[type = "person"]', 
                "style": {
                   "opacity": 0.55,'width': 'data(size)',
                    'height': 'data(size)',
                    "shape": person_shape
                    }
            },
            {
                "selector": 'node[type = "grant"]', 
                "style": {
                    "opacity": 0.55,'width': 'data(size)',
                    'height': 'data(size)',
                    "shape": grant_shape
                    }
            },
            {
                "selector": "edge",
                "style": {
                    'opacity':0.2,
                    'width': "2",
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
                    'width': 'data(size)',
                    'height': 'data(size)',

                },
            },
        ]

        for edge in node["edgesData"]:
            if edge["source"] == node["data"]["id"]:
                stylesheet.append(
                    {
                        "selector": f'node[id = "{edge["target"]}"]',
                        "style": {"background-color": target_color,"label": "data(label)","text-opacity": 0.8,
                    "font-size": 12, "opacity": 0.9},
                    }
                )
                stylesheet.append(
                    {
                        "selector": f'edge[id= "{edge["id"]}"]',
                        "style": {
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
                            "label": "data(label)",
                            "text-opacity": 0.8,
                            "font-size": 12,
                            "opacity": 0.9,
                            "z-index": 9999,
                            'width': 'data(size)',
                            'height': 'data(size)',
                        },
                    }
                )
                stylesheet.append(
                    {
                        "selector": f'edge[id= "{edge["id"]}"]',
                        "style": {
                            "line-color": source_color,
                            "opacity": 1,
                            "z-index": 5000
                        },
                    }
                )
    legend_items = [
        html.Li(f"Person", style={'color': source_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"}),
        html.Li(f"Grant", style={'color': target_color, 'margin': '5px', "fontFamily": "alegreya sans, sans-serif"})
        ]
    legend = html.Ul(legend_items)
    return stylesheet, legend, []

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
        new_elements = [
            ele for ele in elements if ele["data"]["id"] not in ids_to_remove]
        return new_elements
    return elements

@callback(
    Output("cytoscape", "elements", allow_duplicate=True),
    Output("cytoscape", "stylesheet", allow_duplicate=True),
    Output("search-input", "value"),
    Output('filter-output', 'children', allow_duplicate=True),
    Output('filter-history-store', 'data', allow_duplicate=True),
    Output("color-dropdown", "value"),
    Output("color-dropdown2", "value"),
    Output("selected-node-data-json-output-filter", "children", allow_duplicate=True),
    Output("selected-node-data-json-output", "children", allow_duplicate=True),
   [ Input("dropdown-node-shape-person", "value"),
    Input("dropdown-node-shape-grant", "value"),
    Input("input-source-color", "value"),
    Input("input-target-color", "value"),
    Input("bt-reset", "n_clicks"), 
    Input("bt-reset1", "n_clicks")],
    prevent_initial_call = True
)
def reset_layout(person_shape, grant_shape, source_color, target_color, n_clicks_bt_reset, n_clicks_bt_reset1):
    if (n_clicks_bt_reset or n_clicks_bt_reset1):
        default_stylesheet = [
                    {
                        "selector": 'node[type="person"]',
                        "style": {
                            "background-color": source_color,
                            "shape": person_shape,
                            "width": "data(size)",
                            "height": "data(size)",
                            "opacity": 0.55
                        }
                    },
                    {
                        "selector": 'node[type="grant"]',
                        "style": {
                            "background-color": target_color,
                            "shape": grant_shape,
                            "width": "data(size)",
                            "height": "data(size)",
                            "opacity": 0.55
                        }
                    },
                    {
                        "selector": "edge",
                        "style": {
                            "curve-style": "bezier",
                            "opacity": 0.2,
                            "width": "2"
                        }
                    }
                ]
        return default_elements, default_stylesheet, None, None, [], None, None, None, None
    else:
        return no_update,no_update, no_update,no_update,no_update, no_update, no_update, no_update, no_update

@callback(
    Output("selected-node-data-json-output", "children", allow_duplicate=True),
    Input("cytoscape", "selectedNodeData"),
    prevent_initial_call = True
)
def displaySelectedNodeData(data):
    if data and data!=None:
        for i in range(len(data)):
            
            table1= feature_table(data,from_att_df,to_att_df,grant_to_people_df,i)
            if i==0:
                tables=[table1,]                                                                
            else:
                tables.extend([table1,])
        return tables
    raise PreventUpdate                                                                                                 

@callback(
    Output("selected-node-data-json-output-filter", "children", allow_duplicate=True),
    Input("cytoscape", "selectedNodeData"),
    prevent_initial_call = True
)
def displaySelectedNodeData(data):
    if data and data!=None:
        for i in range(len(data)):
            
            table1= feature_table(data,from_att_df,to_att_df,grant_to_people_df,i)
            if i==0:
                tables=[table1,]                                                                
            else:
                tables.extend([table1,])
        return tables
    raise PreventUpdate 


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

@callback(
    [
    Output("cytoscape", "selectedNodeData", allow_duplicate=True),
    Output("selected-node-data-json-output-filter", "children", allow_duplicate=True),
    Output("selected-node-data-json-output", "children", allow_duplicate=True),
    Output("cytoscape", "tapNode"),
    Output("color-dropdown2", "value", allow_duplicate=True),
    Output("color-dropdown", "value", allow_duplicate=True)],
    [
        Input("bt-undo", "n_clicks"),
        Input("bt-undo1", "n_clicks"),
        Input("color-dropdown2", "value"),
        Input("color-dropdown", "value"),    
    ], prevent_initial_call=True)
def reset_stylesheet_on_tap(nclicks, n_clicks1, color2, color1):
    if (nclicks or n_clicks1):
        return  None, None, None, None, color2, color1
    else:
        return  no_update, no_update, no_update, no_update, no_update, no_update
        

@app.callback(
    [
        Output("cytoscape", "stylesheet", allow_duplicate=True),
        Output("color-dropdown", "value", allow_duplicate=True),
        Output("color-dropdown2", "value", allow_duplicate=True),
    ],
    [
        Input("dropdown-node-shape-person", "value"),
        Input("dropdown-node-shape-grant", "value"),
        Input("input-source-color", "value"),
        Input("input-target-color", "value"),
        Input("color-dropdown", "value"),
        Input("color-dropdown2", "value"),
    ],
    prevent_initial_call=True
)
def reset_dropdowns(person_shape, grant_shape, source_color, target_color, dropdown_value1, dropdown_value2):
    default_stylesheet = [
            {
                "selector": 'node[type="person"]',
                "style": {
                    "background-color": source_color,
                    "shape": person_shape,
                    "width": "data(size)",
                    "height": "data(size)",
                    "opacity": 0.55
                }
            },
            {
                "selector": 'node[type="grant"]',
                "style": {
                    "background-color": target_color,
                    "shape": grant_shape,
                    "width": "data(size)",
                    "height": "data(size)",
                    "opacity": 0.55
                }
            },
            {
                "selector": "edge",
                "style": {
                    "curve-style": "bezier",
                    "opacity": 0.2,
                    "width": "2"
                }
            }
        ]
    if dropdown_value1 is None:
        return default_stylesheet, None, dropdown_value2
    elif dropdown_value2 is None:
         return default_stylesheet, dropdown_value1, None
    elif (dropdown_value1 is None) and (dropdown_value2 is None):
        return default_stylesheet, None, None
    else:
        return no_update, no_update, no_update

if __name__ == "__main__":
    app.run(debug=True, port=5003)

