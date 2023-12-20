import pandas as pd
from loguru import logger

from models import AgentLevelAdditions, AnnualCommissionBonus, BaseCommissionPercent


class MIC:
    def __init__(
        self,
        fyc: int,
        psy_19m: float = 0.9,
        agent_level: str = "N/A",
        agent_level_addition: dict = AgentLevelAdditions().model_dump(),
        basecommissionpercentage: BaseCommissionPercent = BaseCommissionPercent(),
    ):
        self.agent_level = agent_level
        self.agent_level_addition = agent_level_addition
        self.fyc = fyc
        self.psy_19m = psy_19m
        self.basecommissionpercentage = basecommissionpercentage

        self.base_commission_percentage = self.match_fyc(self.fyc)
        self.commission_percentage_addition = self.agent_level_addition.get(self.agent_level, 0)
        self.total_commission_percentage = round(
            (
                self.base_commission_percentage + self.commission_percentage_addition
                if self.base_commission_percentage > 0
                else 0
            ),
            4,
        )
        self.commission = self.fyc * self.total_commission_percentage

    def match_fyc(self, fyc_amount):
        """
        Assume 90% 19M PSY
        """
        assert isinstance(fyc_amount, int) | isinstance(fyc_amount, float)
        if fyc_amount < 30000:
            base_commission_percentage = self.basecommissionpercentage.less_than_30k

        elif fyc_amount in range(30000, 49999):
            base_commission_percentage = self.basecommissionpercentage.between_30k_50k

        elif fyc_amount in range(50000, 65999):
            base_commission_percentage = self.basecommissionpercentage.between_50k_66k

        elif fyc_amount in range(66000, 87999):
            base_commission_percentage = self.basecommissionpercentage.between_66k_88k

        elif fyc_amount in range(88000, 109999):
            base_commission_percentage = self.basecommissionpercentage.between_88k_109k

        elif fyc_amount >= 110000:
            base_commission_percentage = self.basecommissionpercentage.above_110k
        else:
            logger.error("Error, please check fyc_amount")
            base_commission_percentage = None
        return base_commission_percentage

    def cal_commission(self):
        return self.commission


class YIC:
    def __init__(self, annual_sales: int):
        self.annual_sales = annual_sales
        self.intervals = [0, 137500, 275000, 385000, 495000]
        self.annual_commission_bonus = AnnualCommissionBonus()
        self.annual_bonus = 0

    def get_annual_bonus(self):
        if self.annual_sales in range(self.intervals[0], self.intervals[1]):
            self.annual_bonus = self.annual_sales * (self.annual_commission_bonus.less_than_137k)
        elif self.annual_sales in range(self.intervals[1], self.intervals[2]):
            self.annual_bonus = self.annual_sales * (self.annual_commission_bonus.between_137k_275k)
        elif self.annual_sales in range(self.intervals[2], self.intervals[3]):
            self.annual_bonus = self.annual_sales * (self.annual_commission_bonus.between_275k_385)
        elif self.annual_sales in range(self.intervals[3], self.intervals[4]):
            self.annual_bonus = self.annual_sales * (self.annual_commission_bonus.between_385k_495k)
        elif self.annual_sales >= self.intervals[4]:
            self.annual_bonus = self.annual_sales * (self.annual_commission_bonus.above_495k)
        else:
            print("Error, please check annual sales")
            self.annual_bonus = 0
        self.annual_bonus = round(self.annual_bonus, 2)
        return self.annual_bonus


class Renewal:
    def __init__(self, yearly_sales: dict):
        self.yearly_sales = yearly_sales
        self.renewal_bonus = 0.15
        self.renewal_bonus_dict = {}
        logger.debug(yearly_sales.items())
        for i in range(len(yearly_sales)):
            if i > 0:
                renewal_commission = yearly_sales[i - 1] * self.renewal_bonus
                self.renewal_bonus_dict[f"Year {i+1} renewal bonus"] = renewal_commission
            else:
                self.renewal_bonus_dict[f"Year {i+1} renewal bonus"] = 0

    def get_renewal_commission(self):
        return self.renewal_bonus_dict


def cal_quarterly_commission(sales: list, agent_level: AgentLevelAdditions):
    com = []
    for i, sale in enumerate(sales):
        if i > 1:  # quarter sales starts at month 3
            commission = MIC(fyc=sale, agent_level=agent_level).cal_commission()
            com.append(commission)
        else:
            com.append(0)
    return com


def calculate_rolling_sum(lst):
    series = pd.Series(lst)
    rolling_sum = series.rolling(window=3).sum()
    rolling_sum.fillna(0, inplace=True)
    return rolling_sum.tolist()


def calculate_rolling_commission(sales_df: pd.DataFrame, agent_level: str) -> pd.DataFrame:
    sales_df["rolling_sales"] = calculate_rolling_sum(sales_df.sales)
    sales_df.fillna(0, inplace=True)
    sales_df["rolling_commission"] = cal_quarterly_commission(
        sales_df["rolling_sales"].values, agent_level=agent_level
    )
    return sales_df


def cal_annual_sales(sales_df):
    return sales_df.sales.sum()
