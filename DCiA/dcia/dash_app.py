from dash import Dash, dcc, html, no_update
from dash.dependencies import Input, Output
import os
import dash_cytoscape as cyto
from dcia.f_visualisation import visualization
from dcia.f_load_data import load_data

cyto.load_extra_layouts()

app = Dash(__name__)

# Paths to the files to monitor
file_paths = {
    'attributes': 'dcia/static/data/attributes_final.xlsx',
    'grants': 'dcia/static/data/grants_to_people.csv',
    'people': 'dcia/static/data/people_to_people.csv'
}

# Function to get the last modification times
def get_last_mod_times():
    return {path: os.path.getmtime(file_paths[path]) for path in file_paths}

# Load initial data and create initial layout
try:
    print("Loading initial data...")
    knowledge_sharing, ga_grants_to_people_df, ga_grant_att_table, ga_people_att_table = load_data()
    initial_layout = visualization(ga_grants_to_people_df, ga_people_att_table, ga_grant_att_table)
    print("Initial layout created.")
except Exception as e:
    initial_layout = html.Div(f"Error loading initial data: {str(e)}")
    print(f"Error during initial data loading: {str(e)}")

app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=1*10000,  # 10 seconds
        n_intervals=0
    ),
    html.Div(id='graph-output', children=initial_layout)  # Include the initial layout
])
# Make sure to define last_mod_times at the top level, not inside any functions.
last_mod_times = get_last_mod_times()

@app.callback(
    Output('graph-output', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_layout(n):
    global last_mod_times  # Declare last_mod_times as global to modify it within this function
    try:
        current_mod_times = get_last_mod_times()
        if current_mod_times != last_mod_times:
            print("Files have been updated, reloading data...")
            last_mod_times = current_mod_times
            knowledge_sharing, ga_grants_to_people_df, ga_grant_att_table, ga_people_att_table = load_data()
            layout = visualization(ga_grants_to_people_df, ga_people_att_table, ga_grant_att_table)
            print("Layout updated")
            return layout
        else:
            print("No changes detected in files.")
            # If no changes are detected, we prevent the layout from updating.
            return no_update
    except Exception as e:
        print(f"Error during callback execution: {str(e)}")
        # If an exception is caught, display it on the dashboard.
        return html.Div(f"Error updating visualization: {str(e)}")

if __name__ == '__main__':
    app.run_server(debug=True, port=5001)
