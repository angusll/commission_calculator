import pandas as pd
from pydantic import BaseModel
from models import (
    AgentLevelAdditions,
    BaseCommissionPercent,
    AnnualCommissionBonus,
)


class MIC:
    def __init__(
        self,
        FYC: int,
        PSY_19M: float = 0.9,
        agent_level: str = "N/A",
        agent_level_addition: dict = AgentLevelAdditions().model_dump(),
        BaseCommissionPercent: BaseModel = BaseCommissionPercent(),
    ):
        self.agent_level = agent_level
        self.agent_level_addition = agent_level_addition
        self.FYC = FYC
        self.PSY_19M = PSY_19M
        self.BaseCommissionPercent = BaseCommissionPercent

    def match_fyc(self, fyc_amount):
        """
        Assume 90% 19M PSY
        """
        assert isinstance(fyc_amount, int) | isinstance(fyc_amount, float)
        if fyc_amount < 30000:
            return self.BaseCommissionPercent.less_than_30k
        elif fyc_amount in range(30000, 49999):
            return self.BaseCommissionPercent.between_30k_50k
        elif fyc_amount in range(50000, 65999):
            return self.BaseCommissionPercent.between_50k_66k
        elif fyc_amount in range(66000, 87999):
            return self.BaseCommissionPercent.between_66k_88k
        elif fyc_amount in range(88000, 109999):
            return self.BaseCommissionPercent.between_88k_109k
        elif fyc_amount >= 110000:
            return self.BaseCommissionPercent.above_110k
        else:
            print("Error, please check FYC amount")

    def cal_commission(self):
        self.bass_commission_percentage = self.match_fyc(self.FYC)
        self.commission_percentage_addition = self.agent_level_addition.get(
            self.agent_level, 0
        )
        self.total_commission_percentage = round(
            (
                self.bass_commission_percentage
                + self.commission_percentage_addition
                if self.bass_commission_percentage > 0
                else 0
            ),
            2,
        )
        self.commission = self.FYC * self.total_commission_percentage
        return self.commission


class YIC:
    def __init__(self, annual_sales):
        self.annual_sales = annual_sales
        self.intervals = [0, 137500, 275000, 385000, 495000]
        self.annual_commission_bonus = AnnualCommissionBonus()

    def get_annual_bonus(self):
        if self.annual_sales in range(self.intervals[0], self.intervals[1]):
            self.annual_bonus = self.annual_sales * (
                1 + self.annual_commission_bonus.less_than_137k
            )
        elif self.annual_sales in range(self.intervals[1], self.intervals[2]):
            self.annual_bonus = self.annual_sales * (
                1 + self.annual_commission_bonus.between_137k_275k
            )
        elif self.annual_sales in range(self.intervals[2], self.intervals[3]):
            self.annual_bonus = self.annual_sales * (
                1 + self.annual_commission_bonus.between_275k_385
            )
        elif self.annual_sales in range(self.intervals[3], self.intervals[4]):
            self.annual_bonus = self.annual_sales * (
                1 + self.annual_commission_bonus.between_385k_495k
            )
        elif self.annual_sales >= self.intervals[4]:
            self.annual_bonus = self.annual_sales * (
                1 + self.annual_commission_bonus.above_495k
            )
        else:
            print("Error, please check annual sales")
            self.annual_bonus = 0
        return self.annual_bonus


def cal_quarterly_commission(sales, agent_level: AgentLevelAdditions):
    com = []
    for month, _ in enumerate(sales):
        if month in range(2, 3):
            quaterly_sales = sum(sales[:3])
            commission = MIC(
                FYC=quaterly_sales, agent_level=agent_level
            ).cal_commission()
            com.append(commission)
        elif month in range(3, 6):
            quaterly_sales = sum(sales[4:7])
            commission = MIC(
                FYC=quaterly_sales, agent_level=agent_level
            ).cal_commission()
            com.append(commission)
        elif month in range(6, 9):
            quaterly_sales = sum(sales[7:10])
            commission = MIC(
                FYC=quaterly_sales, agent_level=agent_level
            ).cal_commission()
            com.append(commission)
        elif month in range(9, 12):
            quaterly_sales = sum(sales[10:13])
            commission = MIC(
                FYC=quaterly_sales, agent_level=agent_level
            ).cal_commission()
            com.append(commission)
        else:
            com.append(0)
    return com


def calculate_rolling_sum(lst):
    series = pd.Series(lst)
    rolling_sum = series.rolling(window=3).sum()
    return rolling_sum.tolist()


def calculate_rolling_commission(
    sales_df: pd.DataFrame, agent_level: str
) -> pd.DataFrame:
    sales_df["rolling_sales"] = calculate_rolling_sum(sales_df.sales)
    sales_df.fillna(0, inplace=True)
    sales_df["rolling_commission"] = cal_quarterly_commission(
        sales_df["rolling_sales"].values, agent_level=agent_level
    )
    return sales_df


def cal_annual_sales(sales_df):
    return sales_df.sales.sum()
