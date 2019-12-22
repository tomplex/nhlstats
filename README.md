### nhlstats

A library and CLI tool for collecting stats from the NHL web API. 

Currently, supported data types include event data such as shots / goals / hits / etc, shift information and general scheduling information.

All data is accessible identically through the Python API or command-line tool.


#### Install

Compatible with Python3.5+.

Use `pip`:

```bash
python3 -m pip install nhlstats
```

Or from source:

```bash
git clone https://github.com/tomplex/nhlstats.git ~/dev/nhlstats
python3 -m pip install ~/dev/nhlstats
# or
python3 ~/dev/nhlstats/setup.py install
```

This will add a new command to your system, `nhl`.

#### Usage - library
Let's say you want to write a script which you'll run once a day, which will find all games played on the given day and download all play-by-play data for each game into a CSV file, labelled with the game's ID.

```python
from nhlstats import list_games, list_plays
from nhlstats.formatters import csv

# List all games today and write all plays from each as a csv file named like the game_id
for game in list_games():  # No args will list all games today
    game_id = game['game_id']
    plays = list_plays(game_id)  # get plays, normalized
    
    with open('{}.csv'.format(game_id), 'w') as f:
        csv.dump(plays, f)

```

If you use Pandas, then you can create a dataframe directly from the data which comes back from list_plays or list_shifts:

```python
from nhlstats import list_plays, list_shifts
import pandas as pd

gameid = "2019020418"

plays = pd.DataFrame(list_plays(gameid))
shifts = pd.DataFrame(list_shifts(gameid))

plays.head()
shifts.head()

``` 

If you use [petl](https://petl.readthedocs.io/en/stable/), then you can use `petl.fromdicts()` to create a `TableContainer`:

```python
from nhlstats import list_plays
import petl as etl

gameid = "2019020418"

pipeline = etl.fromdicts(list_plays(gameid))

print(pipeline)
```

##### Formatters

The formatters package formats data into different types of output, for example CSV, JSON, or a 
text-based table. Each formatter has a `dump` and `dumps` function which work similarly to Python's `json` module. 
If you want to save your data as JSON, for example:

```python
from nhlstats import list_plays
from nhlstats.formatters import json

plays = list_plays('gameid')
with open('file.json', 'w') as f:
    json.dump(plays, f)

```

More detailed examples of the formatters are available below.


#### Usage - CLI

```
$ nhl --help
Usage: nhl [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  list-games   List all games from START_DATE to END_DATE.
  list-plays   List all play events which occurred in the given GAME_ID.
  list-shifts  List all shifts which occurred in the given GAME_ID.
  list-shots   List all shot events which occurred in the given GAME_ID.
```

Use the `--output-format` option to specify how to display the collected data. This option is available with all commands. 
The default is `text`, which will pretty-print the data as a table. Other options include `csv`, `json`, 
which will output a nested JSON like `{"data": [...]}`. The data from these commands will always be printed to stdout.
On Linux, MacOS or Windows you can use the `>` to redirect stdout to a new file 
(will overwrite the contents if it exists), or `>>` to append to a file, like so:

```bash
nhl list-plays 2019020406 --output-format csv > 2019020406.csv  # create a new file
nhl list-plays 2019020406 --output-format csv >> plays.csv  # append result to plays.csv
```


##### list-games

```bash
$ nhl list-games --help
Usage: nhl list-games [OPTIONS] [START_DATE] [END_DATE]

  List all games from START_DATE to END_DATE. Dates should be of the form
  YYYY-MM-DD. Both date arguments default to "today" by system time, so you
  can omit the final argument to get a range from the first date to today.

Options:
  --output-format [text|csv|json]
  --help                          Show this message and exit.
```

##### list-plays

```bash
$ nhl list-plays --help
Usage: nhl list-plays [OPTIONS] GAME_ID

  List all play events which occurred in the given GAME_ID.

Options:
  --output-format [text|csv|json]
  --help                          Show this message and exit.
```

##### list-shifts

```bash
nhl list-shifts --help
Usage: nhl list-shifts [OPTIONS] GAME_ID

  List all shot events which occurred in the given GAME_ID.

Options:
  --output-format [text|csv|json]
  --help                          Show this message and exit.

```

### Data schema

The raw event data from the NHL is highly nested, and doesn't always contain all keys. I flatten, normalize and cull the 
data a bit to make it easier to display as tabular data and remove bits which didn't initially strike me as important.
I could always be convinced to add in more.

The initial events, as received from the NHL, look like this:

```json
{
  "players": [
    {
      "player": {
        "id": 8474189,
        "fullName": "Lars Eller",
        "link": "/api/v1/people/8474189"
      },
      "playerType": "Winner"
    },
    {
      "player": {
        "id": 8470144,
        "fullName": "Frans Nielsen",
        "link": "/api/v1/people/8470144"
      },
      "playerType": "Loser"
    }
  ],
  "result": {
    "event": "Faceoff",
    "eventCode": "DET52",
    "eventTypeId": "FACEOFF",
    "description": "Lars Eller faceoff won against Frans Nielsen"
  },
  "about": {
    "eventIdx": 3,
    "eventId": 52,
    "period": 1,
    "periodType": "REGULAR",
    "ordinalNum": "1st",
    "periodTime": "00:00",
    "periodTimeRemaining": "20:00",
    "dateTime": "2019-12-01T00:08:26Z",
    "goals": {
      "away": 0,
      "home": 0
    }
  },
  "coordinates": {
    "x": 0,
    "y": 0
  },
  "team": {
    "id": 15,
    "name": "Washington Capitals",
    "link": "/api/v1/teams/15",
    "triCode": "WSH"
  }
}
```

the same event, "normalized", looks like this:

```json
{
  "datetime": "2019-12-01T00:08:26Z", 
  "period": 1, 
  "period_time": "00:00", 
  "period_time_remaining": "20:00", 
  "period_type": "REGULAR", 
  "x": 0.0, 
  "y": 0.0, 
  "event_type": "FACEOFF", 
  "event_secondary_type": null, 
  "event_description": "Lars Eller faceoff won against Frans Nielsen", 
  "team_for": "WSH", 
  "player_1": "Lars Eller", 
  "player_1_type": "Winner", 
  "player_1_id": 8474189, 
  "player_2": "Frans Nielsen", 
  "player_2_type": "Loser",
  "player_2_id": 8470144
}
```

### Formatters

The currently available formatters are `csv`, `json`, and `text`.

Using the `text` output format, we get a pretty-printed table with the data:

```
datetime                period  period_time    period_time_remaining    period_type      x    y  event_type       event_secondary_type     event_description                                                                 team_for    player_1             player_1_type      player_1_id  player_2             player_2_type      player_2_id  player_3          player_3_type      player_3_id  player_4          player_4_type      player_4_id
--------------------  --------  -------------  -----------------------  -------------  ---  ---  ---------------  -----------------------  --------------------------------------------------------------------------------  ----------  -------------------  ---------------  -------------  -------------------  ---------------  -------------  ----------------  ---------------  -------------  ----------------  ---------------  -------------
2019-11-30T23:00:31Z         1  00:00          20:00                    REGULAR                  GAME_SCHEDULED                            Game Scheduled
2019-12-01T00:08:21Z         1  00:00          20:00                    REGULAR                  PERIOD_READY                              Period Ready
2019-12-01T00:08:26Z         1  00:00          20:00                    REGULAR                  PERIOD_START                              Period Start
2019-12-01T00:08:26Z         1  00:00          20:00                    REGULAR          0    0  FACEOFF                                   Lars Eller faceoff won against Frans Nielsen                                      WSH         Lars Eller           Winner                 8474189  Frans Nielsen        Loser                  8470144
2019-12-01T00:09:03Z         1  00:20          19:40                    REGULAR         80    8  SHOT             Tip-In                   T.J. Oshie Tip-In saved by Jonathan Bernier                                       WSH         T.J. Oshie           Shooter                8471698  Jonathan Bernier     Goalie                 8473541
2019-12-01T00:09:09Z         1  00:26          19:34                    REGULAR         78  -34  HIT                                       T.J. Oshie hit Darren Helm                                                        WSH         T.J. Oshie           Hitter                 8471698  Darren Helm          Hittee                 8471794
2019-12-01T00:09:45Z         1  01:02          18:58                    REGULAR        -88   29  TAKEAWAY                                  Takeaway by Michal Kempny                                                         WSH         Michal Kempny        PlayerID               8479482
```


Using the `csv` formatter, we get csv-like output:


```csv
datetime,period,period_time,period_time_remaining,period_type,x,y,event_type,event_secondary_type,event_description,team_for,player_1,player_1_type,player_1_id,player_2,player_2_type,player_2_id,player_3,player_3_type,player_3_id,player_4,player_4_type,player_4_id
2019-12-02T01:42:03Z,1,00:00,20:00,REGULAR,,,GAME_SCHEDULED,,Game Scheduled,,,,,,,,,,,,,
2019-12-02T03:07:47Z,1,00:00,20:00,REGULAR,,,PERIOD_READY,,Period Ready,,,,,,,,,,,,,
2019-12-02T03:07:53Z,1,00:00,20:00,REGULAR,,,PERIOD_START,,Period Start,,,,,,,,,,,,,
2019-12-02T03:07:53Z,1,00:00,20:00,REGULAR,0.0,0.0,FACEOFF,,Leon Draisaitl faceoff won against Bo Horvat,EDM,Leon Draisaitl,Winner,8477934,Bo Horvat,Loser,8477500,,,,,,
2019-12-02T03:08:27Z,1,00:12,19:48,REGULAR,97.0,-19.0,HIT,,Bo Horvat hit Leon Draisaitl,VAN,Bo Horvat,Hitter,8477500,Leon Draisaitl,Hittee,8477934,,,,,,
2019-12-02T03:08:45Z,1,00:30,19:30,REGULAR,51.0,-36.0,TAKEAWAY,,Takeaway by Jordie Benn,VAN,Jordie Benn,PlayerID,8474818,,,,,,,,,
2019-12-02T03:09:16Z,1,01:01,18:59,REGULAR,-58.0,0.0,BLOCKED_SHOT,,Elias Pettersson shot blocked shot by Darnell Nurse,EDM,Darnell Nurse,Blocker,8477498,Elias Pettersson,Shooter,8480012,,,,,,
2019-12-02T03:11:13Z,1,02:58,17:02,REGULAR,76.0,-17.0,SHOT,Backhand,Joakim Nygard Backhand saved by Jacob Markstrom,EDM,Joakim Nygard,Shooter,8481638,Jacob Markstrom,Goalie,8474593,,,,,,
2019-12-02T03:11:24Z,1,03:09,16:51,REGULAR,7.0,-3.0,TAKEAWAY,,Takeaway by Tanner Pearson,VAN,Tanner Pearson,PlayerID,8476871,,,,,,,,,
```

the `json` formatter returns JSON identical to the normalized event above.
