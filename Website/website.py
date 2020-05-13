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
            html.A("Link1"),
            html.A("Link2"),
            html.A("Link3")
        ])
    ])




])









if __name__ == '__main__':
    website.run_server(debug=True)