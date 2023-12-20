#!/usr/bin/env python

"""Tests for `commission_calculator` package."""
import pytest
from ..commission_calculator.core import (
    MIC,
    YIC,
    Renewal,
    calculate_rolling_sum,
    cal_quarterly_commission,
)
from ..commission_calculator.models import AgentLevelAdditions, BaseCommissionPercent


@pytest.mark.parametrize(
    "fyc_percentage",
    [
        (20000, 0),
        (30000, 0.2),
        (50000, 0.25),
        (66000, 0.3),
        (88000, 0.325),
        (110000, 0.375),
    ],
)
@pytest.mark.parametrize("level", ["NONE", "MFP", "SMFP", "EMFP"])
def test_mic(fyc_percentage, level):
    percentage = list(BaseCommissionPercent().model_dump().values())
    fyc, percentage = fyc_percentage
    levels = AgentLevelAdditions()
    agent_level_addition = levels.model_dump()
    mic = MIC(fyc=fyc, agent_level=level)
    com = mic.cal_commission()

    com_addition = agent_level_addition.get(level, 0)
    expected_total_commission_percentage = round(
        (percentage + com_addition if percentage > 0 else 0),
        4,
    )
    assert com == fyc * expected_total_commission_percentage


@pytest.mark.parametrize(
    "annual_sales_percentage",
    [
        (100000, 0),
        (137500, 0.17),
        (275000, 0.2),
        (385000, 0.25),
        (495000, 0.275),
    ],
)
def test_yic(annual_sales_percentage):
    annual_sales, percentage = annual_sales_percentage
    yic = YIC(annual_sales=annual_sales)
    yic.get_annual_bonus()
    assert yic.annual_bonus == annual_sales * percentage


def test_renewal():
    yearly_sales = {
        0: 100000,
        1: 200000,
        2: 500000,
        3: 300000,
        4: 250000,
    }
    r = Renewal(yearly_sales)
    yearly_renewal_bonus_dict = r.get_renewal_commission()
    assert yearly_renewal_bonus_dict == {
        "Year 1 renewal bonus": 0,
        "Year 2 renewal bonus": 15000,
        "Year 3 renewal bonus": 30000,
        "Year 4 renewal bonus": 75000,
        "Year 5 renewal bonus": 45000,
    }


def test_calculate_rolling_sum():
    sales = [10000, 20000, 30000, 45000, 60000, 70000, 110000, 141200, 20000, 100000, 50000, 23000]
    rolling_sales = calculate_rolling_sum(sales)
    assert rolling_sales == [
        0.0,
        0.0,
        60000.0,
        95000.0,
        135000.0,
        175000.0,
        240000.0,
        321200.0,
        271200.0,
        261200.0,
        170000.0,
        173000.0,
    ]


@pytest.mark.parametrize("agent_level", ["NONE"])  # , "MFP", "SMFP", "EMFP"]
def test_cal_quarterly_commission(agent_level):
    rolling_sales = [
        0.0,
        0.0,
        60000.0,
        95000.0,
        135000.0,
        175000.0,
        240000.0,
        321200.0,
        271200.0,
        261200.0,
        170000.0,
        173000.0,
    ]

    com = cal_quarterly_commission(rolling_sales, agent_level)
    assert com == [
        0,
        0,
        15000.0,
        30875.0,
        50625.0,
        65625.0,
        90000.0,
        120450.0,
        101700.0,
        97950.0,
        63750.0,
        64875.0,
    ]
