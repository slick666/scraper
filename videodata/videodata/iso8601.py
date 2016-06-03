import re
from datetime import timedelta

DURATION_RE = re.compile(
    '^(?P<neg>-?)'
    'P((?P<years>\d+)Y)?'
    '((?P<months>\d+)M)?'
    '((?P<days>\d+)D)?'
    '(?P<Time>T'
    '((?P<hours>\d+)H)?'
    '((?P<minutes>\d+)M)?'
    '(((?P<seconds>\d+)'
    '(?P<fracsec>\.\d+)?)S)?)?$')


def duration_as_seconds(duration):
    d = DURATION_RE.match(duration).groupdict(0)
    delta = timedelta(
        days=int(d['days']) + (int(d['months']) * 30) + (int(d['years']) * 365),
        hours=int(d['hours']), minutes=int(d['minutes']), seconds=int(d['seconds']))

    if d['neg'] == "-":
        delta *= -1

    return int(delta.total_seconds())
