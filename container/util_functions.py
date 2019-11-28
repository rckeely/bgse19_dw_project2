import pandas as pd

from optimizer import *
from PIL import Image
from io import BytesIO
import base64

import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

### Util Functions ###
def get_full_name(short_code):
    full_names = { "ARI" : "Arizona Cardinals",
    "ATL" : "Atlanta Falcons",
    "BAL" : "Baltimore Ravens",
    "BUF" : "Buffalo Bills",
    "CAR" : "Carolina Panthers",
    "CHI" : "Chicago Bears",
    "CIN" : "Cincinnati Bengals",
    "CLE" : "Cleveland Browns",
    "DAL" : "Dallas Cowboys",
    "DEN" : "Denver Broncos",
    "DET" : "Detroit Lions",
    "GB" : "Green Bay Packers",
    "HOU" : "Houston Texans",
    "IND" : "Indianapolis Colts",
    "JAX" : "Jacksonville Jaguars",
    "KC" : "Kansas City Chiefs",
    "LAC" : "Los Angeles Chargers",
    "LAR" : "Los Angeles Rams",
    "MIA" : "Miami Dolphins",
    "MIN" : "Minnesota Vikings",
    "NE" : "New England Patriots",
    "NO" : "New Orleans Saints",
    "NYG" : "New York Giants",
    "NYJ" : "New York Jets",
    "OAK" : "Oakland Raiders",
    "PHI" : "Philadelphia Eagles",
    "PIT" : "Pittsburgh Steelers",
    "SF" : "San Francisco 49ers",
    "SEA" : "Seattle Seahawks",
    "TB" : "Tampa Bay Buccaneers",
    "TEN" : "Tennessee Titans",
    "WAS" : "Washington ********" }
    return full_names[short_code]


def get_thumbnail(short_code):
   i = Image.open(f"assets/{short_code}.png")
   i.thumbnail((60, 60), Image.LANCZOS)
   buff = BytesIO()
   i.save(buff, format="PNG")
   encoded_image = base64.b64encode(buff.getvalue()).decode('UTF-8')
   print('got a thumbnail.') # for debugging
   return (html.Div(className="team_names", children=[html.Img(src='data:image/png;base64,{}'.format(encoded_image),
                            className="team_logos"),
                    get_full_name(short_code)]))


def initialize_thumbnails(static_df):
    output = static_df[['ShortCode']]
    thumbs = output['ShortCode'].map(get_thumbnail)
    output.loc[:, 'Team'] = pd.Series(thumbs, index=output.index) #this is causing the "slice" warning in terminal
    output = output.rename(columns={'ShortCode': 'team'})

    return output


def generate_table_df(longdata, week_start, week_end, blocked_teams, thumbnails = None, results_df = None):
    results_df = optimize_season(longdata, week_start=week_start,
                                 week_end=week_end, blocked_teams=blocked_teams)

    longdata = longdata[['week', 'team', 'elo']]
    output = results_df.merge(longdata, how='left')
    # output['image'] = output['team'].map(str) + '.png'
    if thumbnails is None:
        output['Team'] = output['team']
    else:
        output = output.merge(thumbnails, how='left')

    output['WinProb'] = ["{:.1%}".format(x) for x in output.prob]
    output['ELO'] = output.elo.astype('int')

    output = output.rename(columns={'week': 'Week'})

    output = output[['Week', 'Team', 'ELO', 'WinProb']]
    return output


def fix_strings(string_var, start=False):
    if string_var == '':
        if start:
            string_var = 1
        else:
            string_var = 17
    else:
        string_var = int(string_var)
    return string_var


### App Layout Functions ###
def get_selector_div(longdata, week_start, week_end, blocked_teams, static_df):
    return html.Div(className="map_div", children=[
        dcc.Graph(
            id='graph-1-tabs',
            figure={
                'data': [go.Scattergeo(
                    lon=static_df['Longitude'],
                    lat=static_df['Latitude'],
                    text=static_df['TeamName'],
                    mode='markers')],
                'layout': go.Layout(geo_scope='usa',
                                    width=1000,
                                    height=600)
            })])


def get_table_div(longdata, results_df, week_start, week_end, blocked_teams, thumbnails):
    week_start = fix_strings(week_start, start=True)
    week_end = fix_strings(week_end)
    results_df = generate_table_df(longdata, week_start=week_start, week_end=week_end,
                                   blocked_teams=blocked_teams, thumbnails=thumbnails, results_df=results_df)
    return html.Div(className="render_div", children=
                dbc.Table.from_dataframe(df=results_df,
                                    id="main_table"))


def get_projections_graph(longdata, results_df, week_start, week_end, blocked_teams,thumbnails):
    week_start = fix_strings(week_start, start=True)
    week_end = fix_strings(week_end)

    graph_df = generate_table_df(longdata, week_start=week_start, week_end=week_end,
                                 blocked_teams=blocked_teams, thumbnails=thumbnails,results_df=results_df)

    graph_df['wp'] = [float(i[:(len(i)-1)]) / 100 for i in graph_df.WinProb]

    graph_df['Optimized'] = graph_df.wp.cumprod()


    output = html.Div(className = 'proj_graph',children=
        dcc.Graph(
            figure=dict(
                data=[
                    dict(
                        x=graph_df['Week'],
                        y=graph_df['Optimized'],
                        #text=graph_df['Team'],
                        name='Optimized',
                        marker=dict(
                            color='rgb(55, 83, 109)'
                        ),
                        fill='tozeroy'
                    )
                ],
                layout=dict(
                    title='Cumulative Survival Likelihood',
                    font = dict(family= "Courier New, monospace",
                            size=18,
                            color='#7f7f7f'),
                    xaxis = {'title': 'Week',
                             'range': [week_start,week_end]},
                    yaxis = {'range': [0,1],
                             'tickformat': ',.0%'},
                    showlegend=False,
                    legend=dict(
                        x=0,
                        y=1.0
                    ),
                    margin=dict(l=50, r=0, t=100, b=30)
                )
            ),
            style={'height': 450},
            id='projections-graph'
        ))

    return output
