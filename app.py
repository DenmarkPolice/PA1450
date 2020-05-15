import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
import re
import dash_table
import io
import base64
import pandas as pd
import os
from weatherdata import weatherdata
import plotly.express as px



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Get the data
data = weatherdata(os.getcwd() + "\\rawData")
data.import_data()
#Random dates just so that we can get to the attributes. 
data_frames = data.get_ranged_df("2015-05-01", "2015-05-02")

#Find all of the attributes to place in the first dropdown
attributes = []
for data_frame in data_frames:
    attributes.append(data_frame.columns[2])



fig = {'data' : []}

app.layout = html.Div(children=[
    html.H1(children='Historical weather data provided by SMHI'),

    #Attribute dropdown
    dcc.Dropdown(
        id='attribute-dropdown',
        options=[{'label':atr, 'value':atr} for atr in attributes],
        placeholder='Pick attributes',
        multi=False
    ),
    html.Br(),

    #Dropdown for yearly interval
    dcc.Dropdown(id='year-dropdown',options=[{'label':x, 'value': x} for x in range(2009, 2021)], placeholder='If you want to select an entire year, please do so here'),
    html.Div(id='year-dropdown-output'),
    html.Br(),

    #Pick an interval between two dates. 
    html.Div('If you would rather want to display the data between two dates, please enter those dates here'),
    dcc.DatePickerRange(
        id='date-pick-range',
        min_date_allowed=dt(2009, 8, 5),
        max_date_allowed=dt(2020, 2, 1),
        initial_visible_month=dt(2020, 1, 1),
        display_format='DD-MM-YYYY',
        clearable=True,
    ),
    html.Div(id='output-date-range'),
    html.Br(),

    html.Div(id='output-data-upload'),
    html.Div(id='fig-error'),
    #The generated graph
    dcc.Graph(
        id='scatter-chart',
        figure = fig      
    ),
])


def generateGraph(dataframe):
    '''Returns a px fig for the graph'''

    date_and_time = []
    for i in range(len(dataframe[dataframe.columns[0]])):
        date_and_time.append(dataframe.iat[i,0] + " " + dataframe.iat[i,1])

    dictionary = {}

    dictionary[dataframe.columns[0]] = date_and_time
    dictionary[dataframe.columns[2]] = dataframe[dataframe.columns[2]]

    return px.line(dictionary, x = dataframe.columns[0], y = dataframe.columns[2])

#Displays the graph based on the attribute selected in the dropdown. 
@app.callback([dash.dependencies.Output('scatter-chart', 'figure'), dash.dependencies.Output('fig-error', 'children')], [dash.dependencies.Input('date-pick-range', 'start_date'), 
dash.dependencies.Input('date-pick-range', 'end_date'), dash.dependencies.Input('attribute-dropdown', 'value'), dash.dependencies.Input('year-dropdown', 'value')])
def update_graf(start_date, end_date, atr_value, year_value):
    '''Updates the graph based on attributes and/or dates'''

    #Find out whether the user has chosen an interval or an entire year
    if atr_value is not None and start_date is not None and end_date is not None:
        data_frames = data.get_ranged_df(str(start_date), str(end_date))
    elif atr_value is not None and year_value is not None:
        start_date = str(year_value) + '-01-01' #The first of January the given year
        end_date = str(year_value) + '-12-12' #The last of December the given year
        data_frames = data.get_ranged_df(str(start_date), str(end_date))
    else:
        #If all of the parameters are not null, we can't create a graph, so we return an empty graph and an error message. 
        return {'data': []}, "Please choose both an attribute and some form of time interval"

    #Find which attribute is selected by the user
    frame_num = 0
    for data_frame in data_frames:
        if data_frame.columns[2] == atr_value: 
            break #Right graph found, break out. 
        frame_num += 1 #Otherwise increment counter and keep looking.     

    fig = generateGraph(data_frames[frame_num])

    #fig = px.line(data_frames[frame_num], x = data_frames[frame_num].columns[1], y = data_frames[frame_num].columns[2]) #Make the graph
    text = "" #text is only for errors, but since it is an output we have to return something
    return fig, text

#Callback that disables the date range picker if a year is selected in the drodown menu.
@app.callback(dash.dependencies.Output('date-pick-range', 'disabled'), [dash.dependencies.Input('year-dropdown', 'value')])
def date_range_set_enabled_state(value):
    '''Disables the date range picker if a year is selected in the dropdown'''

    if value is not None:
        return True

#Callback that disables the year dropdown if a date range is selected. 
@app.callback(dash.dependencies.Output('year-dropdown', 'disabled'), [dash.dependencies.Input('date-pick-range', 'start_date'), 
dash.dependencies.Input('date-pick-range', 'end_date')])
def year_dropdown_set_enabled_state(start_date, end_date):
    '''Disables the dropdown menu to select a year if a date interval is selected'''

    if start_date is not None and end_date is not None:
        return True


if __name__ == '__main__':
    app.run_server(debug=True)