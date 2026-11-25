"""Irrigation input validation. Invalid inputs return None without raising."""

import math


def _parts(text, separator):
    if not isinstance(text, str):
        return None
    parts = text.split(separator)
    return parts if len(parts) == 2 else None


def _number(text):
    try:
        value = float(text)
    except (ValueError, OverflowError):
        return None
    return value if math.isfinite(value) and value >= 0 else None


def parse_zone(text):
    """Parse name:area; require a nonempty name and finite, nonnegative area."""
    parts = _parts(text, ':')
    if parts is None:
        return None
    name, raw_area = parts
    name = name.strip().title()
    area = _number(raw_area)
    if not name or area is None:
        return None
    return name, area


def moisture_average(readings_csv):
    """Return the arithmetic mean of finite readings in [0, 100], or None."""
    if not isinstance(readings_csv, str):
        return None
    values = [_number(item) for item in readings_csv.split(',')]
    if any(value is None or value > 100 for value in values):
        return None
    return math.fsum(values) / len(values)


def water_needed(text):
    """Return max(area * 5 - rainfall, 0); invalid/overflowing inputs give None."""
    parts = _parts(text, '|')
    if parts is None:
        return None
    area, rain = (_number(part) for part in parts)
    if area is None or rain is None:
        return None
    need = area * 5 - rain
    return max(need, 0.0) if math.isfinite(need) else None


def main():
    tasks = [
        ('parse_zone', 'Enter zone:area in m2 (e.g. north:120): ', parse_zone, 'Zone and Area:'),
        ('moisture_average', 'Enter moisture readings as CSV (e.g. 40,35,50): ', moisture_average, 'Average Moisture:'),
        ('water_needed', 'Enter area|rainfall (e.g. 120|8): ', water_needed, 'Water Needed:'),
    ]
    for index, (name, prompt, function, label) in enumerate(tasks):
        print(('\n' if index else '') + f'==== Running {name} ====')
        try:
            result = function(input(prompt))
        except EOFError:
            print('Input ended.')
            return
        print(label, result if result is not None else 'Invalid input')


if __name__ == '__main__':
    main()
