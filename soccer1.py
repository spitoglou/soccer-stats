"""
# Python Handout
Turn Python scripts into handouts with Markdown comments and inline figures. An
alternative to Jupyter notebooks without hidden state that supports any text
editor.
"""
# handout: begin-exclude
# import pandas as pd
# import numpy as np

import handout
from sp_soccer_lib.championships import load_england, load_italy, team_stats, load_country
from sp_soccer_lib.handout_helpers import style
from sp_soccer_lib import create_team_df_dict, championship_teams


def make_link(row):
    return '<a href="./{0}/index.html">Link</a>'.format(row['index_col'])


def add_logo(row):
    return '<img src="https://kassiesa.net/uefa/clubs/images/{0}.png" alt="Logo" height="42" width="42">{0}'.format(row['HomeTeam'])


def get_country_header(country):
    if country == 'england':
        return '<img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/Premier_League_Logo.svg/1920px-Premier_League_Logo.svg.png" alt="Logo" width="100%">'
    else:
        return '<h2>{0}</h2>'.format(country)


countries = ['greece', 'italy', 'england']

for country in countries:
    doc = handout.Handout('handout/' + country)
    doc.add_html(get_country_header(country))
    styling = style()
    doc.add_html(styling)
    df = load_country(country)
    team_dfs = create_team_df_dict(df)
    stats = team_stats(team_dfs)
    stats['index_col'] = stats.index
    # stats['link'] = '<a href="/{0}">Link</a>'.format(stats['index_col'])
    stats['link'] = stats.apply(lambda row: make_link(row), axis=1)
    columns_to_show = ['1920_wins', '1920_draws', '1920_losses', '1920_points', 'CurrentNoDraw', 'MaxNoDraw', 'link']
    doc.add_html(stats.to_html(columns=columns_to_show, escape=False))
    doc.show()

    teams = championship_teams(df)
    for team in teams:
        doc = handout.Handout('handout/' + country + '/' + team)
        doc.add_html(styling)
        team_matches = team_dfs[team]
        # team_matches['HomeTeam'] = team_matches.apply(lambda row: add_logo(row), axis=1)
        doc.add_html(team_matches.iloc[::-1].to_html(escape=False))
        doc.show()


england = load_england()
print(england)
eng_team_dfs = create_team_df_dict(england)
print(eng_team_dfs['Arsenal'])
print(eng_team_dfs['Wolves'])

italy = load_italy()
print(italy)
it_team_dfs = create_team_df_dict(italy)
print(it_team_dfs['Juventus'])
print(it_team_dfs['Napoli'])
team_stats(it_team_dfs).to_html('test.html')

# handout: end-exclude
