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

# app.layout = html.Div([
#     html.H1('Hello Dash'),
#     html.Div([
#         html.P('Dash converts Python classes into HTML'),
#         html.P('This conversion happens behind the scenes by Dashs JavaScript front-end')
#     ])
# ])


results_df = pd.read_csv('dummy_results.csv')
weeks = results_df['week']
team = results_df['team']
all_weeks = range(1,17+1)

app.layout = \
    html.Div([
        dbc.Row(dbc.Col(html.Div("Hatch's Eliminator/Survivor Optimisation"))),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Button('Optimise!', id='button'),
                        html.Br(),
                    ]),
                    html.Div([
                        html.P('Enter current league week:'),
                        dcc.Dropdown(
                            id='current_week',
                            options=[{'label': str(i), 'value': i} for i in weeks],
                            value='',
                            placeholder="Current week",
                            multi=True
                        ),
                        html.Br()
                    ]),
                    html.Div([
                        html.P('Optimise through week:'),
                        dcc.Dropdown(
                            id='target_week',
                            options=[{'label': str(i), 'value': i} for i in all_weeks],
                            value='',
                            placeholder='Final week',
                            multi=True
                        ),
                        html.Br()
                    ]),
                    html.Div([
                        html.Label('Checkboxes'),
                        html.Br(),
                    	dcc.Checklist(options=[
                                     {'label': 'CHI', 'value': 'CHI'},
                                     {'label': 'BAL', 'value': 'BAL'},
                                     {'label': 'DAL', 'value': 'DAL'},
                                     {'label': 'CHI', 'value': 'LAR'},
                                     {'label': 'BAL', 'value': 'PHI'},
                                     {'label': 'DAL', 'value': 'NE'},
                                     {'label': 'DAL', 'value': 'BUF'},
                                     {'label': 'DAL', 'value': 'NO'},
                                     {'label': 'DAL', 'value': 'SEA'},
                                     ],
                                     value=[]),
                    ]),
                ]),
            ]),
            dbc.Col(html.Div("Main panel"))
            ]),
    ])
app.run_server(debug=True)
