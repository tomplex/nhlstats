### NHL Stats CLI

a CLI tool for collecting stats from the NHL API.


#### Install

```bash
pip install nhlstatscli
```

This will add a new command to your system, `nhl`.

#### Usage

```
❯ nhl
Usage: nhl [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  list-games
  list-plays
  list-shots
```

Multiple output formats are available for collected data. The default is `text`, which will pretty-print the data out in tables.
Other options include `csv`, `json`, which will output a nested JSON like `{"plays": [...]}`. 

Future plans include support for some RDBM systems.


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
