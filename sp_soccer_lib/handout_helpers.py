def style():
    style = '''
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
    centered: {
        text-align: center;
    }

</style>

    '''
    return style


def get_country_header(country):
    if country == 'england':
        return '<img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/' + \
            'Premier_League_Logo.svg/1920px-Premier_League_Logo.svg.png" alt="Logo" width="100%">'
    elif country == 'greece':
        return '<img src="http://blog.fieldoo.com/wp-content/uploads/2015/05/images_posts_Greece.jpg" ' + \
            'alt="Logo" width="100%">'
    elif country == 'germany':
        return '<img src="https://2.bp.blogspot.com/-1DSQUPYLIEI/Tfuiy8MMq9I/AAAAAAAAW0c/AGs0P4JDHoA/s1600/' + \
            'Bundesliga_Logo.png" alt="Logo" width="100%">'
    elif country == 'france':
        return '<img src="https://medias.lequipe.fr/img-photo-png/-/1500000000807555/126: 0, 1639: ' + \
            '1008-624-416-75/c397a.png" alt="Logo" width="100%">'
    elif country == 'italy':
        return '<img src="https://2.bp.blogspot.com/-EREH6W98EXU/XNVkWSIhfgI/AAAAAAAB7R4/' + \
            'Kt4WHlhPBYIJ9MZkxJ9v-fL9hLbWHXQwgCLcBGAs/s1600/all-new-serie-a-logo % 2B % 25281 % 2529.jpg"' + \
            ' alt="Logo" width="100%">'
    elif country == 'spain':
        return '<img src="https://besthqwallpapers.com/Uploads/21-9-2017/21194/' + \
            'thumb2-la-liga-emblem-logo-spain-flag-of-spain.jpg"' + \
            ' alt="Logo" width="100%">'
    else:
        return '<h2>{0}</h2>'.format(country.capitalize())


def make_link(row):
    return '<a href="./{0}/index.html">Link</a>'.format(row['index_col'])


def add_logo(row):
    return '<img src="https://kassiesa.net/uefa/clubs/images/{0}.png" alt="Logo" height="42" width="42">{0}' \
        .format(row['HomeTeam'])
