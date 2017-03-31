# -*- coding: utf-8 -*-

from enum import IntEnum
from enum import unique


@unique
class DfReturnType(IntEnum):
    Null = 0
    MultiIndex = 1
    DateIndexAndSecIDCol = 2


@unique
class ReturnType(IntEnum):
    NonCumul = 0
    Cumul = 1
