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
import time
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import webbrowser

'''
Launch the dashboard to display results from the database

Args:
  - csv_file (str): file location of database. Default: '~/Documents/energy_monitor.csv'
'''
def run(csv_file='data-examples/example.csv'):
    print(csv_file)
    external_stylesheets = [
        "https://fonts.googleapis.com/css2?family=Nunito&display=swap",
        dbc.themes.MATERIA
    ]
    # Instantiate Dash app
    app = dash.Dash(external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
    app.css.config.serve_locally = True

    # Get data and features
    data = pd.read_csv(csv_file)
    print(data['remove_background_energy'].values)
    data['remove_background_energy_renamed'] = data['remove_background_energy'].apply(lambda x: 'Idle' if x==True else 'No_Idle')
    data['name_unique'] = data['name'] + '_' + data['date'] + '_' + data['remove_background_energy_renamed']
    data['name'] = data['name']+ '_' + data['remove_background_energy_renamed']
    data['cpu utilisation'] = data['cpu utilisation'].apply(lambda x: ast.literal_eval(x))
    name_test = np.unique(data['name'].values).tolist()
    unique_name_test = np.unique(data['name_unique'].values).tolist()
    name_dropdown = [{'label' : name, 'value': name} for name in name_test]
    unique_name_dropdown = [{'label' : name, 'value': name} for name in unique_name_test]
    dates_str = data['date'].values
    dates_datetime = [datetime.strptime(x, '%Y-%m-%d-%H-%M-%S') for x in dates_str]
    daterange = pd.date_range(start=min(dates_datetime),end=max(dates_datetime))
    data['date_datetime'] = dates_datetime

    def unixTimeMillis(dt):
        ''' Convert datetime to unix timestamp '''
        return int(time.mktime(dt.timetuple()))

    def unixToDatetime(unix):
        ''' Convert unix timestamp to datetime. '''
        return pd.to_datetime(unix,unit='s')

    def getMarks(start, end, Nth=10):
        ''' Returns the marks for labeling.
            Every Nth value will be used.
        '''
        result = {}
        for i, date in enumerate(daterange):
            if (i == 0) or (i == (len(daterange)-1)):
                result[unixTimeMillis(date)] = str(date.strftime('%Y-%m-%d'))
            elif(i%Nth == 1):
                # Append value to dict
                result[unixTimeMillis(date)] = str(date.strftime('%Y-%m-%d'))
        return result

    # Functions
    @app.callback(
    Output('plot_1', 'figure'),
    Input('test-names-dropdown', 'value'),
    Input('test-modalities-dropdown', 'value')
    )
    def update_plot1(names, modalities):
        df = data[data['name'].isin(names)]
        title = 'Cumulative'
        if modalities=='Average':
            df = df.groupby(by=['name'], ).mean().reset_index()
            title = 'Average'
        fig = px.bar(df, x='name', y='cumulative_ia', title=f"{title} Energy for selected tests", color='name',
                    labels={'cumulative_ia':f'Energy [J]', 'name':'Test name'}
        )
        return fig

    @app.callback(
    Output('plot_2', 'figure'),
    Input('year_slider', 'value'))
    def update_plot2(year_range):
        df = data
        min_date = unixToDatetime(year_range[0]).replace(hour=0, minute=0)
        max_date = unixToDatetime(year_range[1]).replace(hour=23, minute=59)
        df = df.loc[(df['date_datetime'] >= min_date) & (df['date_datetime'] <= max_date)]
        df['date'] = data['date'].apply(lambda x: x[:10])
        fig = px.bar(df, x='date', y='cumulative_ia', title="Cumulative Energy over time", color="name",
                    labels={'cumulative_ia':'Cumulative Energy [J]', 'date':'Date'}
        )
        return fig

    @app.callback(
    Output('plot_3', 'figure'),
    Input('unique-names-dropdown', 'value'),
    Input('unique-names-dropdown2', 'value'),
    Input('compare-timeseries-radioitem', 'value')
    )
    def update_plot3(name1, name2, comparison):
        if comparison=='No':
            df = data[data['name_unique'] == str(name1)]
            timeseries = df['cpu utilisation'].values[0]
            fig = px.line(x=np.arange(0, len(timeseries))/2, y=timeseries, title=f"CPU Utilisation for {name1}",
            labels={'x': 'Time [s]', 'y': 'CPU% [W s]'}, template='plotly')
        else:
            fig = make_subplots(rows=1, cols=2, subplot_titles=(f"CPU Utilisation",  f"CPU Utilisation"))
            df1 = data[data['name_unique'] == str(name1)]
            df2 = data[data['name_unique'] == str(name2)]
            timeseries1 = df1['cpu utilisation'].values[0]
            timeseries2 = df2['cpu utilisation'].values[0]

            fig.add_trace(go.Scatter(x=np.arange(0, len(timeseries1))/2, y=timeseries1, name='Timeseries 1'),
                row=1, col=1
            )
            fig.add_trace(go.Scatter(x=np.arange(0, len(timeseries2))/2, y=timeseries2, name='Timeseries 2'),
                row=1, col=2
            )

            # edit axis labels
            fig['layout']['xaxis']['title']='Time [s]'
            fig['layout']['xaxis2']['title']='Time [s]'
            fig['layout']['yaxis']['title']='CPU% [W s]'
            fig['layout']['yaxis2']['title']='CPU% [W s]'
        return fig

    @app.callback(
    Output('show_comparison_query1', 'children'),
    Input('compare-timeseries-radioitem', 'value'))
    def show_comparison_query1(radioitem):
        a = None
        if radioitem == 'Yes':
            a = html.P(['Select the second timeseries to compare:'])
        return a

    @app.callback(
    Output('unique-names-dropdown2', 'style'),
    Input('compare-timeseries-radioitem', 'value'))
    def show_comparison_query2(radioitem):
        display_value = 'table' if radioitem == 'Yes' else 'None'
        return {'width': '100%', 'display' : display_value, '-webkit-appearance': 'menu'}

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
                        options=name_dropdown,   # list of test names
                        value=name_test,        # default
                        multi=True,
                        style=dict(
                                width='60%',
                            )
                    ),
                html.P(['Choose the modality of comparison: ', html.Br()],
                    style={'margin-top': '15px'}),
                dcc.RadioItems(
                        id='test-modalities-dropdown',
                        options=[{'label': 'Average', 'value': 'Average'},
                                 {'label': 'Cumulative', 'value': 'Cumulative'}], # list of modalities
                        value='Average',        # default
                        style={
                            'display': 'grid'
                        }
                    )
                ],
                style={'margin':'auto'}),
            dcc.Graph(id='plot_1')
            ],
            style=style_shadow_box),

        html.Div([
            html.Div(
            [
                html.P(['Select the timeframe: ', html.Br()]),
                dcc.RangeSlider(
                    id='year_slider',
                    min = unixTimeMillis(daterange.min()),
                    max = unixTimeMillis(daterange.max()),
                    value = [unixTimeMillis(daterange.min()),
                            unixTimeMillis(daterange.max())],
                    marks=getMarks(daterange.min(),
                                daterange.max()),
                ),
                    ],
                style={'margin-top': '20',
                       'width': '50%'}
            ),

            dcc.Graph(id='plot_2')],
            style=style_shadow_box
            ),
        html.Div([
            html.P(['Choose the timeseries to visualise: ', html.Br()]),
            dcc.Dropdown(
                id='unique-names-dropdown',
                options=unique_name_dropdown,   # list of test names
                value=unique_name_test[0],        # default
                multi=False,
                style=dict(
                        width='60%',
                    )
            ),html.Br(),
            html.P(['Do you want to compare multiple timeseries?: ', html.Br()]),

            dcc.RadioItems(
                id='compare-timeseries-radioitem',
                options=[{'label': 'Yes', 'value': 'Yes'},
                            {'label': 'No', 'value': 'No'}], # list of modalities
                value='No',        # default
                style={
                    'display': 'grid'
                }
            ),html.Br(),

            html.Div(id='show_comparison_query1'),
            dcc.Dropdown(
                id='unique-names-dropdown2',
                options=unique_name_dropdown,   # list of test names
                value=unique_name_test[0],        # default
                multi=False,
                style=dict(
                    width='60%'
                )
            ),

            dcc.Graph(id='plot_3')
            ],
            style=style_shadow_box
            )
    ], style={'margin': '30px'})

    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=True)

if __name__ == '__main__':
    run()
