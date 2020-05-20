import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
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
from flask import send_file

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
        multi=True
    ),
    html.Br(),

    #Dropdown for yearly interval
    dcc.Dropdown(id='year-dropdown',options=[{'label':x, 'value': x} for x in range(2009, 2021)], placeholder='If you want to select an entire year, please do so here'),
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
    html.Br(),

    html.Div(id='output-data-upload'),
    html.Div(id='fig-error'),
    #The generated graph
    dcc.Graph(
        id='scatter-chart',
        figure = fig      
    ),
    html.Br(),
    html.Button(id='excel-button', n_clicks=0, children='Make excel'),
    #html.A(href='download_excel', children='Download File'),
])

@app.callback(dash.dependencies.Output('excel-button', 'style'), [dash.dependencies.Input('excel-button', 'n_clicks')])
def make_excel(n_clicks):
    raise dash.exceptions.PreventUpdate('Cancel callback')
    weatherdata.makeExcel()

#Feature coming in the future
# @app.server.route('/dash/urlToDownload')
# def download_excel():

#     strIO = io.BytesIO()
#     excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")

#     weatherdata.makeExcel()
#     excel_writer.save()
#     excel_data = strIO.getvalue()
#     strIO.seek(0)

#     return send_file(strIO, mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', attachment_filename='report.xlsx', as_attachment=True, cache_timeout=0)



def generate_graph(data_frames):
    '''Returns a px fig for the graph'''

    fig = go.Figure()
    for data_frame in data_frames:
        
        date_and_time = []
        for i in range(len(data_frame[data_frame.columns[0]])):
            date_and_time.append(data_frame.iat[i,0] + " " + data_frame.iat[i,1])
        dictionary = {}
        dictionary[data_frame.columns[0]] = date_and_time
        listan = []
        if data_frame.columns[2] == 'Solskenstid':
            for i in data_frame[data_frame.columns[2]]:
                listan.append(i/3600)
            dictionary[data_frame.columns[2]] = listan
        else:
            dictionary[data_frame.columns[2]] = data_frame[data_frame.columns[2]]
        
        fig.add_trace(go.Scatter(x=dictionary[data_frame.columns[0]], y = dictionary[data_frame.columns[2]], mode='lines', name= data_frame.columns[2]))
    fig.update_layout(title ="Test", xaxis_title = "Tid", yaxis_title = "Värde")

    return fig

@app.callback([dash.dependencies.Output('scatter-chart', 'figure'), dash.dependencies.Output('fig-error', 'children')], [dash.dependencies.Input('date-pick-range', 'start_date'), 
dash.dependencies.Input('date-pick-range', 'end_date'), dash.dependencies.Input('attribute-dropdown', 'value'), dash.dependencies.Input('year-dropdown', 'value')])
def update_graf(start_date, end_date, atr_values, year_value):
    '''Updates the graph based on attributes and/or dates'''

    #Find out whether the user has chosen an interval or an entire year
    if atr_values is not None and start_date is not None and end_date is not None:
        data_frames = data.get_ranged_df(str(start_date), str(end_date))
    elif atr_values is not None and year_value is not None:
        start_date = str(year_value) + '-01-01' #The first of January the given year
        end_date = str(year_value) + '-12-12' #The last of December the given year
        data_frames = data.get_ranged_df(str(start_date), str(end_date))
    else:
        #If none of the above if statements are true we can't make a graph, return an empty graph and an error message
        return {'data': []}, "Please choose both an attribute and some form of time interval"

    #Find which data frames indexes are selected
    frame_nums = []
    for attribute in atr_values:
        frame = 0
        for data_frame in data_frames:
            if data_frame.columns[2] == attribute:
                frame_nums.append(frame)
                break
            frame += 1

    frame_list = []
    for i in frame_nums:
        frame_list.append(data_frames[i])

    #Generate the graph 
    fig = generate_graph(frame_list)

    text = "" #text is only for errors, but since it is an output in the callback we have to return something
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