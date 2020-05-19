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

def CorrectifyDataframe(dataframe):
    newFrameDict = {dataframe.columns[0] : dataframe[dataframe.columns[0]], dataframe.columns[1] : dataframe[dataframe.columns[1]], dataframe.columns[2] : dataframe[dataframe.columns[2]]}
    dataframe = pd.DataFrame(newFrameDict)
    print(dataframe)
    return dataframe

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

    dbc.Button("How to format your own csv-file", id="open"),
        dbc.Modal(
            [
                dbc.ModalHeader("How to upload your own csv-file"),
                dbc.ModalBody('If you would like to use your own csv-file to display data it has to be formatted in the right way.'),
                dbc.ModalBody('The format that is used on this website is as follows:'),
                dbc.ModalBody(''),
                dbc.ModalBody('Datum,Tid (UTC),xyz'),
                dbc.ModalBody(''),
                dbc.ModalBody('Where xyz stands for the attribute of the csv-file, for example temperature.'),
                dbc.ModalBody(''),
                dbc.ModalBody('Once you have made sure that your csv-file is formatted this way, please use the box above to upload your file.'),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            size="sm"
        ),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
])


def generateGraph(dataframes):
    '''Returns a px fig for the graph'''

    fig = go.Figure()
    for dataframe in dataframes:
        
        date_and_time = []
        for i in range(len(dataframe[dataframe.columns[0]])):
            date_and_time.append(dataframe.iat[i,0] + " " + dataframe.iat[i,1])
        dictionary = {}
        dictionary[dataframe.columns[0]] = date_and_time
        listan = []
        if dataframe.columns[2] == 'Solskenstid':
            for i in dataframe[dataframe.columns[2]]:
                listan.append(i/60)
            dictionary[dataframe.columns[2]] = listan
        else:
            dictionary[dataframe.columns[2]] = dataframe[dataframe.columns[2]]
        
        fig.add_trace(go.Scatter(x=dictionary[dataframe.columns[0]], y = dictionary[dataframe.columns[2]], mode='lines', name= dataframe.columns[2]))
    fig.update_layout(title ="Test", xaxis_title = "Tid", yaxis_title = "Värde")
        
    #fig = px.line(dictionary, x = dataframe.columns[0], y = dataframe.columns[2])
   
    return fig

#Testing function for correctly formatting csv files



#correctDF = CorrectifyDataframe(pd.read_csv("Nederbordsmang_noformat.csv", skiprows = 9, sep = ';'))


    

#Displays the graph based on the attribute selected in the dropdown. 
# @app.callback([dash.dependencies.Output('scatter-chart', 'figure'), dash.dependencies.Output('fig-error', 'children')], [dash.dependencies.Input('date-pick-range', 'start_date'), 
# dash.dependencies.Input('date-pick-range', 'end_date'), dash.dependencies.Input('attribute-dropdown', 'value'), dash.dependencies.Input('year-dropdown', 'value')])
# def update_graf(start_date, end_date, atr_value, year_value):
#     '''Updates the graph based on attributes and/or dates'''

#     #Find out whether the user has chosen an interval or an entire year
#     if atr_value is not None and start_date is not None and end_date is not None:
#         data_frames = data.get_ranged_df(str(start_date), str(end_date))
#     elif atr_value is not None and year_value is not None:
#         start_date = str(year_value) + '-01-01' #The first of January the given year
#         end_date = str(year_value) + '-12-12' #The last of December the given year
#         data_frames = data.get_ranged_df(str(start_date), str(end_date))
#     else:
#         #If all of the parameters are not null, we can't create a graph, so we return an empty graph and an error message. 
#         return {'data': []}, "Please choose both an attribute and some form of time interval"

#     #Find which attribute is selected by the user
#     frame_num = 0
#     for data_frame in data_frames:
#         if data_frame.columns[2] == atr_value: 
#             break #Right graph found, break out. 
#         frame_num += 1 #Otherwise increment counter and keep looking.     

#     fig = generateGraph(data_frames[frame_num])

#     #fig = px.line(data_frames[frame_num], x = data_frames[frame_num].columns[1], y = data_frames[frame_num].columns[2]) #Make the graph
#     text = "" #text is only for errors, but since it is an output we have to return something
#     return fig, text

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
        #If all of the parameters are not null, we can't create a graph, so we return an empty graph and an error message. 
        return {'data': []}, "Please choose both an attribute and some form of time interval"

    #Find which data frames are selected
    frame_nums = []
    for attribute in atr_values:
        frame = 0
        for data_frame in data_frames:
            if data_frame.columns[2] == attribute:
                frame_nums.append(frame)
                break
            frame += 1

    #print(frame_nums)

    frame_list = []
    for i in frame_nums:
        frame_list.append(data_frames[i])


    fig = generateGraph(frame_list)

    # fig = go.Figure()
    # fig.update_layout(showlegend=True)
    # for frame in frame_nums:
    #     fig.add_scatter(generateGraph(data_frames[frame]))

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

#Callback for the modal window
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#Parses the contents of the uploaded csv file
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    #Assuming that this Div creates the table that is displayed
    return html.Div([
        html.H5(filename),
        html.H6(dt.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

#Displays the table generated for the uploaded csv file.
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)