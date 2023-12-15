from pydantic import BaseModel


class BaseCommissionPercent(BaseModel):
    less_than_30k: float = 0
    between_30k_50k: float = 0.2
    between_50k_66k: float = 0.25
    between_66k_88k: float = 0.3
    between_88k_109k: float = 0.325
    above_110k: float = 0.375


class AgentLevelAdditions(BaseModel):
    NONE: float = 0
    MFP: float = 0.05
    SMFP: float = 0.075
    EMFP: float = 0.1


class AnnualCommissionBonus(BaseModel):
    less_than_137k: float = 0
    between_137k_275k: float = 0.17
    between_275k_385: float = 0.2
    between_385k_495k: float = 0.25
    above_495k: float = 0.275
