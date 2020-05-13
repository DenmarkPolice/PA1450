# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

website = dash.Dash(__name__, external_stylesheets=external_stylesheets)

website.layout = html.Div(children = [
    html.Div(className = "dropdown", children = [
        html.Button("Dropdown", className = "dropbtn"),
        html.Div(className = "dropdown-content", children = [
            html.P("Soltimmar"),
            html.P("Nederbörd"),
            html.P("Temperatur")
        ])
    ]),

    dcc.Dropdown(
        id='dropdown2',
        options=[
            {'label': i, 'value' : i} for i in ['KSD', 'KNA', 'GTB']],
            value = 'KSD'
    ),
    html.Div(id='dd-output-container'),
    html.Br()
])


# @app.callback(
#     dash.dependencies.Output('dd-output-container', 'children'),
#     [dash.dependencies.Input('dropdown2', 'value')])
# def update_output(value):
#     return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    website.run_server(debug=True)