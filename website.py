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
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

website = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = weatherdata(os.getcwd() + "\\rawData")
data.import_data()
dataframes = data.get_ranged_df("2015-05-01", "2015-05-05")

frameNames = []
for df in dataframes:
    frameNames.append(df.columns[2])

date_and_time = []

for i in range(len(dataframes[0][dataframes[0].columns[0]])):
    date_and_time.append(dataframes[0].iat[i,0] + " " + dataframes[0].iat[i,1])
 

dictionary = {}

dictionary["Tid"] = date_and_time
dictionary[dataframes[0].columns[2]] = dataframes[0][dataframes[0].columns[2]]

fig = px.line(dictionary, x = 'Tid', y = dataframes[0].columns[2])





website.layout = html.Div(children = [
    html.Label('Parameter'),
    dcc.Dropdown(
        id='dropdown2',
        options=[
            {'label': i, 'value' : i} for i in frameNames],
            value = frameNames[0],
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
        figure = fig      
    )

])

@website.callback(dash.dependencies.Output('scatter-chart', 'figure'), [dash.dependencies.Input('my-date-picker-range', 'start_date'),
 dash.dependencies.Input('my-date-picker-range', 'end_date')])
def date_range_set_enabled_state(start_date, end_date):
    dataframes = data.get_ranged_df(start_date, end_date)

    
    date_and_time = []

    for i in range(len(dataframes[0][dataframes[0].columns[0]])):
        date_and_time.append(dataframes[0].iat[i,0] + " " + dataframes[0].iat[i,1])
    

    dictionary = {}

    dictionary["Tid"] = date_and_time
    dictionary[dataframes[0].columns[2]] = dataframes[0][dataframes[0].columns[2]]
    
    fig = px.line(dictionary, x = 'Tid', y = dataframes[0].columns[2])
    return fig


if __name__ == '__main__':
    website.run_server(debug=True)