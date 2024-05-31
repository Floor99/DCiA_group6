################################# IMPORT PACKAGES ################################

import pandas as pd

################################# MAIN CODE ################################

def load_data():
    """
    Load and process dataset files into structured DataFrames.

    This function performs several key operations:
    - It loads data.
    - Extracts relevant attributes and processes the data to prepare for network visualization.
    - Removes duplicate entries and filters out unconnected nodes.
    - Normalizes the 'Connected nodes' count into a 'Node_Size' metric for visualization.

    Returns:
        tuple: Contains processed DataFrames for people-to-people relationships, grants-to-people relationships, and attribute tables.
    """
    # Load people_to_people.csv, grants_to_people.csv and attribute_tabel_final.xlsx
    att_table = pd.read_excel('dcia/static/data/attributes_final.xlsx')
    grant_to_people_df = pd.read_csv('dcia/static/data/grants_to_people.csv')
    people_to_people_df = pd.read_csv('dcia/static/data/people_to_people.csv')
        
    # Extract the three attributes: grant awarded, doi year, and organisation
    grant_att_table = att_table[att_table['Grant Awarded'] != 0].iloc[:, 0:3]
    people_att_table = att_table[att_table['Organisation'] != 0].iloc[:, [0, 3, 4, 5, 6]]
    edge_df = grant_to_people_df.drop_duplicates(keep="first").reset_index(drop=True)
    
    # Ensure that 'from' and 'to' in edges are not the same to avoid self-loops
    edge_df = edge_df[edge_df['from'] != edge_df['to']].reset_index(drop=True)
    
    # Remove nodes without edges and insert the nodes and edges into a dataset readable by the network generator
    attribute_csv1 = grant_att_table[grant_att_table['Node'].isin(edge_df['from']) | grant_att_table['Node'].isin(edge_df['to'])].reset_index()
    
    # Calculate and append the total number of connections for each node
    for i in range(len(attribute_csv1)):
        attribute_csv1.loc[i, 'Connected nodes'] = len(edge_df[edge_df.to == attribute_csv1.loc[i,'Node']])
        attribute_csv1.loc[i, 'Connected nodes'] = attribute_csv1.loc[i, 'Connected nodes']+len(edge_df[edge_df['from'] == attribute_csv1.loc[i,'Node']])
    
    # Normalize the 'Connected nodes'
    max_val = max(attribute_csv1['Connected nodes'])
    attribute_csv1['Node_Size'] = attribute_csv1['Connected nodes']/max_val                                                           
     
    # Same process is repeated for people attributes table
    attribute_csv_empty = people_att_table[people_att_table['Node'].isin(edge_df['from']) | people_att_table['Node'].isin(edge_df['to'])].reset_index()
    
    for i in range(len(attribute_csv_empty)):
        attribute_csv_empty.loc[i, 'Connected nodes'] = len(edge_df[edge_df.to == attribute_csv_empty.loc[i,'Node']])
        attribute_csv_empty.loc[i, 'Connected nodes'] = attribute_csv_empty.loc[i, 'Connected nodes']+len(edge_df[edge_df['from'] == attribute_csv_empty.loc[i,'Node']])  
    
    max_val = max(attribute_csv_empty['Connected nodes'])
    attribute_csv_empty['Node_Size']=attribute_csv_empty['Connected nodes']/max_val 
    attribute_csv1.set_index('Node', inplace = True, drop=False)
    attribute_csv_empty.set_index('Node', inplace = True, drop=False)
    # Return the processed DataFrames
    return people_to_people_df, grant_to_people_df,  attribute_csv_empty, attribute_csv1