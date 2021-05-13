from datetime import timedelta

### Event types and info
GOAL = "GOAL"
SHOT = "SHOT"
MISS = "MISSED_SHOT"
BLOCK = "BLOCKED_SHOT"


SHOT_EVENTS = (GOAL, SHOT)
FENWICK_EVENTS = (GOAL, SHOT, MISS)
CORSI_EVENTS = (GOAL, SHOT, MISS, BLOCK)


# Location
NET_X_LOCATION = 89


# Time
ONE_PERIOD = timedelta(minutes=20)
FULL_GAME = timedelta(minutes=60)
