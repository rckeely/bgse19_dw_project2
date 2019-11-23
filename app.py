import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
#import records
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
app = dash.Dash('dash-tutorial')
#analytics = records.Database('postgres://postgres@0.0.0.0/analytics')
#res = analytics.query('select * from order_facts LEFT JOIN dates ON date_id = id')
#df = pd.DataFrame(res.as_dict())
app.layout = html.Div(className = 'layout', children =
    [
        dbc.Row(dbc.Col(html.Div("A single column"))),
        dbc.Row(
            [
                dbc.Col(className = 'sidePanel', children =
                [
                    html.Div("Side columns"),
                ]),
                dbc.Col(className = 'mainPanel', children =
                [
                    html.Div("Main Panel"),
                ])
            ]
        ),
    ])
app.run_server(debug=True)
