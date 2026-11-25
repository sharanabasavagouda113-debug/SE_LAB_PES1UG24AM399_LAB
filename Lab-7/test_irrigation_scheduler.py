"""Fuzz properties and regressions for Lab 7. Same suite runs before/after."""
import math

import pytest
from hypothesis import given, settings, strategies as st

from irrigation_scheduler import parse_zone, moisture_average, water_needed

settings.register_profile('lab7', max_examples=300, derandomize=True, deadline=None)
settings.load_profile('lab7')

invalid_types = st.one_of(st.none(), st.integers(), st.floats(), st.lists(st.integers()), st.dictionaries(st.text(), st.integers()))
inputs = st.one_of(st.text(), invalid_types)


@given(inputs)
def test_parse_zone_no_crash(s):
    result = parse_zone(s)
    if result is not None:
        name, area = result
        assert name and name == name.strip().title()
        assert math.isfinite(area) and area >= 0


@given(inputs)
def test_moisture_average_no_crash(s):
    result = moisture_average(s)
    assert result is None or (math.isfinite(result) and 0 <= result <= 100)


@given(inputs)
def test_water_needed_no_crash(s):
    result = water_needed(s)
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.text(alphabet=st.characters(categories=('Lu', 'Ll')), min_size=1, max_size=30), st.integers(0, 10**12))
def test_valid_zone(name, area):
    assert parse_zone(f' {name} : {area} ') == (name.title(), float(area))


@given(st.lists(st.integers(0, 10000), min_size=1, max_size=100))
def test_valid_moisture_mean(hundredths):
    readings = [value / 100 for value in hundredths]
    result = moisture_average(','.join(map(str, readings)))
    assert result == pytest.approx(sum(readings) / len(readings))
    assert min(readings) - 1e-12 <= result <= max(readings) + 1e-12


@given(st.integers(0, 10**12), st.integers(0, 10**12))
def test_water_formula(area, rain):
    assert water_needed(f'{area}|{rain}') == max(area * 5 - rain, 0)


@pytest.mark.parametrize('function,bad', [
    (parse_zone, ''), (parse_zone, None), (parse_zone, ':12'),
    (parse_zone, 'a:1:2'), (parse_zone, 'a:-1'),
    (parse_zone, 'a:nan'), (parse_zone, 'a:inf'), (parse_zone, 'a:1e309'),
    (moisture_average, ''), (moisture_average, None),
    (moisture_average, '1,,3'), (moisture_average, 'one,two'),
    (moisture_average, '-1,40'), (moisture_average, '101'),
    (moisture_average, 'nan'), (moisture_average, 'inf'),
    (water_needed, ''), (water_needed, None), (water_needed, '1|2|3'),
    (water_needed, '-1|2'), (water_needed, '1|-2'),
    (water_needed, 'nan|0'), (water_needed, '1|inf'),
    (water_needed, '1e308|0'),
])
def test_invalid_input_returns_none(function, bad):
    assert function(bad) is None


def test_regressions():
    assert parse_zone(' north : 120 ') == ('North', 120.0)
    assert moisture_average('40,35,50') == pytest.approx(125 / 3)
    assert moisture_average('1,2') == 1.5
    assert moisture_average('0,100') == 50
    assert water_needed('120|8') == 592
    assert water_needed('0|0') == 0
    assert water_needed('1|10') == 0
