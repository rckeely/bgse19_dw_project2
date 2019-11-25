from optimizer import *

def generate_table_df(longdata,week_start,week_end,blocked_teams):
    import pandas as pd

    results_df = optimize_season(longdata, week_start=1, week_end=17, blocked_teams=blocked_teams)
    longdata = longdata[['week','team','elo']]
    output = results_df.merge(longdata,how='left')

    output['WinProb'] = ["{:.1%}".format(x) for x in output.prob]
    output['ELO'] = output.elo.astype('int')

    output = output.rename(columns={'week':'Week','team':'Team'})

    output = output[['Week','Team','ELO','WinProb']]
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


def get_table_div(longdata, week_start, week_end, blocked_teams):
    import dash
    import dash_html_components as html
    import dash_core_components as dcc
    import dash_bootstrap_components as dbc

    week_start = fix_strings(week_start, start=True)
    week_end = fix_strings(week_end)
    results_df = generate_table_df(longdata, week_start=week_start,
                                   week_end=week_end, blocked_teams=blocked_teams)
    return html.Div(
                dbc.Table.from_dataframe(df=results_df,
                                    id="main_table"))
