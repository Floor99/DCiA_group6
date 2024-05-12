import pandas as pd
from dash import html
from typing import Dict, Any

# Define styles for the tables
stylesheet = {
    'fontFamily': "alegreya sans, sans-serif",
    'fontSize': '16px',
    'textAlign': 'center',
    'width': '100%',
    'table-layout': 'fixed',
    'borderCollapse': 'collapse',
    'border': '1px solid black',
    'background-color': '#dfe0e1',
    'marginRight': '10px',
    'marginBottom': '0px'
}

stylesheetNodes = {
    'fontFamily': "alegreya sans, sans-serif",
    'fontSize': '16px',
    'textAlign': 'center',
    'width': '100%',
    'table-layout': 'fixed',
    'borderCollapse': 'collapse',
    'border': '1px solid black',
    'background-color': '##d2d4d3',
    'marginRight': '10px',
    'marginBottom': '10px'
}


td_stylesheet = {
    'width': '50%'
}

def feature_table(cytoscape_nodes: Dict[str, Any], source_att_df: pd.DataFrame, target_att_df: pd.DataFrame, adjency_list_df: pd.DataFrame, node_index: int):
    # Determine NODE_ID based on whether cytoscape_nodes is a list or a single node
    if isinstance(cytoscape_nodes, list):
        NODE_ID = str(cytoscape_nodes[node_index]["id"])
    else:
        NODE_ID = str(cytoscape_nodes)

    # Concatenate the source and target attribute dataframes
    combined_df = pd.concat([
        source_att_df[source_att_df['Node'].astype(str).str.startswith(NODE_ID)],
        target_att_df[target_att_df['Node'].astype(str).str.startswith(NODE_ID)]
    ])

    combined_html = []
    for _, row in combined_df.iterrows():
        node_id = row['Node']
        # Create a DataFrame for displaying attributes, excluding 'Node_Size'
        attributes_df = pd.DataFrame([("Selected Node", node_id)] + list(row.drop(['Node','index', 'Node_Size']).items()), columns=['Attribute', 'Value'])
        attributes_df['Attribute'] = attributes_df['Attribute'].apply(truncate_with_dots)
        # Get connected nodes from adjacency list
        connected_nodes_df = adjency_list_df[adjency_list_df['from'] == node_id]['to']
        connected_nodes_df = pd.concat([connected_nodes_df, adjency_list_df[adjency_list_df['to'] == node_id]['from']]).drop_duplicates()
        # Append generated HTML for attributes and connected nodes to combined_html
        combined_html.append(generate_table_html(attributes_df, connected_nodes_df))

    return html.Div(combined_html, style={"width": "100%"})

def generate_table_html(attributes_df, connected_nodes_df):
    attributes_df.dropna(inplace=True)
    return html.Div([
        html.Table(
            [html.Tr([html.Th(col, style=td_stylesheet) for col in attributes_df.columns])] +
            [html.Tr([html.Td(attributes_df.at[idx, col], style=td_stylesheet) for col in attributes_df.columns]) for idx in attributes_df.index],
            style=stylesheet
        ),
        html.Table(
            [html.Tr([html.Th('Connected Nodes', style=td_stylesheet)])] +
            [html.Tr([html.Td(node, style=td_stylesheet)]) for node in connected_nodes_df],
            style=stylesheetNodes
        )
    ])

def truncate_with_dots(string):
    # Truncate strings longer than 20 characters
    return string[:18] + "..." if len(string) > 20 else string
