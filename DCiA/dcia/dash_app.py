from dash import Dash
import dash_cytoscape as cyto
from dcia.f_visualisation import visualization
from dcia.f_load_data import load_data
cyto.load_extra_layouts()

app = Dash(__name__)

if __name__ == '__main__':
    knowledge_sharing, ga_grants_to_people_df, ga_grants_att_table, ga_people_att_table = load_data()
    layout = visualization(ga_grants_to_people_df,ga_people_att_table,ga_grants_att_table) # @niels is the visualisation currently without people to people? because they are not passed to the visualisation function?

    app.layout = layout
    app.run(debug=True, port=5001)













# When we are doing knowledge sharing:
# layout=visualization(knowledge_sharing,people_att_table,0)
