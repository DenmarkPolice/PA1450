import dash
from server import server

app = dash.Dash(name='weather', sharing=True,
                server=server, url_base_pathname='/weather')
