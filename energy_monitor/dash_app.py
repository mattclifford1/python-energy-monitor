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

    # Get data
    #data = energy_monitor.utils.read_results('energy_monitor/data-examples/example.csv')
    data = pd.read_csv('energy_monitor/data-examples/example.csv')
    names_unique = np.unique(data['name'].values)
    labels_dropdown = [{'label' : name, 'value':name } for name in names_unique]

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
        dcc.Graph(id='plot_1'),
        dcc.Graph(id='plot_2')
    ])
    
    @app.callback(
    Output('plot_1', 'figure'),
    Input('multi_selector', 'value')
    )
    def update_plot1(names):
        #values = data[data==names]
        df = data[data['name'].isin(names)]
        fig = px.bar(df, x='name', y='cumulative_ia', title="Cumulative Energy",
                    labels={'cumulative_ia':'Cumulative Energy [J]', 'name':'Test name'}
        )
        return fig

    @app.callback(
    Output('plot_2', 'figure'),
    Input('multi_selector', 'value')
    )
    def update_plot2(names):
        df = data
        df['date'] = data['date'].apply(lambda x: x[:10])
        fig = px.bar(data, x='date', y='cumulative_ia', title="Cumulative Energy", color="name",
                    labels={'cumulative_ia':'Cumulative Energy [J]', 'date':'Date'}
        )
        return fig
    
    app.run_server(debug=True)   
