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
from sp_soccer_lib.championships import load_greece, load_england, load_italy, team_stats
from sp_soccer_lib import period_stats, create_team_df_dict

doc = handout.Handout('handout')
df = load_greece()  # handout: exclude

team_dfs = create_team_df_dict(df)
print(team_dfs['Atromitos'])

styling = '''
<style>

    h2 {
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    table {
        margin-left: auto;
        margin-right: auto;
        width: 100%;
    }
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th, td {
        padding: 5px;
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
        font-size: 90%;
    }
    table tbody tr:hover {
        background-color: #dddddd;
    }
    .wide {
        width: 90%;
    }

</style>

    '''
doc.add_html(styling)
doc.add_html(team_dfs['Atromitos'].to_html())
print(team_dfs['Olympiakos'])
doc.show()
# handout: end-exclude


print(period_stats(team_dfs['Panionios'], '1819'))

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
