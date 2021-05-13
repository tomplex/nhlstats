import pytest

from nhlstats.time_tracking import TimeDelta, _shave_seconds, GameTime


@pytest.mark.parametrize('seconds,expected', [
    (10, (0, 10)),
    (30, (0, 30)),
    (61, (1, 1)),
    (122, (2, 2)),
])
def test_shave_seconds(seconds, expected):
    assert _shave_seconds(seconds) == expected


@pytest.mark.parametrize('et_args,tte', [
    [
        ('10:30', 1),
        '10:30'
    ],
    [
        ('10:30', 2),
        '30:30'
    ],
])
def test_event_time_elapsed(et_args, tte):
    et = GameTime(*et_args)
    assert et.total_time_elapsed == tte
