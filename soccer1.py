# handout: begin-exclude
import pandas as pd
import matplotlib.pyplot as plt
# import numpy as np
from collections import Counter

import handout
import statistics
from sp_soccer_lib.championships import load_england, load_italy, team_stats, load_country
from sp_soccer_lib.handout_helpers import style, get_country_header, make_link
from sp_soccer_lib import create_team_df_dict, championship_teams, no_draw_frequencies


countries = ['greece', 'italy', 'england', 'spain', 'germany', 'france']
doc = handout.Handout('handout')
for country in countries:
    doc.add_html(
        '<a href="./{0}/index.html">{1}</a>'.format(country, get_country_header(country)))
doc.show()


for country in countries:
    doc = handout.Handout('handout/' + country)
    doc.add_html(get_country_header(country))
    styling = style()
    doc.add_html(styling)
    df = load_country(country)
    team_dfs = create_team_df_dict(df)
    stats = team_stats(team_dfs)
    stats['index_col'] = stats.index
    stats['link'] = stats.apply(lambda row: make_link(row), axis=1)
    stats = stats.rename(columns={
        '1920_wins': 'W',
        '1920_draws': 'D',
        '1920_losses': 'L',
        '1920_gf': 'GF',
        '1920_ga': 'GA',
        '1920_points': 'PTS'
    })
    columns_to_show = ['W', 'D', 'L', 'GF', 'GA',
                       'PTS', 'CurrentNoDraw', 'MaxNoDraw', 'B365D_mean', 'c_prob', 'link']
    doc.add_html(stats.to_html(columns=columns_to_show, escape=False))

    series = no_draw_frequencies(country)
    freq = Counter(series)
    doc.add_text(' ')
    doc.add_html(
        '<p class="centered">Country Average: <b>{0}</b></p>'.format(statistics.mean(series)))
    doc.add_html(
        '<p class="centered">Country Median: <b>{0}</b></p>'.format(statistics.median(series)))
    table = pd.Series(freq).to_frame()
    doc.add_html(table.sort_index().to_html())
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.hist(series)
    doc.add_figure(fig, width=0.8)
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.boxplot(series, vert=False)
    doc.add_figure(fig, width=0.8)

    doc.show()

    teams = championship_teams(df)
    for team in teams:
        doc = handout.Handout('handout/' + country + '/' + team)
        doc.add_html(styling)
        doc.add_text('## ' + team)
        team_matches = team_dfs[team]
        # TODO: Find a solution with team logos?
        # team_matches['HomeTeam'] = team_matches.apply(lambda row: add_logo(row), axis=1)
        team_matches = team_matches.rename(columns={
            'HomeTeam': 'H',
            'AwayTeam': 'A',
        })
        columns_to_show = ['period', 'H', 'A', 'result', 'FTHG', 'FTAG',
                           'B365D', 'count_draw', 'count_no_draw']
        team_html = team_matches.iloc[::-1].to_html(escape=False, columns=columns_to_show).replace(
            '<td>W</td>', '<td style="background-color:greenyellow;">W</td>'
        ).replace(
            '<td>D</td>', '<td style="background-color:orange;">D</td>'
        ).replace(
            '<td>L</td>', '<td style="background-color:red;">L</td>'
        ).replace(
            team, '<b>{0}</b>'.format(team)
        )
        doc.add_html(team_html)
        try:
            series = no_draw_frequencies(country, [team])
            freq = Counter(series)
            doc.add_text(' ')
            doc.add_html(
                '<p class="centered">Team Average: <b>{0}</b></p>'.format(statistics.mean(series)))
            doc.add_html(
                '<p class="centered">Team Median: <b>{0}</b></p>'.format(statistics.median(series)))
            table = pd.Series(freq).to_frame()
            doc.add_html(table.sort_index().to_html())
            fig, ax = plt.subplots(figsize=(3, 2))
            ax.hist(series)
            doc.add_figure(fig, width=0.8)
            fig, ax = plt.subplots(figsize=(3, 2))
            ax.boxplot(series, vert=False)
            doc.add_figure(fig, width=0.8)
        except statistics.StatisticsError as e:
            print(e)
            pass

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
