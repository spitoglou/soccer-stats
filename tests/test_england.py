def bootstrap_england():
    from sp_soccer_lib import create_team_df_dict
    from sp_soccer_lib.championships import load_england
    df = load_england()
    team_dfs = create_team_df_dict(df)
    return team_dfs


def test_team_dfs():
    from sp_soccer_lib import period_stats
    team_dfs = bootstrap_england()
    wins, draws, losses, points, gf, ga = period_stats(team_dfs['Arsenal'], 'Arsenal', '1819')
    assert wins == 21
    assert draws == 7
    assert losses == 10
    assert points == 70
    arsenal = team_dfs['Arsenal']
    assert arsenal.shape[0] == 83


def test_team_stats():
    from sp_soccer_lib.championships import team_stats
    team_dfs = bootstrap_england()
    new = team_stats(team_dfs)
    assert new.loc['Wolves'].MaxNoDraw == 6.0
    assert new.loc['Southampton']['1718_draws'] == 15.0
