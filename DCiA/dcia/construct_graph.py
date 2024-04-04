
import pandas as pd
from dash import Dash, html
import dash_cytoscape as cyto
cyto.load_extra_layouts()

#run this app to run only the website
app = Dash(__name__)



#load colors for the nodes 
def interpolate_color(color1, color2, factor):
    """ Interpolate between two RGB colors """
    r = int(color1[0] * (1 - factor) + color2[0] * factor)
    g = int(color1[1] * (1 - factor) + color2[1] * factor)
    b = int(color1[2] * (1 - factor) + color2[2] * factor)
    return (r, g, b)

def number_to_rgb_gradient(number, min_val, max_val,csv):
    """ Convert number to RGB gradient """
    normalized_value = (number - min_val) / (max_val - min_val)
    if csv==1:
        color1 = (255,255,204)  # Lightest color (white)
        color2 = (255,0,0)  # Brightest color (red)
        
    if csv==2:
        color1 = (240,248,255) # Lightest color (blue)
        color2 = (0, 2, 29)  # Brightest color (dark blue)    
    return interpolate_color(color1, color2, normalized_value)


    
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
    app.layout = html.Div(
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
                #this section determines the label, size and opacity of all the nodes
                stylesheet=[
                    {'selector': 'node', 'style': {'label': 'data(label)',"font-size": "3px",'width': "5%",
                    'height': "5%",'background-color':'data(color)'}},
                    {'selector': 'edge', 'style': {"font-size": "3px",'opacity':0.3,'width': "0.3",}},
        ],
            )
        ]
        )
    return app.layout
    

if __name__ == '__main__':
     #load all the data that has been provided by apollo
    knowledge_sharing=pd.read_csv('dcia/static/network_visualisations/people_to_people.csv')
    grant_to_people_df=pd.read_csv('dcia/static/network_visualisations/grants_to_people.csv')

    #split excel file
    att_table=pd.read_excel('dcia/static/network_visualisations/Attribute table_Final (1).xlsx')
    grant_att_table=att_table[att_table['Grant Awarded']!=0].iloc[:, 0:3]
    publ_att_table=att_table[att_table['DOI Year']!=0].iloc[:, [0,7]]
    people_att_table=att_table[att_table['Organisation']!=0].iloc[:, [0,3,4,5,6]]
    
     #load the fastest visualization
    layout=visualization(grant_to_people_df,people_att_table,grant_att_table)
    #layout=visualization(knowledge_sharing,people_att_table,0)
    
    app.run(debug=True, port=5001)
