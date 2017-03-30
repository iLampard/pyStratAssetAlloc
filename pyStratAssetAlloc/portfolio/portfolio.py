# -*- coding: utf-8 -*-
# ref: https://github.com/bergarog/spicy-selection/toolbox/FactorPortfolio.py
# ref: https://github.com/ailzy/riskim/blob/master/portfolio/portfolio.py

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from PyFin.Utilities import pyFinWarning


class Portfolio(object):
    def __init__(self, **kwargs):
        self._mu = kwargs.get('mu', None)
        self._sd = kwargs.get('sd', None)
        self._ir = kwargs.get('ir', None)
        self._mu_min = np.nan
        self._mu_max = np.nan
        self._desc = kwargs.get('desc', 'Portfolio')
        self._tol = kwargs.get('tol', 1e-10)
        self._asset_return = kwargs.get('asset_return', None)
        self._asset_mu = kwargs.get('asset_mu', None)
        self._asset_cov = kwargs.get('asset_cov', None)
        self._asset_weight = kwargs.get('asset_weight', None)
        self._asset_name = kwargs.get('asset_name', None)

        pyFinWarning(not (self._asset_return is not None and self._asset_mu is not None),
                     UserWarning,
                     "When both asset return and asset mu is given, only asset mu {0} will be used".format(
                         self._asset_mu))

        if self._asset_name is None:
            if isinstance(self._asset_mu, pd.DataFrame) or isinstance(self._asset_mu, pd.Series):
                self._asset_name = self._asset_mu.index
            elif isinstance(self._asset_cov, pd.DataFrame):
                self._asset_name = self._asset_cov.index
            elif isinstance(self._asset_weight, pd.DataFrame) or isinstance(self._asset_mu, pd.Series):
                self._asset_name = self._asset_weight.index
            else:
                self._asset_name = pd.Index(['Asset_' + str(i) for i in range(len(self._asset_cov))]) \
                    if self._asset_cov is not None else \
                    pd.Index(['Asset_' + str(i) for i in range(len(self._asset_return))])

        self._nb_asset = len(self._asset_name)

        if self._asset_mu is None:
            if self._asset_return is None:
                self._asset_mu = pd.Series({'mu': np.repeat(np.nan, self._nb_asset, 0)}, index=self._asset_name)
            else:
                mu = np.mean(self._asset_return, axis=0)
                self._asset_mu = pd.Series({'mu': mu}, index=self._asset_name)
        else:
            self._mu_min = np.ceil(self._asset_mu.min()[0] / self._tol) * self._tol
            self._mu_max = np.floor(self._asset_mu.max()[0] / self._tol) * self._tol

        if self._asset_cov is None:
            if self._asset_return is None:
                tmp = np.empty((self._nb_asset, self._nb_asset))
                tmp[:] = np.nan
            else:
                tmp = np.cov(self._asset_return)
            self._asset_cov = pd.DataFrame(tmp, index=self._asset_name, columns=self._asset_name)

    def calc_mu(self):
        self._mu = np.dot(self._asset_weight, self._asset_mu)

    def calc_sd(self):
        self._sd = np.sqrt(np.dot(np.dot(self._asset_weight, self._asset_cov), self._asset_weight))

    def calc_ir(self):
        self._ir = self._mu / self._sd

    def calc_risk_parity_weight(self, x0=None):
        cov = np.matrix(self._asset_cov)

        def fun(x):
            tmp = (cov * np.matrix(x).T).A1
            risk = x * tmp
            delta_risk = [sum((i - risk) ** 2) for i in risk]
            return sum(delta_risk)

        x0 = np.ones(cov.shape[0]) / cov.shape[0] if x0 is None else x0
        bnds = tuple((0, None) for x in x0)
        cons = ({'type': 'eq', 'fun': lambda x: sum(x) - 1})
        options = {'disp': False, 'maxiter': 1000, 'ftol': 1e-20}

        res = minimize(fun, x0, bounds=bnds, constraints=cons, method='SLSQP', options=options)

        w = res['x']
        w = np.divide(w, w.sum())
        self._asset_weight = pd.Series(w, index=self._asset_name)
        self._desc = 'Risk Parity Portfolio'
        self.calc_mu()
        self.calc_sd()
        self.calc_ir()

    @property
    def mu(self):
        return self._mu

    @property
    def sd(self):
        return self._sd

    @property
    def ir(self):
        return self._ir

    @property
    def asset_weight(self):
        return self._asset_weight

    @asset_weight.setter
    def asset_weight(self, weight):
        self._asset_weight = weight

    @property
    def asset_cov(self):
        return self._asset_cov

    @asset_cov.setter
    def asset_cov(self, cov):
        self._asset_cov = cov


if __name__ == "__main__":
    n = 10

    A = np.random.sample([n, n])

    # Q is our covariance matrix
    Q = np.dot(A, A.transpose())

    x = [[1, 0.2], [0.2, 1]]
    ptf = Portfolio(asset_cov=x)
    ptf.calc_risk_parity_weight()
    print ptf.asset_weight
