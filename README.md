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

Using the `text` output format, we get a pretty-printed table with the same data:

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


Using the `csv` output format, we get csv-like output which can be redirected into a file, or viewed directly:

```bash
nhl list-plays 2019020406 --output-format csv > 2019020406.csv
```

```csv
datetime,period,period_time,period_time_remaining,period_type,x,y,event_type,event_secondary_type,event_description,team_for
2019-11-30T23:00:31Z,1,00:00,20:00,REGULAR,,,GAME_SCHEDULED,,Game Scheduled,
2019-12-01T00:08:21Z,1,00:00,20:00,REGULAR,,,PERIOD_READY,,Period Ready,
2019-12-01T00:08:26Z,1,00:00,20:00,REGULAR,,,PERIOD_START,,Period Start,
2019-12-01T00:08:26Z,1,00:00,20:00,REGULAR,0.0,0.0,FACEOFF,,Lars Eller faceoff won against Frans Nielsen,WSH,Lars Eller,Winner,8474189,Frans Nielsen,Loser,8470144
2019-12-01T00:09:03Z,1,00:20,19:40,REGULAR,80.0,8.0,SHOT,Tip-In,T.J. Oshie Tip-In saved by Jonathan Bernier,WSH,T.J. Oshie,Shooter,8471698,Jonathan Bernier,Goalie,8473541
2019-12-01T00:09:09Z,1,00:26,19:34,REGULAR,78.0,-34.0,HIT,,T.J. Oshie hit Darren Helm,WSH,T.J. Oshie,Hitter,8471698,Darren Helm,Hittee,8471794
2019-12-01T00:09:45Z,1,01:02,18:58,REGULAR,-88.0,29.0,TAKEAWAY,,Takeaway by Michal Kempny,WSH,Michal Kempny,PlayerID,8479482
2019-12-01T00:09:49Z,1,01:06,18:54,REGULAR,-56.0,34.0,GIVEAWAY,,Giveaway by Michal Kempny,WSH,Michal Kempny,PlayerID,8479482
2019-12-01T00:10:51Z,1,01:08,18:52,REGULAR,-72.0,2.0,SHOT,Wrist Shot,Luke Glendening Wrist Shot saved by Ilya Samsonov,DET,Luke Glendening,Shooter,8476822,Ilya Samsonov,Goalie,8478492
```