# handout: begin-exclude
import pandas as pd
import matplotlib.pyplot as plt
# import numpy as np

import handout
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
    columns_to_show = ['1920_wins', '1920_draws', '1920_losses',
                       '1920_points', 'CurrentNoDraw', 'MaxNoDraw', 'B365D_mean', 'c_prob', 'link']
    doc.add_html(stats.to_html(columns=columns_to_show, escape=False))

    freq = no_draw_frequencies(country)
    series = pd.Series(freq)
    counts = series.value_counts()
    doc.add_text(' ')
    doc.add_text(dict(counts))
    table = pd.Series(dict(counts)).to_frame()
    doc.add_html(table.sort_index().to_html())
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.hist(series)
    doc.add_figure(fig, width=0.6)

    doc.show()

    teams = championship_teams(df)
    for team in teams:
        doc = handout.Handout('handout/' + country + '/' + team)
        doc.add_html(styling)
        team_matches = team_dfs[team]
        # TODO: Find a solution with team logos?
        # team_matches['HomeTeam'] = team_matches.apply(lambda row: add_logo(row), axis=1)
        team_html = team_matches.iloc[::-1].to_html(escape=False).replace(
            '<td>W</td>', '<td style="background-color:greenyellow;">W</td>'
        ).replace(
            '<td>D</td>', '<td style="background-color:orange;">D</td>'
        ).replace(
            '<td>L</td>', '<td style="background-color:red;">L</td>'
        ).replace(
            team, '<b>{0}</b>'.format(team)
        )
        doc.add_html(team_html)
        freq = no_draw_frequencies(country, [team])
        series = pd.Series(freq)
        counts = series.value_counts()
        doc.add_text(' ')
        doc.add_text(dict(counts))
        table = pd.Series(dict(counts)).to_frame()
        doc.add_html(table.sort_index().to_html())
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.hist(series)
        doc.add_figure(fig, width=0.6)

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
