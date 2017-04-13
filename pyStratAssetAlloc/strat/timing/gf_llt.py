# -*- coding: utf-8 -*-

import datetime as dt
from AlgoTrading.Strategy.Strategy import Strategy
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from decouple import config
from pyStratAssetAlloc.technical import LLT
from PyFin.api import DIFF


class GFLLT(Strategy):
    def __init__(self, alpha):
        self.signal = DIFF(LLT(alpha=alpha, dependency='close'))

    def handle_data(self):
        for sec in self.universe:
            if self.signal[sec] > 0 >= self.secPos[sec]:
                self.order_to_pct(sec, 1, 1)
                # self.order_pct(sec, 1, 1)
            elif self.signal[sec] < 0 <= self.secPos[sec]:
                self.order_to_pct(sec, -1, 1)
                # self.order_pct(sec, -1, 1)


def run_example():
    universe = ['000300.zicn']
    start_date = dt.datetime(2013, 1, 1)
    end_date = dt.datetime(2017, 4, 1)
    alpha = config('GF_LLT_ALPHA', default=2.0/61, cast=float)

    strategyRunner(userStrategy=GFLLT,
                   strategyParameters=[alpha],
                   symbolList=universe,
                   startDate=start_date,
                   endDate=end_date,
                   benchmark='000300.zicn',
                   logLevel='info',
                   saveFile=True,
                   portfolioType=PortfolioType.CashManageable,
                   plot=True,
                   freq='D')


if __name__ == "__main__":
    from VisualPortfolio.Env import Settings
    from AlgoTrading.Env import Settings

    Settings.set_source(DataSource.WIND)
    startTime = dt.datetime.now()
    print("Start: %s" % startTime)
    run_example()
    endTime = dt.datetime.now()
    print("End : %s" % endTime)
    print("Elapsed: %s" % (endTime - startTime))
