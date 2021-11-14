# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import dash
from dash import dcc
from dash import html
import energy_monitor
import os
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
  
if __name__ == "__main__":
    # Instantiate Dash app
    app = dash.Dash()     
    print(os.getcwd())
    # Get data
    #data = energy_monitor.utils.read_results('energy_monitor/data-examples/example.csv')
    data = pd.read_csv('energy_monitor/data-examples/example.csv')
    names_unique = np.unique(data['name'].values)
    labels_dropdown = [{'label' : name, 'value':name } for name in names_unique]
    print(labels_dropdown)

    # Dash histogram
    app.layout = html.Div(children=[
        html.H1('Energy Monitor',
            style={
                "font-family": "Montserrat",
                "textAlign": "center"
                }
            ),
        dcc.Dropdown(
            id='multi_selector',
            options=labels_dropdown,   # list
            value=names_unique,    # default
            multi=True
        ),        
        dcc.Graph(id='cumulative_consumption')
    ])
    
    @app.callback(
    Output('cumulative_consumption', 'figure'),
    Input('multi_selector', 'value')
    )
    def update_output(names):
        #values = data[data==names]
        df = data[data['name'].isin(names)]
        fig = px.bar(df, x='name', y='cumulative_ia', title="Cumulative Energy",
                    labels={'cumulative_ia':'Cumulative Energy [J]', 'name':'Test name'}
        )
        print(names)

        return fig
    
    app.run_server(debug=True)   
