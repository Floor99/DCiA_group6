from color_functions import interpolate_color, number_to_rgb_gradient
import pandas as pd
from dash import Dash, html
import dash_cytoscape as cyto

def visualization(csv,attribute_csv,attribute_csv2):
    #drop the duplicates and edges to themselves
    Edge_df=csv.drop_duplicates(keep="first").reset_index(drop=True)
    Edge_df = Edge_df[Edge_df['from'] != Edge_df['to']].reset_index(drop=True)

    #remove nodes without edges and insert the nodes and edges into a dataset readable by the network generator
    attribute_csv_empty = attribute_csv[attribute_csv['Node'].isin(Edge_df['from']) | attribute_csv['Node'].isin(Edge_df['to'])].reset_index()
    for i in range(len(attribute_csv_empty)):
        attribute_csv_empty.loc[i, 'Count'] = len(Edge_df[Edge_df.to == attribute_csv_empty.loc[i,'Node']])
        attribute_csv_empty.loc[i, 'Count'] = attribute_csv_empty.loc[i, 'Count']+len(Edge_df[Edge_df['from'] == attribute_csv_empty.loc[i,'Node']])

    min_val = min(attribute_csv_empty['Count'])
    max_val = max(attribute_csv_empty['Count'])

    # Convert each number to RGB gradient
    rgb_gradients = [number_to_rgb_gradient(num, min_val, max_val,1) for num in attribute_csv_empty['Count']]
    attribute_csv_empty['gradient']=rgb_gradients
    #adds the nodes
    nodes = [{
                "data": {"id": str(attribute_csv_empty.loc[i, "Node"]),
                       "label": str(attribute_csv_empty.loc[i, "Node"]),
                       'color': 'rgb'+str(attribute_csv_empty.loc[i, "gradient"])
                       }
                } for i in range(len(attribute_csv_empty))]


    #copy paste
    if isinstance(attribute_csv2, pd.DataFrame):
        #remove nodes without edges and insert the nodes and edges into a dataset readable by the network generator
        attribute_csv_empty2 = attribute_csv2[attribute_csv2['Node'].isin(Edge_df['from']) | attribute_csv2['Node'].isin(Edge_df['to'])].reset_index()

        for i in range(len(attribute_csv_empty2)):
            attribute_csv_empty2.loc[i, 'Count'] = len(Edge_df[Edge_df.to == attribute_csv_empty2.loc[i,'Node']])
            attribute_csv_empty2.loc[i, 'Count'] = attribute_csv_empty2.loc[i, 'Count']+len(Edge_df[Edge_df['from'] == attribute_csv_empty2.loc[i,'Node']])

        min_val = min(attribute_csv_empty2['Count'])
        max_val = max(attribute_csv_empty2['Count'])

        # Convert each number to RGB gradient
        rgb_gradients = [number_to_rgb_gradient(num, min_val, max_val,2) for num in attribute_csv_empty2['Count']]
        attribute_csv_empty2['gradient']=rgb_gradients

        #adds the nodes from the different csv in a different colour
        nodes2 = [{
                    "data": {"id": str(attribute_csv_empty2.loc[i, "Node"]),
                        "label": str(attribute_csv_empty2.loc[i, "Node"]),
                        'color': 'rgb'+str(attribute_csv_empty2.loc[i, "gradient"])
                        }
                    } for i in range(len(attribute_csv_empty2))]
        nodes.extend(nodes2)
    attribute_csv_empty.set_index('Node', inplace=True)

    #adds the edges
    edges = [
        {
        "data": {
            "source": str(Edge_df.loc[j, "from"]),
            "target": str(Edge_df.loc[j, "to"]),
            'label': attribute_csv_empty.loc[Edge_df.loc[j, "from"],str(attribute_csv_empty.columns[2])],

            }
        }
        for j in range(len(Edge_df))
    ]
    #combines the data into a cytoscape objects
    default_elements = nodes + edges
    #presets avalaible for the graph ["random","preset","circle","concentric","grid","breadthfirst","cose","cose-bilkent","fcose","cola","euler","spread","dagre","klay"].
    return html.Div(
        [
            cyto.Cytoscape(
                id="cytoscape",
                boxSelectionEnabled=False,
                autounselectify=True,
                elements=default_elements,
                layout={"name": "cose-bilkent"},
                style={
                    "width": "100%",
                    "height": "100%",
                    "position": "absolute",
                    "left": 0,
                    "top": 0,
                    "z-index": 999,
                },
                stylesheet=[
                    {'selector': 'node', 'style': {'label': 'data(label)',"font-size": "3px",'width': "5%",
                    'height': "5%",'background-color':'data(color)'}},
                    {'selector': 'edge', 'style': {"font-size": "3px",'opacity':0.3,'width': "0.3",}},
                ],
            )
        ]
    )
