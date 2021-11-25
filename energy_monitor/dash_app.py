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
import dash_bootstrap_components as dbc

if __name__ == "__main__":
    external_stylesheets = [
        "https://fonts.googleapis.com/css2?family=Nunito&display=swap",
        dbc.themes.MATERIA
    ]
    # Instantiate Dash app
    app = dash.Dash(external_stylesheets=external_stylesheets)     
    app.css.config.serve_locally = True

    # Get data and features
    data = pd.read_csv('energy_monitor/data-examples/example.csv')  
    data['name_unique'] = data['name'] + '_' + data['date']
    data['cpu utilisation'] = data['cpu utilisation'].apply(lambda x: ast.literal_eval(x))
    name_test = np.unique(data['name'].values).tolist(),             # for some reasons, this is stored as a tuple
    unique_name_test = np.unique(data['name_unique'].values).tolist(),      # for some reasons, this is stored as a tuple
    name_dropdown = [{'label' : name, 'value': name} for name in name_test[0]],
    unique_name_dropdown = [{'label' : name, 'value': name} for name in unique_name_test[0]],

    # Functions
    @app.callback(
    Output('plot_1', 'figure'),
    Input('test-names-dropdown', 'value'),
    Input('test-modalities-dropdown', 'value')
    )
    def update_plot1(names, modalities):
        print(f'MODALITIES: {modalities}')
        df = data[data['name'].isin(names)]
        if modalities=='Average':
            df = df.groupby(by=['name'], ).mean().reset_index()
            print(df) 
        fig = px.bar(df, x='name', y='cumulative_ia', title="Cumulative Energy for selected tests", color='name',
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
        timeseries = df['cpu utilisation'].values[0]
        print(timeseries)
        fig = px.line(x=np.arange(0, len(timeseries)), y=timeseries, title=f"CPU Utilisation for {name}", 
        labels={'x': 'Time', 'y': 'CPU Utilisation'}, template='plotly')

        return fig

    # Variables for layout
    style_shadow_box = {
                'border-radius': '5px',
                'border': '1.5px solid rgba(0,0,0,.125)',
                'padding': '20px',
                'margin-top': '15px'}

    # Dash histogram
    app.layout = html.Div(children=[
        html.H1('Energy Monitor',
            style={
                "textAlign": "center"
                }
            ),
        html.Div([
            html.Span([
                html.Img(src='https://freerangestock.com/sample/38788/vector-lightbulb-ideas.jpg', height='80px'),
                f"Your total energy consumption is {int(np.floor(data['cumulative_ia'].sum()))} J"],             
                )
        ], style=style_shadow_box),

        html.Div([
            html.Div([
                html.P(['Choose the tests to compare: ', html.Br()]),
                dcc.Dropdown(
                        id='test-names-dropdown',
                        options=name_dropdown[0],   # list of test names
                        value=name_test[0],        # default
                        multi=True,
                        style=dict(
                                width='60%',
                            )
                    ),
                html.P(['Choose the modality of comparison: ', html.Br()],
                    style={'margin-top': '15px'}),
                dcc.Dropdown(
                        id='test-modalities-dropdown',
                        options=[{'label': 'Average', 'value': 'Average'},
                                 {'label': 'Cumulative', 'value': 'Cumulative'}], # list of modalities
                        value='Average',        # default
                        multi=False,
                        style=dict(
                                width='60%',
                            )
                    )
                ],
                style={'margin':'auto'}),               
            dcc.Graph(id='plot_1')                
            ],
            style=style_shadow_box),

        html.Div([    
            dcc.Graph(id='plot_2', figure=update_plot2())],
            style=style_shadow_box
            ),
        html.Div([   
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
            )],
            style=style_shadow_box
            )
    ], style={'margin': '30px'})
    
    app.run_server(debug=True)   
