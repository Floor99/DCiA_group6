from dash import Dash
import dash_cytoscape as cyto
from dcia.f_visualisation import visualization
from dcia.f_load_data import load_data
cyto.load_extra_layouts()

app = Dash(__name__)

if __name__ == '__main__':
    knowledge_sharing, grant_to_people_df, grant_att_table, people_att_table = load_data()
    layout = visualization(grant_to_people_df,people_att_table,grant_att_table)

    app.layout = layout
    app.run(debug=True, port=5001)













# When we are doing knowledge sharing:
# layout=visualization(knowledge_sharing,people_att_table,0)
