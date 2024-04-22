import pandas as pd

def load_data():
    # Load people_to_people.csv, grants_to_people.csv and attribute_tabel_final.xlsx
    knowledge_sharing = pd.read_csv('dcia/static/data/people_to_people.csv')
    grant_to_people_df = pd.read_csv('dcia/static/data/grants_to_people.csv')
    att_table = pd.read_excel('dcia/static/data/attributes_final.xlsx')
   
        
    # Extract the three attributes: grant awarded, doi year, and organisation
    grant_att_table = att_table[att_table['Grant Awarded'] != 0].iloc[:, 0:3]
    publ_att_table = att_table[att_table['DOI Year'] != 0].iloc[:, [0, 7]]
    people_att_table = att_table[att_table['Organisation'] != 0].iloc[:, [0, 3, 4, 5, 6]]

    edge_df=grant_to_people_df.drop_duplicates(keep="first").reset_index(drop=True)
    edge_df = edge_df[edge_df['from'] != edge_df['to']].reset_index(drop=True)
    
    #remove nodes without edges and insert the nodes and edges into a dataset readable by the network generator
    attribute_csv1 = grant_att_table[grant_att_table['Node'].isin(edge_df['from']) | grant_att_table['Node'].isin(edge_df['to'])].reset_index()
    for i in range(len(attribute_csv1)):
        attribute_csv1.loc[i, 'Connected nodes'] = len(edge_df[edge_df.to == attribute_csv1.loc[i,'Node']])
        attribute_csv1.loc[i, 'Connected nodes'] = attribute_csv1.loc[i, 'Connected nodes']+len(edge_df[edge_df['from'] == attribute_csv1.loc[i,'Node']])
    #normalize
    max_val = max(attribute_csv1['Connected nodes'])
    attribute_csv1['Node_Size']=attribute_csv1['Connected nodes']/max_val                                                           
     #remove nodes without edges and insert the nodes and edges into a dataset readable by the network generator
    attribute_csv_empty = people_att_table[people_att_table['Node'].isin(edge_df['from']) | people_att_table['Node'].isin(edge_df['to'])].reset_index()
    for i in range(len(attribute_csv_empty)):
        attribute_csv_empty.loc[i, 'Connected nodes'] = len(edge_df[edge_df.to == attribute_csv_empty.loc[i,'Node']])
        attribute_csv_empty.loc[i, 'Connected nodes'] = attribute_csv_empty.loc[i, 'Connected nodes']+len(edge_df[edge_df['from'] == attribute_csv_empty.loc[i,'Node']])  
    max_val = max(attribute_csv_empty['Connected nodes'])
    attribute_csv_empty['Node_Size']=attribute_csv_empty['Connected nodes']/max_val 
    return knowledge_sharing, grant_to_people_df,  attribute_csv_empty, attribute_csv1
