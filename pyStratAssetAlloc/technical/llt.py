# -*- coding: utf-8 -*-

from PyFin.Math.Accumulators.IAccumulators import StatelessSingleValueAccumulator
from PyFin.Math.Accumulators.StatefulAccumulators import MovingHistoricalWindow
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityStatelessSingleValueHolder
from collections import deque
import numpy as np


class LLT(StatelessSingleValueAccumulator):
    def __init__(self, dependency, alpha):
        super(LLT, self).__init__(dependency)
        self._underlying = MovingHistoricalWindow(window=3, dependency=dependency)
        self._llt = deque(maxlen=2)
        self._alpha = alpha

    def push(self, data):
        self._underlying.push(data)
        value = self._underlying.result()[0]
        if np.isnan(value):
            return np.nan
        if len(self._llt) == 2:
            item = np.zeros(5)
            item[0] = (self._alpha - self._alpha ** 2 / 4.0) * (self._underlying.result()[0])
            item[1] = (self._alpha ** 2 / 2.0) * (self._underlying.result()[1])
            item[2] = -(self._alpha - 3 * (self._alpha ** 2) / 4.0) * (self._underlying.result()[2])
            item[3] = 2 * (1 - self._alpha) * self._llt[1]
            item[4] = -(1 - self._alpha) ** 2 * self._llt[0]
            self._llt.append(sum(item))
        else:
            self._llt.append(value)

    def result(self):
        return self._llt[-1]

    def __deepcopy__(self, memo):
        return LLT(self._dependency, self._alpha)

    def __reduce__(self):
        d = {}
        return LLT, (self._dependency, self._alpha), d

    def __setstate__(self, state):
        pass


class SecurityLLT(SecurityStatelessSingleValueHolder):
    def __init__(self, alpha=2.0/61.0, dependency='x'):
        super(SecurityLLT, self).__init__(holderType=LLT, dependency=dependency, alpha=alpha)

    def __deepcopy__(self, memo):
        if self._compHolder:
            return SecurityLLT(self._holderTemplate._alpha, self._compHolder)
        else:
            return SecurityLLT(self._holderTemplate._alpha, self._dependency)

    def __reduce__(self):
        d = {}
        if self._compHolder:
            return SecurityLLT, (self._holderTemplate._alpha, self._compHolder), d
        else:
            return SecurityLLT, (self._holderTemplate._alpha, self._dependency), d

    def __setstate__(self, state):
        pass


