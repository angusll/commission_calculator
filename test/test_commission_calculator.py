#!/usr/bin/env python

"""Tests for `commission_calculator` package."""
import pytest
from ..commission_calculator.core import MIC, YIC
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
