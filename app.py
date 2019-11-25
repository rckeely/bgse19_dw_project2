import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.graph_objects as go

from dash.dependencies import Input, Output

import os
from optimizer import *
from transform_elo import *

app = dash.Dash('dash-tutorial')

#Get data
mydata = pd.read_csv('data/elo/nfl_elo.csv')
teams_full = pd.read_csv('configs/teams.csv')

mydata = transform_elo_data(mydata)
teams = teams_full['abb']

blocked_teams = ['BAL']

results_df = optimize_season(mydata, week_start=1, week_end=17, blocked_teams=blocked_teams)

SEASON_LENGTH = 17
weeks = list(range(1, SEASON_LENGTH + 1))
target_weeks = list(range(1, SEASON_LENGTH + 1))

# Colours
# Dark Grey #5d5c61
# Light Grey #39683
# Light blue #7395ae
# Dark blue #557a95
# Sand #b1a296
app.layout = \
    html.Div(className="container", children=[
        dbc.Row(dbc.Col(html.Div(className="mastHead",
                                children=[html.H1(className="mastHead", children=[html.Img(className="logo",
                                                                                        src=app.get_asset_url ('nfl-league-logo.png'),),
                                                    f"Hatch's Eliminator/Survivor Optimisation",]),]))),
        dbc.Row([
            dbc.Col([
                html.Div(className="sidePanel", children=[
                    html.Div(className="subcomponent", children=[
                        html.Button('Optimise!', id='button'),
                        html.Br(),
                    ]),
                    html.Div(className="subcomponent", children=[
                        html.H3('Enter current league week:', className="sidePanel"),
                        dcc.Dropdown(
                            id='current_week',
                            options=[{'label': str(i), 'value': i} for i in weeks],
                            value='',
                            placeholder="Current week",
                            multi=False
                        ),
                        html.Br()
                    ]),
                    html.Div(className="subcomponent", children=[
                        html.H3('Optimise through week:', className="sidePanel"),
                        dcc.Dropdown(
                            id='target_week',
                            options=[{'label': str(i), 'value': i} for i in target_weeks],
                            value='',
                            placeholder='Final week',
                            multi=False
                        ),
                        html.Br()
                    ]),
                    html.Div(className="subcomponent", children=[
                        html.H3('Select Teams:', className="sidePanel"),
                        dcc.Checklist(id='teams',
                                      options=[{'label': str(i), 'value': i} for i in teams],
                                      value=[]
                                     ),
                        html.Br(),
                    ]),
                ]),
            ]),
            dbc.Col([
                html.Div(className="mainPanel", children=[
                	html.Div([
                    	#html.Label('Table'),
                    	dbc.Table.from_dataframe(results_df,
                                                id="mainTable")
                	])
            	]),
            ])
        ]),
        dbc.Row(dbc.Col(html.Div(className="footer",
                                children=[html.H1("Footer",
                                                className="footer")]))),
    ])
app.run_server(debug=True)
