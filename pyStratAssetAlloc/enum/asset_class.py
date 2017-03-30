# -*- coding: utf-8 -*-


from enum import IntEnum
from enum import unique


@unique
class AssetClass(IntEnum):
    EQUITY = 0
    BOND = 1
    GOLD = 2
