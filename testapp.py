# -*- coding: utf-8 -*-
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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Historical weather data provided by SMHI'),


    dcc.Dropdown(
        id='Multi-dropdown',
        options=[
            {'label': 'Temperatur', 'value': 'TEMP'},
            {'label': 'Nederbörd', 'value': 'NED'},
            {'label': 'Solskenstid', 'value': 'SOL'},
        ],
        placeholder='Pick attributes',
        multi=True
    ),
    html.Br(),

    dcc.Dropdown(id='year-dropdown',options=[{'label':x, 'value': x} for x in range(2009, 2020)], placeholder='If you want to select an entire year, please do so here'),
    html.Div(id='year-dropdown-output'),
    html.Br(),

    html.Div('''If you would rather want to display the data between two dates, please choose those dates here'''),
    dcc.DatePickerRange(
        id='date-pick-range',
        min_date_allowed=dt(2009, 8, 5),
        max_date_allowed=dt.now(),
        initial_visible_month=dt(2019, 11, 11),
        display_format='DD/MM/YYYY',
        clearable=True,
    ),
    html.Div(id='output-date-range'),
    html.Br(),

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

    html.Div(id='output-data-upload'),

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
])

#Callback for the dropdown menu that displays years.
@app.callback(
    dash.dependencies.Output('year-dropdown-output', 'children'),
    [dash.dependencies.Input('year-dropdown', 'value')])
def update_output(value):
    return 'You have selected the entire year of {}'.format(value)


#Callback for date range picker
@app.callback(
    dash.dependencies.Output('output-date-range', 'children'),
    [dash.dependencies.Input('date-pick-range', 'start_date'),
     dash.dependencies.Input('date-pick-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

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