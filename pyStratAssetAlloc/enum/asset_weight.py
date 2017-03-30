# -*- coding: utf-8 -*-


from enum import IntEnum
from enum import unique


@unique
class AssetWeight(IntEnum):
    EQUAL = 0
    RISK_PARITY = 1
