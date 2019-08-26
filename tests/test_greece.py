def bootstrap_greece():
    from lib import create_team_df_dict
    from lib.championships import load_greece
    df = load_greece()
    team_dfs = create_team_df_dict(df)
    return team_dfs


def test_team_dfs():
    from lib import period_stats
    team_dfs = bootstrap_greece()
    wins, draws, losses, points = period_stats(team_dfs['Panionios'], '1819')
    assert wins == 11
    assert draws == 5
    assert losses == 14
    assert points == 38
    olympiakos = team_dfs['Olympiakos']
    assert olympiakos.shape[0] == 61
