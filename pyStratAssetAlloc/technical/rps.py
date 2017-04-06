# -*- coding: utf-8 -*-

from PyFin.api import MAX
from PyFin.api import MIN
from PyFin.api import MA
from PyFin.api import SUM


def SecurityRPS(window_min_max, window_ma, dependency):
    RPS = (SUM(1, dependency=dependency) - MIN(window=window_min_max, dependency=dependency)) / (
        MAX(window=window_min_max, dependency=dependency) - MIN(window=window_min_max, dependency=dependency))
    RPS = MA(dependency=RPS, window=window_ma)
    return RPS
