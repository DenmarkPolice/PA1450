# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import re
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import glob as glob
import os
from weatherdata import weatherdata

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

website = dash.Dash(__name__, external_stylesheets=external_stylesheets)

np.random.seed(50)
x_rand = np.random.randint(1,61,60)
y_rand = np.random.randint(1,61,60)







data = weatherdata(os.getcwd() + "\\rawData")
data.import_to_data()


dataframes = data.get_data_frames()

for df in dataframes:
    for label in df.columns:
        print(label + "\n")



website.layout = html.Div(children = [
    html.Label('Parameter'),
    dcc.Dropdown(
        id='dropdown2',
        options=[
            {'label': i, 'value' : i} for i in ['KSD', 'KNA', 'GTB']],
            value = 'KSD',
            multi=True,
    ),
    html.Div(id='dd-output-container'),
    html.Br(),

     dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(2009, 7, 1),
        max_date_allowed=dt(2020, 2, 1),
        initial_visible_month=dt(2020, 1, 1),
        end_date=dt(2020, 2, 1).date()
    ),
    html.Div(id='output-container-date-picker-range'),
    dcc.Graph(
        id='scatter-chart',
        figure = {'data' : [
            go.Scatter(
                x = x_rand,
                y = y_rand, 
                mode = 'markers'
            )
        ],
        'layout' : go.Layout(
            title = 'Scatterplot',
            xaxis = {'title' : 'Test'},
            yaxis = {'title' : 'Test2'}
        )
        }
    )

])


@website.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('dropdown2', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    website.run_server(debug=True)