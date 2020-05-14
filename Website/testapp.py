# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Fuck SMHI'),


    html.Label('Välj en stad'),
    dcc.Dropdown(
        id='dropdown2',
        options=[
            {'label': i, 'value' : i} for i in ['KSD', 'KNA', 'GTB']],
            placeholder= 'Välj en stad',
            multi=True
    ),
    html.Div(id='dd-output-container'),
    html.Br(),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),

])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('dropdown2', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value), html.Br(), 1+1

if __name__ == '__main__':
    app.run_server(debug=True)