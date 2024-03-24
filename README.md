# DCiA_group6

Run the app: navigate to app.py and run the script in the terminal. Follow the link provided (e.g. http://127.0.0.1:5000/).

Once the app is running you can navigate from the landing page to e.g. grant_applications. Here you can see the figure produced by notebook grants_applications.ipynb.

To edit the network visualisation: navigate to dcia/static/network_visualisations and pick the notebook for the network you want to visualize. In this notebook you can create the figure that you want including the interactive elements. 
To export the figure, including interactive elements, you can include the following code: 

import plotly
plotly.offline.plot(fig, filename='grant_application_graph.html')

The webpage for grant_applications will fetch grant_application_graph.html and show it on the webpage. 
