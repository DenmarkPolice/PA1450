# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import re


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

website = dash.Dash(__name__, external_stylesheets=external_stylesheets)

website.layout = html.Div(children = [
    html.Label('Paremeter'),
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
    html.Div(id='output-container-date-picker-range')




])


@website.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('dropdown2', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    website.run_server(debug=True)