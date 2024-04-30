import json
import pandas as pd
import dash
from dash import Input, Output, State, dcc, html
import dash_cytoscape as cyto
from  f_dash_components  import NamedDropdown, DropdownOptionsList,NamedRadioItems

# Load extra layouts for Cytoscape
cyto.load_extra_layouts()

# Initialize the Dash app (assuming asset_path is defined or not needed)
app = dash.Dash(__name__, external_stylesheets= [
    "https://fonts.googleapis.com/css?family=Alegreya+Sans:300"
], assets_folder="./static/assets")

app.css.config.serve_locally = True

# ################################# LOAD DATA ################################
grant_to_people_df = pd.read_csv('dcia/static/data/grants_to_people.csv')


# ############################## PREPROCESS DATA #############################
# Drop druplicates
edge_data = grant_to_people_df.drop_duplicates(keep="first").reset_index(drop=True)
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
}

# Define the styles of the CSS components
styles = {
    "json-output": {
        "overflow-y": "scroll",
        "height": "calc(50% - 25px)",
        "border": "thin lightgrey solid",
    },
    "tab": {"height": "calc(98vh - 115px)"},
}

########################### Functions ###################################################################
# Initialize global data structures for node expansion (followers and following)
def populate_relationships(edges: list):
    """This function creates and populates dictionaries representing nodes and edges in the graph."""
    following_node_di = {}
    following_edges_di = {}
    followers_node_di = {}
    followers_edges_di = {}

    # Iterate through each edge to populate following and followers dictionaries
    for index, edge in edges.iterrows():
        source = edge['from']
        target = edge['to']

        # Populate following relationships
        if source not in following_node_di:
            following_node_di[source] = []
            following_edges_di[source] = []

        following_edges_di[source].append({
            "data": {
                "id": str(source + target),
                "source": str(source),
                "target": str(target)
            }
        })

        # Populate followers relationships
        if target not in followers_node_di:
            followers_node_di[target] = []
            followers_edges_di[target] = []

        followers_edges_di[target].append({
            "data": {
                "id": str(source + target),
                "source": str(source),
                "target": str(target)
            }
        })

    # Now populate the lists of following and follower nodes based on edges
    for source, edges in following_edges_di.items():
        following_node_di[source] = [{'data': {'id': str(edge['data']['target']), 'label': str(edge['data']['target'])}} for edge in edges]

    for target, edges in followers_edges_di.items():
        followers_node_di[target] = [{'data': {'id': str(edge['data']['source']), 'label': str(edge['data']['source'])}} for edge in edges]

    return following_node_di, following_edges_di, followers_node_di, followers_edges_di

############################### This function is a replacement for the search bar ###################################
def get_node_with_highest_degree(edges_dict: dict):
    """This function calculates the degree of each node and returns the node with the highest degree."""
    degrees = {}
    for source, edges in edges_dict.items():
        degrees[source] = len(edges)
    # Find the node with the highest degree
    max_degree_node = max(degrees, key=degrees.get)

    # Retrieve the target node of the highest degree node
    edges_of_max_node = edges_dict[max_degree_node]
    first_edge = edges_of_max_node[0]  # Assuming at least one edge exists
    max_node_target = first_edge["data"]["target"]

    # Construct the node data with the desired layout
    node_with_highest_degree = {
        "data": {
            "id": str(max_node_target),
            "label": str(max_node_target)
        }
    }

    return node_with_highest_degree

######################################## Initiate functions ####################################################
following_node_di, following_edges_di, followers_node_di, followers_edges_di = populate_relationships(edges)

genesis_node = get_node_with_highest_degree(following_edges_di)
default_elements = [genesis_node]

################################### Dash Components #######################################################
# Define the app layout, integrating the control panel and cytoscape component
control_panel = dcc.Tab(
    label="Explore network",
    children=[
        html.Br(),
        html.P(
            children = "Search for person or grant:",
            style = {
                "marginLeft": "3px"
                }
            ),
            dcc.Input(
                id="search-input",
                type="text",
                placeholder = "Type to search..."
            ),
        NamedDropdown(
            name="Layout",
            id="dropdown-layout",
            options=DropdownOptionsList(
                "random",
                "grid",
                # "circle",
                # "concentric",
                # "breadthfirst",
                # "cose",
                "Default (cose-bilkent)",
                # "dagre",
                # "cola",
                # "klay",
                # "spread",
                # "euler",
            ),
            value="Default (cose-bilkent)",
            clearable=False,
        ),
        NamedRadioItems(
            name="Expand",
            id="radio-expand",
            options=DropdownOptionsList(
                "People", "Grant"
            ),
            value="People",
        ),
    ],
)
json_panel = dcc.Tab(
    label="JSON",
    children=[
        html.Div(
            #style=styles["tab"],
            children=[
                html.P("Node Object JSON:"),
                html.Pre(
                    id="tap-node-json-output",
                    #style=styles["json-output"],
                ),
                html.P("Edge Object JSON:"),
                html.Pre(
                    id="tap-edge-json-output",
                    #style=styles["json-output"],
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
            style= {
                "minWidth": "100%",
                "height": "95vh"
            },
            id="cytoscape",
            elements=default_elements,
            stylesheet=[
                # Default stylesheet
                {
                    "selector": "node",
                    "style": {
                        "opacity": 0.65
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "curve-style": "bezier",
                        "opacity": 0.65
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
        "padding": "15px",
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
    State("radio-expand", "value"),
    prevent_initial_call=True
)
def generate_elements(nodeData: dict, elements: dict, expansion_mode):
    """
    No Node has no data, return the elements unchanged.
    :param dict nodeData: nodedata contains: (expanded: bool), (class: string) and (data: dict) with (id: string), (label: string)
    :param dict elements: all elements returned from cytoscape.
    """
    if not nodeData:
        return elements

    # Node has already been expanded; no further action is necessary.
    if nodeData.get("expanded"):
        return elements

    # Mark the node as expanded to prevent re-expansion.
    for element in elements:
        if nodeData["data"]["id"] == element.get("data", {}).get("id"):
            element["data"]["expanded"] = True
            break

    # Expand nodes based on the expansion mode (followers or following).
    if expansion_mode == "People":
        # Add follower nodes and edges.
        followers_nodes = followers_node_di.get(int(nodeData["data"]["id"]))
        followers_edges = followers_edges_di.get(int(nodeData["data"]["id"]))
        if followers_nodes:
            for node in followers_nodes:
                node["classes"] = "followerNode"
            elements.extend(followers_nodes)

            if followers_edges:
                for follower_edge in followers_edges:
                    follower_edge["classes"] = "followerEdge"
                elements.extend(followers_edges)
    elif expansion_mode == "Grant":
        # Add following nodes and edges.
        following_nodes = following_node_di.get(int(nodeData["data"]["id"]))
        following_edges = following_edges_di.get(int(nodeData["data"]["id"]))

        if following_nodes:
            for node in following_nodes:
                if node["data"]["id"] != genesis_node["data"]["id"]:
                    node["classes"] = "followingNode"
                    elements.append(node)

        if following_edges:
            for follower_edge in following_edges:
                follower_edge["classes"] = "followingEdge"
            elements.extend(following_edges)

    return elements

@app.callback(
    Output("cytoscape", "elements",allow_duplicate=True),
    Input("search-input", "value"),
    prevent_initial_call=True
)
def update_graph(search_value):
    if not search_value:
        return cyto_edges + cyto_nodes
    filtered_data_edges = []
    filtered_data_nodes = set()

    for edge in cyto_edges:
        if edge['data']['source'] == search_value or edge['data']['target'] == search_value:
            filtered_data_edges.append(edge)
            filtered_data_nodes.update([edge['data']['source'], edge['data']['target']])
    new_cyto_nodes = [node for node in cyto_nodes if node['data']['id'] in filtered_data_nodes]

    return filtered_data_edges + new_cyto_nodes

@app.callback(
    Output("cytoscape", "layout"),
    [Input("dropdown-layout", "value")])
def update_layout(layout_value):
    return {"name": layout_value}

@app.callback(
    Output("tap-node-json-output", "children"),
    [Input("cytoscape", "tapNode")])
def display_tap_node(data):
    return json.dumps(data, indent=2) if data else ""

@app.callback(
    Output("tap-edge-json-output", "children"),
    [Input("cytoscape", "tapEdge")])
def display_tap_edge(data):
    return json.dumps(data, indent=2) if data else ""

if __name__ == "__main__":
    app.run_server(debug=False, port = 5002)
