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

results_df = pd.DataFrame()

app = dash.Dash('NFL Survivor Pool Optimiser')
#app.config.suppress_callback_exceptions = True
app.title = 'NFL Survivor Pool Optimiser'
#Get data
mydata = pd.read_csv('data/elo/nfl_elo.csv')
teams_full = pd.read_csv('configs/teams.csv')

longdata = transform_elo_data(mydata)
static_df = pd.read_csv('data/nfl_lookup_table.csv')
teams = teams_full['abb']

blocked_teams = []

SEASON_LENGTH = 17
weeks = list(range(1, SEASON_LENGTH + 1))
target_weeks = list(range(1, SEASON_LENGTH + 1))

x = generate_table_df(longdata, week_start=1,
                      week_end=17, blocked_teams=blocked_teams)

# Colours
# Dark Grey #5d5c61
# Light Grey #39683
# Light blue #7395ae
# Dark blue #557a95
# Sand #b1a296
app.layout = \
    html.Div(className="container", children=[
        dbc.Row(dbc.Col(html.Div(className="mast_head",
                children=[html.H1(className="mast_head",
                                children=[html.Img(className="logo",
                                                   src=app.get_asset_url('nfl-league-logo.png'),),
                                         f"NFL Survivor Pool Optimiser",]),
                        html.Hr(className="mast_head")]))),
        dbc.Row([
            dbc.Col([
                html.Div(className="side_panel", children=[
                    html.Div(className="subcomponent", children=[
                        html.H3('Enter current league week:', className="side_panel"),
                        dcc.Dropdown(
                            id='current_week',
                            options=[{'label': str(i), 'value': i} for i in weeks],
                            value='',
                            placeholder="Current week",
                            multi=False,
                            className="side_controls"
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
                            multi=False,
                            className="side_controls"
                        ),
                        html.Br()
                    ]),
                    html.Div(className="subcomponent", children=[
                        html.H3('Block Teams:', className="side_panel"),
                        dcc.Checklist(id='blocked_teams',
                                      options=[{'label': get_full_name(i) , 'value': i} for i in teams],
                                      value=[],
                                      className="check_list"
                                     ),
                        html.Br(),
                    ]),
                ]),
            ]),
            dbc.Col([
                html.Div(className="main_panel", children=[
                	html.Div([
                        html.Div(id="headline_stats", className="headline_stats"),
                    	dcc.Tabs(id="tabs-example", value='probabilities_table', children=[
                            dcc.Tab(label='Team Location', value='team_selector'),
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

def get_selector_div(longdata, week_start, week_end, blocked_teams, static_df):
     return html.Div(className="render_div", children=[
        # html.Div(className="subcomponent", children=[
        #         dcc.Checklist(id='blocked_teams',
        #                       options=[{'label': str(i), 'value': i} for i in teams],
        #                       value=[],
        #                       className="check_list"
        #                      ),
        # ]),
        dcc.Graph(
            id='graph-1-tabs',
            figure={
                'data': [go.Scattergeo(
                        lon = static_df['Longitude'],
                        lat = static_df['Latitude'],
                        text = static_df['TeamName'],
                        mode = 'markers')],
                'layout': go.Layout(geo_scope='usa')
                })])

@app.callback([Output('tabs-content-example', 'children'),
               Output('headline_stats', 'children')],
              [Input('tabs-example', 'value'),
               Input('current_week', 'value'),
               Input('target_week', 'value'),
               Input('blocked_teams', 'value')])
def render_content(tab, week_start, week_end, blocked_teams):
    if tab == 'team_selector':
        result = get_selector_div(longdata, week_start, week_end, blocked_teams, static_df)
    elif tab == 'probabilities_table':
        result = get_table_div(longdata, results_df, week_start, week_end, blocked_teams)
    elif tab == 'projections_graph':
        result = get_projections_graph(longdata, results_df, week_start, week_end, blocked_teams)
    return result, "hello"

app.run_server(debug=True)
