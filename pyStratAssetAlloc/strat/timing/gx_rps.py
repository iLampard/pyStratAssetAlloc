# -*- coding: utf-8 -*-

# ref: 黄志文，单向波动率差值研究择时之二：RPS分级靠档减少交易频率，国信证券，2016

import datetime as dt
import numpy as np
from AlgoTrading.Strategy.Strategy import Strategy
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from decouple import config
from pyStratAssetAlloc.technical import RPS
from PyFin.api import HIST
import itertools

class GXRPS(Strategy):
    def __init__(self, window_min_max, window_ma, vol_diff_slice):
        self.rps = RPS(window_min_max=window_min_max, window_ma=window_ma, dependency='close')
        self.hist_open = HIST(100, 'open')
        self.hist_high = HIST(100, 'high')
        self.hist_low = HIST(100, 'low')
        self.vol_diff_slice = vol_diff_slice

    def handle_data(self):
        for sec in self.universe:
            if np.isnan(self.rps[sec]):
                continue
            window = get_window_layer(self.rps[sec]) if self.vol_diff_slice else int(self.rps[sec] * 100)
            price_open = self.hist_open[sec][:window]
            price_high = self.hist_high[sec][:window]
            price_low = self.hist_low[sec][:window]
            signal = calc_vol_diff(price_open, price_high, price_low)

            if signal > 0 >= self.secPos[sec]:
                self.order_to_pct(sec, 1, 1)
            elif signal < 0 <= self.secPos[sec]:
                self.order_to_pct(sec, -1, 1)


def calc_vol_diff(price_open, price_high, price_low):
    return np.mean((price_high - price_open) / price_open - (price_open - price_low) / price_open)


def get_window_layer(rps):
    if rps <= 0.2:
        window = 20
    elif rps <= 0.4:
        window = 40
    elif rps <= 0.6:
        window = 60
    elif rps <= 0.8:
        window = 80
    else:
        window = 100
    return window


def run_example():
    universe = ['000300.zicn']
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2017, 4, 1)
    window_min_max = config('GX_WINDOW_MIN_MAX', default=250, cast=int)
    window_ma = config('GX_WINDOW_MA', default=9, cast=int)
    vol_diff_slice = config('GX_VOL_DIFF_SLICE', default=False, cast=bool)
    strategyRunner(userStrategy=GXRPS,
                   strategyParameters=(window_min_max, window_ma, vol_diff_slice),
                   symbolList=universe,
                   startDate=start_date,
                   endDate=end_date,
                   benchmark='000300.zicn',
                   logLevel='info',
                   saveFile=True,
                   portfolioType=PortfolioType.CashManageable,
                   plot=True,
                   freq='D')

def parameters_generator():
    window_min_max = range(200, 215, 5)
    window_ma = range(1, 3, 1)
    vol_diff_slice = [True, False]
    return itertools.product(window_min_max, window_ma, vol_diff_slice), ['min_max', 'ma', 'vol_diff_slice']

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
