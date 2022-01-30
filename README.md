# bbstats
Test Python Project for getting stats for baseball cards  
**Works with Python 3.8+**  

## Running the example (2 players) to cards.json
```
# create Venv
python3.8 -m venv venv
source venv/bin/activate
# install requirements
python -m pip install -r requirements.txt
python get_stats.py
```


## Get Player Data by Team
```
BASE_URL = 'https://statsapi.mlb.com/api/v1/'
team_id = 139 # Tampa Bay Rays
players = get_players_by_team_id(team_id)
```

## Get Card Info for a player in the list of players
```
card_info = get_card_info(card_no, id, players, raw=False, show=True)
```
### raw will return the raw data for gathered stats, false returns a list of list with a header
```
card_info = get_card_info(card_no, id, players, raw=True, show=False)
```
results if true (shortened example)
```
....
'season': '2013',
'sport': {'abbreviation': 'MLB',
    'id': 1,
    'link': '/api/v1/sports/1'},
'stat': {'airOuts': 0,
         'atBats': 0,
         'atBatsPerHomeRun': '-.--',
         'avg': '.000',
....
```
results if false
```
....
  'season_stats': [['Year','Team','G','IP','W','L','S','ER','SO','BB','ERA'],
                   ['2020', 'Brewers', 12, '15.1', 1, 0, 0, 10, 21, 9, '5.87'],
                   ['2021', 'Brewers', 15, '17.0', 0, 1, 1, 8, 25, 12, '4.24'],
                   ['2021', 'Rays', 20, '59.0', 4, 0, 0, 16, 48, 13, '2.44']]}]
....
```
### show will print the data in viewable format
```
card_info = get_card_info(card_no, id, players, raw=False, show=True)
```
stdout
```
Kevin Kiermaier
HT: 6' 1"  WT: 210  Bats: L  Throws: R  Position: Outfielder
DOB: 4/22/1990  From: Fort Wayne, IN  Debut: 9/30/2013
+------+-------+-----+------+-----+-----+-----+----+----+-----+-----+-----+-----+------+
| Year |  Team |   G |  ABs |   R |   H |  2B | 3B | HR | RBI |  SB |  BB |  SO |  AVG |
+------+-------+-----+------+-----+-----+-----+----+----+-----+-----+-----+-----+------+
| 2013 |  Rays |   1 |    0 |   0 |   0 |   0 |  0 |  0 |   0 |   0 |   0 |   0 | .000 |
| 2014 |  Rays | 108 |  331 |  35 |  87 |  16 |  8 | 10 |  35 |   5 |  23 |  71 | .263 |
| 2015 |  Rays | 151 |  505 |  62 | 133 |  25 | 12 | 10 |  40 |  18 |  24 |  95 | .263 |
| 2016 |  Rays | 105 |  366 |  55 |  90 |  20 |  2 | 12 |  37 |  21 |  40 |  74 | .246 |
| 2017 |  Rays |  98 |  380 |  56 | 105 |  15 |  3 | 15 |  39 |  16 |  31 |  99 | .276 |
| 2018 |  Rays |  88 |  332 |  44 |  72 |  12 |  9 |  7 |  29 |  10 |  25 |  91 | .217 |
| 2019 |  Rays | 129 |  447 |  60 | 102 |  20 |  7 | 14 |  55 |  19 |  26 | 104 | .228 |
| 2020 |  Rays |  49 |  138 |  16 |  30 |   5 |  3 |  3 |  22 |   8 |  20 |  42 | .217 |
| 2021 |  Rays | 122 |  348 |  54 |  90 |  19 |  7 |  4 |  37 |   9 |  33 |  99 | .259 |
|   -- |    -- |  -- |   -- |  -- |  -- |  -- | -- | -- |  -- |  -- |  -- |  -- |   -- |
|  MLB | Total | 851 | 2847 | 382 | 709 | 132 | 51 | 75 | 294 | 106 | 222 | 675 | .249 |
+------+-------+-----+------+-----+-----+-----+----+----+-----+-----+-----+-----+------+
```
## Examples

### Example 2 players from a team (cards 1 and 2)
without Pretty Print
```
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
```
output
```
[{'card': 1, 'player_info': {'id': 595281, 'firstName': 'Kevin', 'lastName': 'Kiermaier', 'birthDate': '4/22/1990', 'height': '6\' 1"', 'weight': 210, 'primaryPosition': 'CF', 'mlbDebutDate': '9/30/2013', 'batSide': 'L', 'pitchHand': 'R', 'currentTeamId': 139, 'primaryPositionName': 'Outfielder', 'bornIn': 'Fort Wayne, IN'}, 'season_stats': [['Year', 'Team', 'G', 'ABs', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'BB', 'SO', 'AVG'], ['2013', 'Rays', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '.000'], ['2014', 'Rays', 108, 331, 35, 87, 16, 8, 10, 35, 5, 23, 71, '.263'], ['2015', 'Rays', 151, 505, 62, 133, 25, 12, 10, 40, 18, 24, 95, '.263'], ['2016', 'Rays', 105, 366, 55, 90, 20, 2, 12, 37, 21, 40, 74, '.246'], ['2017', 'Rays', 98, 380, 56, 105, 15, 3, 15, 39, 16, 31, 99, '.276'], ['2018', 'Rays', 88, 332, 44, 72, 12, 9, 7, 29, 10, 25, 91, '.217'], ['2019', 'Rays', 129, 447, 60, 102, 20, 7, 14, 55, 19, 26, 104, '.228'], ['2020', 'Rays', 49, 138, 16, 30, 5, 3, 3, 22, 8, 20, 42, '.217'], ['2021', 'Rays', 122, 348, 54, 90, 19, 7, 4, 37, 
9, 33, 99, '.259']], 'career_stats': ['MLB', 'Total', 851, 2847, 382, 709, 132, 51, 75, 294, 106, 222, 675, '.249']}, {'card': 2, 'player_info': {'id': 656876, 'firstName': 'Drew', 'lastName': 'Rasmussen', 'birthDate': '7/27/1995', 'height': '6\' 1"', 'weight': 211, 'primaryPosition': 'P', 'mlbDebutDate': '8/19/2020', 'batSide': 'R', 'pitchHand': 'R', 'currentTeamId': 139, 'primaryPositionName': 'Pitcher', 'bornIn': 'Puyallup, WA'}, 'season_stats': [['Year', 'Team', 'G', 'IP', 'W', 'L', 'S', 'ER', 'SO', 'BB', 'ERA'], ['2020', 'Brewers', 12, '15.1', 1, 0, 0, 10, 21, 9, '5.87'], ['2021', 'Brewers', 15, '17.0', 0, 1, 1, 8, 25, 12, '4.24'], ['2021', 'Rays', 20, '59.0', 4, 0, 0, 16, 48, 13, '2.44']], 'career_stats': ['MLB', 'Total', 47, '91.1', 5, 1, 1, 34, 94, 34, '3.35']}]
```

### Generate Cards for all MLB Players
```
cards = []
players = get_info_mlb_players()
card_no = 1
for player in players:
    if player['currentTeamId']:
    try:
        card_info = get_card_info(card_no, player['id'], players, raw=False, show=False)
        card.append(card_info)
        card_no += 1
    except:
        warnings.warn("Failed to generate card for ID: {}".format(player[id]))
print(cards)
```

## Mockup Card
### Front
![alt text](https://github.com/caveman8fb/bbstats/blob/main/images/mockup/example_front.png?raw=true)
### Back
![alt text](https://github.com/caveman8fb/bbstats/blob/main/images/mockup/example_back.png?raw=true)

Blank images inlcuded for future use with Pillow, PIL, ImageMagick, etc.

# TODO:
- Add ArgParse options
- Refactor code
- Store data (pickle, sqlite, other db, etc.)
- Get Current Team Info
  - Team Colors
  - Team Logos
- Locate and Pull Player Photos (bing_image_downloader?)
- Add Photo Generator for card sides (Pillow?)
- Add Web Front-End for easy viewing (Flask?)
- Add Error Handling
- Add Typing
- Add Unit Testing
