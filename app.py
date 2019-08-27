from flask import Flask, abort, jsonify
from sp_soccer_lib.championships import load_greece, load_england, load_italy, team_stats
from sp_soccer_lib import create_team_df_dict

app = Flask(__name__)

app.debug = True


def bootstrap_country(country):
    if country == 'greece':
        df = load_greece()
    elif country == 'england':
        df = load_england()
    elif country == 'italy':
        df = load_italy()
    else:
        abort(400)
    return df


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/team_stats/<country>')
def ep_team_stats(country):
    df = bootstrap_country(country)
    teams = create_team_df_dict(df)
    stats = team_stats(teams)
    return jsonify(stats.to_dict(orient='index'))


@app.route('/team/<country>/<team>')
def ep_team(country, team):
    df = bootstrap_country(country)
    teams = create_team_df_dict(df)
    try:
        team_df = teams[team].reset_index()
    except KeyError:
        abort(400)
    return jsonify({team: team_df.to_dict(orient='records')})


if __name__ == '__main__':
    app.run()
