# -*- coding: utf-8 -*-

from enum import Enum
from enum import unique


class StrEnum(str, Enum):
    pass


@unique
class FreqType(StrEnum):
    MIN1 = 'min1'
    MIN5 = 'min5'
    MIN10 = 'min10'
    EOD = 'D'
    EOW = 'W'
    EOM = 'M'
    EOQ = 'Q'
    EOSY = 'S'
    EOY = 'Y'
