# -*- coding: utf-8 -*-


from enum import IntEnum
from enum import unique


@unique
class DataSource(IntEnum):
    CSV = 0
    WIND = 1
    TUSHARE = 2
    MYSQL_LOCAL = 3
