# -*- coding: utf-8 -*-

from enum import IntEnum
from enum import unique


@unique
class TimeUnit(IntEnum):
    BDays = 0
    Days = 1
    Weeks = 2
    Months = 3
    Years = 4
