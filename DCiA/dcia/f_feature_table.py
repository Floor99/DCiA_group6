import pandas as pd
from dash import html
from typing import Dict, Any

stylesheet= {
            'fontFamily': "alegreya sans, sans-serif",
            'fontSize': '16px',
            'textAlign': 'center',
            'width' : '100%',
            'table-layout': 'fixed',
        }
td_stylesheet= {
            'width' : '50%'
        }
def current_node_attributes_table(cytoscape_nodes : Dict[str, Any], source_att_df : pd.DataFrame, target_att_df : pd.DataFrame, adjency_list_df : pd.DataFrame, node_index: int ):
        NODE_ID = int(cytoscape_nodes[node_index]["id"])
        node_is_in_source_df = NODE_ID in source_att_df['Node'].values
        
        node_df = source_att_df if node_is_in_source_df else target_att_df

        node_attributes = node_df[node_df['Node'] == NODE_ID].iloc[0].drop(["index","Node","Node_Size"]).to_dict()

        # Prepend "Current Node : ID" to the attributes list.
        node_attributes = { 'Current Node': 100, **node_attributes }
        
        # Truncate the keys with an elipsis when it is too long
        node_attributes = {truncate_string(key, 19): value for key, value in node_attributes.items()}

        # Find the adjacent nodes in the given dataframe of structure: From to
        adjacent_nodes_df = adjency_list_df.loc[adjency_list_df['from'] == NODE_ID]['to']

        return html.Div([
            html.Table(
                # Header
                [
                    html.Tr([
                                html.Th("Attribute", style= td_stylesheet), html.Th("Value", style= td_stylesheet)
                            ], style= td_stylesheet)
                ] +
                [
                    html.Tr([
                                html.Td(key, style= td_stylesheet), html.Td(value, style= td_stylesheet)
                            ], style= td_stylesheet) for key, value in node_attributes.items()
                ],
                style=stylesheet
            ),
            html.Hr(),
            html.Table(
                # Header
                [
                    html.Tr([
                                html.Th('Connected Nodes'), html.Th('')
                            ], style= td_stylesheet)
                ] +
                # Body
                [
                        html.Tr(
                                    html.Td(val),
                                    style= td_stylesheet) for val in adjacent_nodes_df.values
                ],
                style=stylesheet
            )
        ], style= {"width" : "100%"})
def truncate_string(string: str, limit: int):
    return string[:limit] + '…' if len(string) > limit else string