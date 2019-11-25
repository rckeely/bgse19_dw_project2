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
from util_functions import *

app = dash.Dash('dash-tutorial')

#Get data
mydata = pd.read_csv('data/elo/nfl_elo.csv')
teams_full = pd.read_csv('configs/teams.csv')

longdata = transform_elo_data(mydata)
teams = teams_full['abb']

blocked_teams = []

SEASON_LENGTH = 17
weeks = list(range(1, SEASON_LENGTH + 1))
target_weeks = list(range(1, SEASON_LENGTH + 1))

x = get_table_div(longdata,1,17,blocked_teams=blocked_teams)

# Colours
# Dark Grey #5d5c61
# Light Grey #39683
# Light blue #7395ae
# Dark blue #557a95
# Sand #b1a296
app.layout = \
    html.Div(className="container", children=[
        dbc.Row(dbc.Col(html.Div(className="mast_head",
                                children=[html.H1(className="mast_head", children=[html.Img(className="logo",
                                                                                        src=app.get_asset_url ('nfl-league-logo.png'),),
                                                    f"Hatch's Eliminator/Survivor Optimisation",]),]))),
        dbc.Row([
            dbc.Col([
                html.Div(className="side_panel", children=[
                    # html.Div(className="subcomponent", children=[
                    #     html.Button('Optimise!', id='button'),
                    #     html.Br(),
                    # ]),
                    html.Div(className="subcomponent", children=[
                        html.H3('Enter current league week:', className="side_panel"),
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
                        html.H3('Optimise through week:', className="side_panel"),
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
                        html.H3('Select Teams:', className="side_panel"),
                        dcc.Checklist(id='blocked_teams',
                                      options=[{'label': str(i), 'value': i} for i in teams],
                                      value=[]
                                     ),
                        html.Br(),
                    ]),
                ]),
            ]),
            dbc.Col([
                html.Div(className="main_panel", children=[
                	html.Div([
                    	dcc.Tabs(id="tabs-example", value='team_selector', children=[
                            dcc.Tab(label='Team Selector', value='team_selector'),
                            dcc.Tab(label='Probabilities Table', value='probabilities_table'),
                            dcc.Tab(label='Projections Graph', value='projections_graph'),
                        ]),
                        html.Div(id='tabs-content-example', className='tab_content')
                	])
            	]),
            ])
        ]),
        dbc.Row(dbc.Col(html.Div(className="footer",
                                children=[html.H1("Footer",
                                                className="footer")]))),
    ])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value'),
               Input('current_week', 'value'),
               Input('target_week', 'value'),
               Input('blocked_teams', 'value')])
def render_content(tab, week_start, week_end, blocked_teams):
    if tab == 'team_selector':
        result = html.Div(className="render_div", children=[
            html.H3('Tab content 1'),
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [3, 1, 2],
                        'type': 'bar'
                    }]
                }
            )
        ])
    elif tab == 'probabilities_table':
        result = get_table_div(longdata, week_start, week_end, blocked_teams)
    elif tab == 'projections_graph':
        result = html.Div(className="render_div", children=[
            html.H3('Tab content 3'),
            dcc.Graph(
                id='graph-3-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])
    return result
app.run_server(debug=True)
