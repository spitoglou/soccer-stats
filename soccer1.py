# handout: begin-exclude
import pandas as pd
import matplotlib.pyplot as plt
# import numpy as np
from collections import Counter
from loguru import logger

import handout
import statistics
from sp_soccer_lib.championships import team_stats, load_country
from sp_soccer_lib.handout_helpers import style, get_country_header, make_link
from sp_soccer_lib import create_team_df_dict, championship_teams, no_draw_frequencies


countries = ['greece', 'italy', 'england', 'spain', 'germany', 'france']
styling = style()


def country_df_properties(df):
    df = df.rename(columns={
        '1920_wins': 'W',
        '1920_draws': 'D',
        '1920_losses': 'L',
        '1920_gf': 'GF',
        '1920_ga': 'GA',
        '1920_points': 'PTS'
    })
    columns_to_show = ['W', 'D', 'L', 'GF', 'GA',
                       'PTS', 'CurrentNoDraw', 'MaxNoDraw', 'B365D_mean', 'c_prob', 'link']
    return df, columns_to_show


def team_df_properties(df):
    df = df.rename(columns={
        'HomeTeam': 'H',
        'AwayTeam': 'A',
    })
    columns_to_show = ['period', 'H', 'A', 'result', 'FTHG', 'FTAG',
                       'B365D', 'count_draw', 'count_no_draw']
    return df, columns_to_show


def frequency_graphs(doc, country, team=None):
    series = no_draw_frequencies(country, team)
    freq = Counter(series)
    doc.add_text(' ')
    doc.add_html(
        '<p class="centered">Average: <b>{0}</b></p>'.format(statistics.mean(series)))
    doc.add_html(
        '<p class="centered">Median: <b>{0}</b></p>'.format(statistics.median(series)))
    table = pd.Series(freq).to_frame()
    doc.add_html(table.sort_index().to_html())
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.hist(series)
    doc.add_figure(fig, width=0.8)
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.boxplot(series, vert=False)
    doc.add_figure(fig, width=0.8)
    plt.close('all')
    return doc


main_doc = handout.Handout('handout')
main_doc._logger.setLevel(0)
for country in countries:
    main_doc.add_html(
        '<a href="./{0}/index.html">{1}</a>'.format(country, get_country_header(country)))
main_doc.show()


for country in countries:
    logger.info('Starting country: ' + country)
    country_doc = handout.Handout('handout/' + country)

    country_doc.add_html(get_country_header(country))
    country_doc.add_html(styling)

    df = load_country(country)
    team_dfs = create_team_df_dict(df)
    stats = team_stats(team_dfs)

    stats['index_col'] = stats.index
    stats['link'] = stats.apply(lambda row: make_link(row), axis=1)
    stats, columns_to_show = country_df_properties(stats)
    country_doc.add_html(stats.to_html(columns=columns_to_show, escape=False))

    country_doc = frequency_graphs(country_doc, country)

    country_doc.show()
    # logger.info('Finished')

    teams = championship_teams(df)
    for team in teams:
        logger.info('Starting Team: ' + team)
        team_doc = handout.Handout('handout/' + country + '/' + team)

        team_doc.add_html(styling)
        team_doc.add_text('## ' + team)

        team_matches = team_dfs[team]

        # TODO: Find a solution with team logos?
        # team_matches['HomeTeam'] = team_matches.apply(lambda row: add_logo(row), axis=1)
        team_matches, columns_to_show = team_df_properties(team_matches)
        team_html = team_matches.iloc[::-1].to_html(escape=False, columns=columns_to_show).replace(
            '<td>W</td>', '<td style="background-color:greenyellow;">W</td>'
        ).replace(
            '<td>D</td>', '<td style="background-color:orange;">D</td>'
        ).replace(
            '<td>L</td>', '<td style="background-color:red;">L</td>'
        ).replace(
            team, '<b>{0}</b>'.format(team)
        )
        team_doc.add_html(team_html)

        try:  # because there were countries with few stats in the time of codeing
            team_doc = frequency_graphs(team_doc, country, [team])
        except statistics.StatisticsError as e:
            # print(e)
            logger.exception(e)
            pass

        team_doc.show()
        # logger.info('Finished')
logger.info('Finished All Countries and Teams')

""" ### Footer
Authored by Stavros Pitoglou (Computer Solutions SA) / 2019

 """

# handout: end-exclude
