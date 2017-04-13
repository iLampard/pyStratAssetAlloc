# -*- coding: utf-8 -*-

from PyFin.api import MMAX
from PyFin.api import MMIN
from PyFin.api import MA
from PyFin.api import MSUM


def SecurityRPS(window_min_max, window_ma, dependency):
    RPS = (MSUM(1, dependency=dependency) - MMIN(window=window_min_max, dependency=dependency)) / (
        MMAX(window=window_min_max, dependency=dependency) - MMIN(window=window_min_max, dependency=dependency))
    RPS = MA(dependency=RPS, window=window_ma)
    return RPS
