# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Fuck SMHI'),


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
 
    dcc.DatePickerRange(
        id='date-pick-range',
        min_date_allowed=dt(2009, 8, 5),
        max_date_allowed=dt(2020, 2, 1),
        initial_visible_month=dt(2019, 11, 11),
        display_format='DD/MM/YYYY'
    ),
    html.Div(id='output-date-range')
])


if __name__ == '__main__':
    app.run_server(debug=True)


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