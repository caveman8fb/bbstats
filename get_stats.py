import requests
from pprint import pprint
from datetime import date
from prettytable import PrettyTable


def get_info_mlb_players():
    api_endpoint = 'sports/1/players'
    options = 'season=2022&fields=people,id,firstName,lastName,birthDate,currentTeam,id,name,primaryPosition,abbreviation,'
    more_options = 'mlbDebutDate,birthCity,birthStateProvince,birthCountry,height,weight,batSide,code,pitchHand,code'
    url = BASE_URL + api_endpoint + '?' + options + more_options # Breaking up the long url for readability
    response = requests.get(url)
    allplayers = response.json()['people']
    
    players = []
    for player in allplayers:
        if 'mlbDebutDate' in player:
            player = cleanup_flatten(player)
            players.append(player)
    return players


def cleanup_flatten(player):
    # Transform Dates, Cleanup and Flatten some fields
    player['mlbDebutDate'] = traditional_date(player['mlbDebutDate'])
    player['birthDate'] = traditional_date(player['birthDate'])
    player['batSide'] = player['batSide']['code']
    player['pitchHand'] = player['pitchHand']['code']
    player['currentTeamId'] = player.pop('currentTeam')['id']
    player['primaryPositionName'] = player['primaryPosition']['name']
    player['primaryPosition'] = player['primaryPosition']['abbreviation']
    player = create_bornin_field(player)
    return player


def traditional_date(olddate):
    # switch date to M/D/Y with no leading zeros
    # just because that how the old cards show dates
    moddate = date.fromisoformat(olddate)
    newdate = moddate.strftime("%m/%d/%Y").replace('/0', '/')
    if newdate.startswith('0'):
        newdate = newdate[1:]
    return newdate


def create_bornin_field(player):
    bornIn = ""
    b_keys = ['birthCity', 'birthStateProvince', 'birthCountry']
    for bkey in b_keys:
        if bkey in player.keys():
            bornIn += player.pop(bkey) + ', '
    if bornIn.endswith(', '):
        bornIn = bornIn[:-2]
    if bornIn.endswith('USA'):
        # Strip off USA
        bornIn = bornIn[:-5]
    if bornIn == "":
        bornIn = 'Parts Unknown'
    player['bornIn'] = bornIn
    return player


def get_players_by_team_id(team_id):
    # based on team id from https://statsapi.mlb.com/api/v1/teams
    team_players = []
    players = get_info_mlb_players()
    for player in players:
        if player['currentTeamId'] == int(team_id):
            team_players.append(player)
    return team_players


def get_players_multiple_teams(teams):
    players = []
    for team in teams:
        team_players = get_players_by_team_id(team)
        players += team_players
    return players


def get_player_stats(id, stat_type):
    print(stat_type)
    if stat_type not in ['hitting', 'pitching']:
        raise ValueError('Invalid Type provided')
    api_endpoint = 'people/{}'.format(id)
    options = 'hydrate=stats(group={},type=yearByYear),currentTeam'.format(stat_type)
    url = BASE_URL + api_endpoint + '?' + options
    response = requests.get(url)
    stats = response.json()
    return stats["people"][0]["stats"][0]


def search_players_by_id(id, players):
    for p in players:
        if p['id'] == id:
            return p


def only_mlb_stats(stats):
    mlb_stats = []
    for s in stats['splits']:
        if s['sport']['id'] == 1:
            mlb_stats.append(s)
    return mlb_stats

def team_name(stat):
    team = ''
    if 'team' in stat:
        team = str(stat['team']['name']).split(' ')[-1]
    else:
        team = 'MLB'
    return team

def cleanup_stats(stats, stat_type):
    if stat_type == 'pitching':
        return cleanup_pitching_stats(stats)
    else:
        return cleanup_batting_stats(stats)


def cleanup_pitching_stats(stats):
    # Create list of lists with the headers in the first record
    clean_stats = []
    headers = ['Year','Team','G','IP','W','L','S','ER','SO','BB','ERA']
    clean_stats.append(headers)
    for s in stats:
        team = team_name(s)
        sstats = [
            s['season'], 
            team, 
            s['stat']['gamesPlayed'], 
            s['stat']['inningsPitched'],
            s['stat']['wins'], 
            s['stat']['losses'],
            s['stat']['saves'],
            s['stat']['earnedRuns'],
            s['stat']['strikeOuts'],
            s['stat']['baseOnBalls'],
            s['stat']['era']
        ]
        if team != 'MLB':
            clean_stats.append(sstats)
    return clean_stats


def cleanup_batting_stats(stats):
    # Create list of lists with the headers in the first record
    clean_stats = []
    headers = ['Year','Team','G','ABs','R','H','2B','3B','HR','RBI','SB','BB','SO','AVG']
    clean_stats.append(headers)
    for s in stats:
        team = team_name(s)
        sstats = [
            s['season'], 
            team,
            s['stat']['gamesPlayed'], 
            s['stat']['atBats'],
            s['stat']['runs'], 
            s['stat']['hits'],
            s['stat']['doubles'],
            s['stat']['triples'],
            s['stat']['homeRuns'],
            s['stat']['rbi'],
            s['stat']['stolenBases'],
            s['stat']['baseOnBalls'],
            s['stat']['strikeOuts'],
            s['stat']['avg']
        ]
        if team != 'MLB':
            clean_stats.append(sstats)
    return clean_stats

def career_to_array(stats, stat_type):
    if stat_type == 'pitching':
        return career_pitching_to_array(stats)
    else:
        return career_batting_to_array(stats)

def career_pitching_to_array(s):
    # Create an array with the career totals
    career_stats = [
            'MLB', 
            'Total', 
            s['stat']['gamesPlayed'], 
            s['stat']['inningsPitched'],
            s['stat']['wins'], 
            s['stat']['losses'],
            s['stat']['saves'],
            s['stat']['earnedRuns'],
            s['stat']['strikeOuts'],
            s['stat']['baseOnBalls'],
            s['stat']['era']
        ]
    return career_stats    

def career_batting_to_array(s):
    # Create an array with the career totals
    career_stats = [
            'MLB', 
            'Total', 
            s['stat']['gamesPlayed'], 
            s['stat']['atBats'],
            s['stat']['runs'], 
            s['stat']['hits'],
            s['stat']['doubles'],
            s['stat']['triples'],
            s['stat']['homeRuns'],
            s['stat']['rbi'],
            s['stat']['stolenBases'],
            s['stat']['baseOnBalls'],
            s['stat']['strikeOuts'],
            s['stat']['avg']
        ]
    return career_stats


def get_career_stats(id, stat_type):
    api_endpoint = 'people/{}'.format(id)
    options = 'hydrate=stats(group={},type=career),currentTeam'.format(stat_type)
    url = BASE_URL + api_endpoint + '?' + options
    response = requests.get(url)
    stats = response.json()
    return stats["people"][0]["stats"][0]['splits'][0]


def print_stats_table(stats, career_stats):
    x = PrettyTable()
    for s in stats:
        if s[0] == 'Year':
            x.field_names = s
        else:
            x.add_row(s)
    last = []
    for i in career_stats:
        last.append('--\n' + str(i))
    x.add_row(last)
    x.align = "r"
    print(x)


def print_rear_text(player_info):
    player_name = player_info['firstName'] + ' ' + player_info['lastName']
    line1 = ''
    line2 = ''
    line1 += 'HT: ' + str(player_info['height'])
    line1 += '  WT: ' + str(player_info['weight'])
    line1 += '  Bats: ' + str(player_info['batSide'])
    line1 += '  Throws: ' + str(player_info['pitchHand'])
    line1 += '  Position: ' + str(player_info['primaryPositionName'])
    line2 += 'DOB: ' + str(player_info['birthDate'])
    line2 += '  From: ' + str(player_info['bornIn'])
    line2 += '  Debut: ' + str(player_info['mlbDebutDate'])
    print(player_name)
    print(line1)
    print(line2)


def player_stats(id, stat_type):
    stats = get_player_stats(id, stat_type)
    mlb_stats = only_mlb_stats(stats)
    career_stats = get_career_stats(id, stat_type)
    return mlb_stats, career_stats


def get_card_info(card_no, id, players, raw=False, show=False):
    player_info = search_players_by_id(id, players)
    stat_type = 'hitting'
    if player_info['primaryPosition'] == 'P':
        stat_type = 'pitching'

    mlb_stats, career_stats = player_stats(id, stat_type)
    
    clean_career_stats = career_to_array(career_stats, stat_type)
    clean_mlb_stats = cleanup_stats(mlb_stats, stat_type)
    card_info = {'card': card_no}
    card_info['player_info'] = player_info
    # Include raw or cleaned/flattened stat data
    if raw:
        card_info['season_stats'] = mlb_stats
        card_info['career_stats'] = career_stats
    else:
        card_info['season_stats'] = clean_mlb_stats
        card_info['career_stats'] = clean_career_stats

    if print:
        print_rear_text(player_info)
        print_stats_table(clean_mlb_stats, clean_career_stats)
    return card_info
    


if __name__ == "__main__":
    BASE_URL = 'https://statsapi.mlb.com/api/v1/'
    team_id = 139 # Tampa Bay Rays
    players = get_players_by_team_id(team_id)

    cards = []
    example_players = [(1, 595281), (2, 656876)]
    for t in example_players:
        card_no = t[0]
        id = t[1]
        card_info = get_card_info(card_no, id, players, raw=False, show=True)
        cards.append(card_info)
    print(cards)
    
    
