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
import ast

if __name__ == "__main__":
    # Instantiate Dash app
    app = dash.Dash()     
    
    # Get data and features
    data = pd.read_csv('energy_monitor/data-examples/example.csv')  
    data['name_unique'] = data['name'] + '_' + data['date']
    data['timeseries_1'] = data['timeseries_1'].apply(lambda x: ast.literal_eval(x))
    name_test = np.unique(data['name'].values).tolist(),             # for some reasons, this is stored as a tuple
    unique_name_test = np.unique(data['name_unique'].values).tolist(),      # for some reasons, this is stored as a tuple
    name_dropdown = [{'label' : name, 'value': name} for name in name_test[0]],
    unique_name_dropdown = [{'label' : name, 'value': name} for name in unique_name_test[0]],

    # Functions
    @app.callback(
    Output('plot_1', 'figure'),
    Input('test-names-dropdown', 'value')
    )
    def update_plot1(names):
        #values = data[data==names]
        df = data[data['name'].isin(names)]
        fig = px.bar(df, x='name', y='cumulative_ia', title="Cumulative Energy for selected tests",
                    labels={'cumulative_ia':'Cumulative Energy [J]', 'name':'Test name'}
        )
        return fig

    def update_plot2():
        df = data
        df['date'] = data['date'].apply(lambda x: x[:10])
        fig = px.bar(df, x='date', y='cumulative_ia', title="Cumulative Energy over time", color="name",
                    labels={'cumulative_ia':'Cumulative Energy [J]', 'date':'Date'}
        )
        return fig

    @app.callback(
    Output('plot_3', 'figure'),
    Input('unique-names-dropdown', 'value') 
    )
    def update_plot3(name):
        df = data[data['name_unique'] == str(name)]
        timeseries = df['timeseries_1'].values[0]
        print(timeseries)
        fig = px.line(x=np.arange(0, len(timeseries)), y=timeseries, title=f"Timeseries for {name}", 
        labels={'x': 'Indexes', 'y': 'Timeseries'})
        
        #fig = px.scatter(df,  y='timeseries_1', title="Cumulative Energy", color="name",
        #            labels={'name_unique':'Test name', 'date':'Date'})
        
        return fig

    # Dash histogram
    app.layout = html.Div(children=[
        html.H1('Energy Monitor',
            style={
                "font-family": "Montserrat",
                "textAlign": "center"
                }
            ),
        html.Div([
            html.P(['Choose the tests to compare: ', html.Br()]),
            dcc.Dropdown(
                    id='test-names-dropdown',
                    options=name_dropdown[0],   # list of test names
                    value=name_test[0],        # default
                    multi=True,
                    style=dict(
                            width='50%',
                        )
                )
        ]),        
        dcc.Graph(id='plot_1'),
        dcc.Graph(id='plot_2', figure=update_plot2()),
        html.P(['Choose the timeseries to visualise: ', html.Br()]),
        dcc.Dropdown(
            id='unique-names-dropdown',
            options=unique_name_dropdown[0],   # list of test names
            value=unique_name_test[0][0],        # default
            multi=False,
            style=dict(
                    width='60%',
                )
        ),
        dcc.Graph(id='plot_3',
        style=dict(
            width='70%'
            )
        )
    ])
    
    app.run_server(debug=True)   
