import re

from functools import partial

from slugify import slugify as _slugify


slugify = partial(_slugify, to_lower=True, max_length=50)


EXTRACT_SPEAKERS_RE = re.compile('speaker[s]?: (.+)', re.IGNORECASE)


def extract_speakers(text):
    match = EXTRACT_SPEAKERS_RE.findall(text)

    result = []
    for line in match:
        result += [speaker.strip() for speaker in line.split(',')]

    return result
