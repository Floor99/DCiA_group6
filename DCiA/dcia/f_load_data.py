import pandas as pd

def load_data():
    # Load people_to_people.csv, grants_to_people.csv and attribute_tabel_final.xlsx
    knowledge_sharing = pd.read_csv('dcia/static/network_visualisations/people_to_people.csv')
    grant_to_people_df = pd.read_csv('dcia/static/network_visualisations/grants_to_people.csv')
    att_table = pd.read_excel('dcia/static/network_visualisations/attributes_final.xlsx')

    # Extract the three attributes: grant awarded, doi year, and organisation
    grant_att_table = att_table[att_table['Grant Awarded'] != 0].iloc[:, 0:3]
    publ_att_table = att_table[att_table['DOI Year'] != 0].iloc[:, [0, 7]]
    people_att_table = att_table[att_table['Organisation'] != 0].iloc[:, [0, 3, 4, 5, 6]]

    return knowledge_sharing, grant_to_people_df, grant_att_table, people_att_table
