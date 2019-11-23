import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
#import records
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
app = dash.Dash('dash-tutorial')

results_df = pd.read_csv('dummy_results.csv')
weeks = results_df['week']
teams = results_df['team']
max_weeks = 17
target_weeks = range(1,max_weeks+1)

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
                            options=[{'label': str(i), 'value': i} for i in target_weeks],
                            value='',
                            placeholder='Final week',
                            multi=True
                        ),
                        html.Br()
                    ]),
                    html.Div([
                        html.Label('Checkboxes'),
                        html.Br(),
                    	dcc.Checklist(id='teams',
                                      options=[{'label': str(i), 'value': i} for i in teams],
                                      value=[]
                                     ),
                    ]),
                ]),
            ]),
            dbc.Col([
                html.Div([
                	html.Div([
                    	html.Label('Table'),
                    	dbc.Table.from_dataframe(results_df,
                                                striped=True,
                                                bordered=True,
                                                hover=True)
                    	])
                	]),
                ])
            ]),
    ])
app.run_server(debug=True)
