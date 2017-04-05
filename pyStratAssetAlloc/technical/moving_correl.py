# -*- coding: utf-8 -*-

from PyFin.Math.Accumulators.StatefulAccumulators import MovingCorrelationMatrix
from PyFin.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecuritySingleValueHolder


class SecurityMovingCorrelationMatrix(SecuritySingleValueHolder):
    def __init__(self, window, dependency='values'):
        super(SecurityMovingCorrelationMatrix, self).__init__(window=window, HolderType=MovingCorrelationMatrix,
                                                              dependency=dependency)

    def __deepcopy__(self, memo):
        if self._compHolder:
            return SecurityMovingCorrelationMatrix(self._window - self._compHolder._window, self._compHolder)
        else:
            return SecurityMovingCorrelationMatrix(self._window, self._dependency)

    def __reduce__(self):
        d = {}
        if self._compHolder:
            return SecurityMovingCorrelationMatrix, (self._window - self._compHolder._window, self._compHolder), d
        else:
            return SecurityMovingCorrelationMatrix, (self._window, self._dependency), d

    def __setstate__(self, state):
        pass
