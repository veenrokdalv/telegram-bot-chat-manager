import datetime as dt
import re
import typing

from aiogram import types

PATTERN = re.compile(r"(?P<value>\d+)(?P<modifier>[wdhms])")
LINE_PATTERN = re.compile(r"^(\d+[wdhms]){1,}$")

MODIFIERS = {
    "w": dt.timedelta(weeks=1),
    "d": dt.timedelta(days=1),
    "h": dt.timedelta(hours=1),
    "m": dt.timedelta(minutes=1),
    "s": dt.timedelta(seconds=1),
}


class TimedeltaParseError(Exception):
    pass


def parse_timedelta(value: str, default: dt.timedelta = None) -> dt.timedelta:
    if value is None:
        return default
    match = LINE_PATTERN.match(value)
    if not match:
        if default:
            return default
        raise TimedeltaParseError("Invalid time format")

    try:
        result = dt.timedelta()
        for match in PATTERN.finditer(value):
            value, modifier = match.groups()

            result += int(value) * MODIFIERS[modifier]
    except OverflowError:
        if default:
            return default
        raise TimedeltaParseError("Timedelta value is too large")

    return result