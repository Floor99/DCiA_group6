import dash
from dash import Input, Output, State, dcc, html
import dash_cytoscape as cyto
from  f_dash_components  import DropdownOptionsList,NamedRadioItems
from f_feature_table import current_node_attributes_table
from f_load_data import load_data
from dash.exceptions import PreventUpdate
from dash import callback_context as ctx
# Load extra layouts for Cytoscape
cyto.load_extra_layouts()

# Initialize the Dash app (assuming asset_path is defined or not needed)
app = dash.Dash(__name__, external_stylesheets= [
    "https://fonts.googleapis.com/css?family=Alegreya+Sans:300"
], assets_folder="./static/assets")

app.css.config.serve_locally = True

# ################################# LOAD DATA ################################
people_to_people_df, grant_to_people_df,from_att_df,to_att_df = load_data()

# ############################## PREPROCESS DATA #############################
# Drop druplicates
edge_data = people_to_people_df.drop_duplicates(keep="first").reset_index(drop=True)
# Remove self-edges(edges where the source and target nodes are the same)
edge_data = edge_data[edge_data['from'] != edge_data['to']].reset_index(drop=True)

edges = edge_data.copy()
nodes = set()

########################### Deze Code is voor nu niet nodig #######################################
# # Data looks like this
# # From          To 
# # People        Grant
# # Source        Target

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
    
########################### Stylesheet ##########################################################

# Define the cytoscape stylesheet
styles = {
    "json-output": {
        "overflow-y": "scroll",
        "height": "calc(50% - 25px)",
        "border": "thin lightgrey solid",
    },
    "tab": {"height": "calc(98vh - 80px)"},
    "cytoscape" : {
                "minWidth": "100%",
                "height": "95vh"
            },
    "P": {"fontFamily": "alegreya sans, sans-serif", "color": "grey", "fontSize": "14px"}
}

################################# global variable ####################################
# Initialize a counter to keep track of the number of expansions
expansion_counter:int = 0

########################### Functions ###################################################################
# Initialize global data structures for node expansion (followers and following)
def populate_relationships(edges: list):
    """This function creates and populates dictionaries for an undirected network representing nodes and edges in the graph."""
    node_di = {}
    edges_di = {}

    # Iterate through each edge to populate dictionaries
    for index, edge in edges.iterrows():
        source = edge['from']
        target = edge['to']

        # Populate edges for source node
        if source not in edges_di:
            edges_di[source] = []
        edges_di[source].append({
            "data": {
                "id": str(source + target),
                "source": str(source),
                "target": str(target)
            }
        })

        # Populate edges for target node
        if target not in edges_di:
            edges_di[target] = []
        edges_di[target].append({
            "data": {
                "id": str(source + target),
                "source": str(source),
                "target": str(target)
            }
        })

    # Now populate the node list on the source or target list, which is not the node in the loop.
    for node, edges in edges_di.items():
        # Add the node itself with its data
        node_di[node] = [{'data': {'id': str(node), 'label': str(node)}}]
        # Add all the nodes that are connected to the node in question
        for edge in edges:
            if str(node) != edge['data']['source']:
                node_di[node].append({'data': {'id': str(edge['data']['source']), 'label': str(edge['data']['source'])}})
            if str(node) != edge['data']['target']:
                node_di[node].append({'data': {'id': str(edge['data']['target']), 'label': str(edge['data']['target'])}})
        
    return node_di, edges_di

######################################## Initiate functions ####################################################
nodes_di, edges_di = populate_relationships(edges)


default_elements = []

################################### Dash Components #######################################################
# Define the app layout, integrating the control panel and cytoscape component
control_panel = dcc.Tab(
    label="Control Panel",
    children=[
        html.P("Graph layout", style = {"fontFamily": "alegreya sans, sans-serif", "fontWeight": "bold"}),
        html.P("You can also change the layout of the network to see the people spread out in a different way.",
               style=styles["P"]),
        dcc.Dropdown(
            id = "dropdown-layout",
            options = [
                # {'label': 'Breadth-first', 'value': 'breadthfirst'},
                # {'label': 'Circle', 'value': 'circle'},
                # {'label': 'Concentric', 'value': 'concentric'},
                {'label': 'Default (Cose-bilkent)', 'value': 'cose-bilkent'},
                {'label': 'Grid', 'value': 'grid'},
                {'label': 'Random', 'value': 'random'},
                {'label': 'cola','value': 'cola'}
                ],
            value = "cose-bilkent",
            clearable = False,
            style = {"fontFamily": "alegreya sans, sans-serif"}
        ),
        html.Br(),
            dcc.Input(
                id="search-input",
                type="text",
                placeholder = "Type to search..."
            ),
        html.Br(),
            NamedRadioItems(
                name="Expand",
                id = "radio-expand",
                options = DropdownOptionsList(
                    "expanding","not expanding"
                ),
                value = "not expanding"
            )
    ],
)
json_panel = dcc.Tab(
    label="Information",
    children=[
        html.Div(
            #style=styles["tab"],
            children=[
                html.P("Information of Selected Node:",style = {"fontFamily": "alegreya sans, sans-serif", "fontWeight": "bold"} ),
                html.Pre(
                    id="selected-node-data-json-output",
                    style=styles["json-output"],
                )
            ]
        )
    ]
)
# Cytoscape network visualization component
cytoscape_panel = html.Div(
    style= {
        "minWidth" : "75%"
    },
    children=
    [
        cyto.Cytoscape(
            style= styles["cytoscape"],
            id="cytoscape",
            elements=default_elements,  
            stylesheet=[
                # Default stylesheet
                {
                    "selector": "node",
                    "style": {
                        "opacity": 0.65,
                        "label" : "data(label)",
                        'font-size': '12px'
                        
                    }
                },
                {
                    "selector": "edge", 
                    "style": {
                        "curve-style": "bezier", 
                        "opacity": 0.65,
                        "width" : 2
                    }
                },
            ]
        )
    ])

app.layout = html.Div(
    [ html.Link(
        rel='stylesheet',
        href='https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/cosmo/bootstrap.min.css'
    ),
        # Control panel and JSON output components
        html.Div(
            children=[
                dcc.Tabs(
                    id="tabs",
                    children=[
                        control_panel,
                        json_panel
                    ],
                ),
            ],
            style= {
                "minWidth" : "25%"
            }
        ),
        cytoscape_panel
    ],
    style=
    {
        "display": "flex",
        "flexDirection": "row",
        "width": "100%"
    },
)

                

# Define callbacks for interactive features (node/edge taps, layout changes, etc.)
# Include callbacks for updating the layout, displaying JSON data, and expanding nodes
############################### Callbacks ################################################################
@app.callback(
    Output("cytoscape", "elements",allow_duplicate=True),
    Input("cytoscape", "tapNode"),
    State("cytoscape", "elements"),
    State("radio-expand","value"),
    prevent_initial_call=True
)
def generate_elements(nodeData: dict, elements: dict,expansion_mode:str) -> dict:
    """
    Expands with all connections to the selected node. 
    :param dict nodeData: nodedata contains: (expanded: bool), (class: string) and (data: dict) with (id: string), (label: string)
    :param dict elements: all elements returned from cytoscape.
    :param str expansion_mode: gives the value from the radio_button

    Returns dict elements: all new elements are returned to cytoscape
    """
    # Initiate the global variable to keep track of the expansions
    global expansion_counter

    # If the button is on not expanding and the user clicks; no further action is necessary
    if expansion_mode == "not expanding":
        return elements


    # Node has already been expanded or there is no NodeData; no further action is necessary.
    if not nodeData or nodeData["data"].get("expanded"):
        return elements 
    
    # If the expansion counter exceeds 4, prevent further expansion
    if expansion_counter > 4:
        raise PreventUpdate
    
    # Mark the node as expanded to prevent re-expansion.
    for element in elements:

        if nodeData["data"]["id"] == element.get("data", {}).get("id"):
            element["data"]["expanded"] = True
            break

    # Add follower nodes and edges. 
    followers_nodes = nodes_di.get(int(nodeData["data"]["id"]))
    followers_edges = edges_di.get(int(nodeData["data"]["id"]))
    if followers_nodes:
        for node in followers_nodes:
            node["classes"] = "followerNode"
        elements.extend(followers_nodes)
    
        if followers_edges:
            for follower_edge in followers_edges:
                follower_edge["classes"] = "followerEdge"
            elements.extend(followers_edges)
    
    # Increment the expansion counter
    expansion_counter += 1

    return elements

@app.callback(
    Output("cytoscape", "elements",allow_duplicate=True), 
    Input("search-input", "value"),
    Input("search-input","n_submit"),
    prevent_initial_call=True
)
def update_graph(search_value: str,n_submit: int):
    # Check if the callback was triggered by pressing Enter
    if not ctx.triggered or ctx.triggered[0]['prop_id'] != 'search-input.n_submit':
        # Callback was not triggered by pressing Enter, return empty elements
        return []
    
    if not search_value:
        return []
    
    filtered_data_edges = []
    filtered_data_nodes = set()
    new_nodes = []

    for edge in edges_di[int(search_value)]:
        if edge['data']['source'] == search_value or edge['data']['target'] == search_value:
            filtered_data_edges.append(edge)
            filtered_data_nodes.update([edge['data']['source'], edge['data']['target']])
    
    for node in nodes_di[int(search_value)]:
        
        if node['data']['id'] in filtered_data_nodes:
            new_nodes.append(node)


    return filtered_data_edges + new_nodes

@app.callback(
    Output("selected-node-data-json-output", "children", allow_duplicate=True),
    Input("cytoscape", "selectedNodeData"),
    prevent_initial_call = True
)
def displaySelectedNodeData(data):
    if data and data!=None:
        for i in range(len(data)):

            table1= current_node_attributes_table(data,from_att_df,to_att_df,people_to_people_df,i)
            if i==0:
                tables=[table1,]
            else:
                tables.extend([table1,])
        return tables
    raise PreventUpdate
@app.callback(
    Output("cytoscape", "layout"),
    [Input("dropdown-layout", "value")])
def update_layout(layout_value):
    return {"name": layout_value}


if __name__ == "__main__":
    app.run_server(debug=True,port = 5002)

