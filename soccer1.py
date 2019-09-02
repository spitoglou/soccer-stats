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
    return '<img src="https://kassiesa.net/uefa/clubs/images/{0}.png" alt="Logo" height="42" width="42">{0}' \
        .format(row['HomeTeam'])


def get_country_header(country):
    if country == 'england':
        return '<img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/', \
            'Premier_League_Logo.svg/1920px-Premier_League_Logo.svg.png" alt="Logo" width="100%">'
    elif country == 'greece':
        return '<img src="http://blog.fieldoo.com/wp-content/uploads/2015/05/images_posts_Greece.jpg" ', \
            'alt="Logo" width="100%">'
    elif country == 'germany':
        return '<img src="https://2.bp.blogspot.com/-1DSQUPYLIEI/Tfuiy8MMq9I/AAAAAAAAW0c/AGs0P4JDHoA/s1600/', \
            'Bundesliga_Logo.png" alt="Logo" width="100%">'
    elif country == 'france':
        return '<img src="https://medias.lequipe.fr/img-photo-png/-/1500000000807555/126: 0, 1639: ', \
            '1008-624-416-75/c397a.png" alt="Logo" width="100%">'
    elif country == 'italy':
        return '<img src="https://2.bp.blogspot.com/-EREH6W98EXU/XNVkWSIhfgI/AAAAAAAB7R4/', \
            'Kt4WHlhPBYIJ9MZkxJ9v-fL9hLbWHXQwgCLcBGAs/s1600/all-new-serie-a-logo % 2B % 25281 % 2529.jpg"', \
            ' alt="Logo" width="100%">'
    else:
        return '<h2>{0}</h2>'.format(country.capitalize())


countries = ['greece', 'italy', 'england', 'spain', 'germany', 'france']
doc = handout.Handout('handout')
# doc.add_html('<ul>')
for country in countries:
    doc.add_html(
        '<a href="./{0}/index.html">{1}</a>'.format(country, get_country_header(country)))
#     doc.add_html('<li><a href="./{0}/index.html">{1}</a></li>'.format(country, get_country_header(country)))
# doc.add_html('</ul>')
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
    # stats['link'] = '<a href="/{0}">Link</a>'.format(stats['index_col'])
    stats['link'] = stats.apply(lambda row: make_link(row), axis=1)
    columns_to_show = ['1920_wins', '1920_draws', '1920_losses',
                       '1920_points', 'CurrentNoDraw', 'MaxNoDraw', 'link']
    doc.add_html(stats.to_html(columns=columns_to_show, escape=False))
    doc.show()

    teams = championship_teams(df)
    for team in teams:
        doc = handout.Handout('handout/' + country + '/' + team)
        doc.add_html(styling)
        team_matches = team_dfs[team]
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
