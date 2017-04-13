# -*- coding: utf-8 -*-

import numpy as np
import datetime as dt
from AlgoTrading.Strategy.Strategy import Strategy
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from PyFin.api import HIST
from decouple import config
from pyStratAssetAlloc.enum import AssetWeight
from pyStratAssetAlloc.enum import AssetClass
from pyStratAssetAlloc.portfolio import Portfolio


class RISKPARITY(Strategy):
    def __init__(self, window, assets, tiaocang_freq, weight_type=AssetWeight.RISK_PARITY):
        self._assets = assets
        self._moving_cov = None
        self._weight_type = weight_type
        self._nb_asset = len(self._assets)
        self._hist_close = HIST(window, 'close')
        self._cov_window = window
        self._count = 0
        self._tiaocang_freq = tiaocang_freq

    def _update_asset_target_weight(self):
        if self._weight_type == AssetWeight.EQUAL:
            ret = dict(zip(self._assets.keys(), [1.0 / self._nb_asset] * self._nb_asset))
        elif self._weight_type == AssetWeight.RISK_PARITY:
            try:
                ptf = Portfolio(asset_cov=self._moving_cov, asset_name=self._assets.keys())
                x0 = [self._assets[asset]['target_weight'] for asset in self._assets]
                ptf.calc_risk_parity_weight(x0=x0)
                ret = ptf.asset_weight.to_dict()
            except ValueError:
                ret = {asset: self._assets[asset]['default_weight'] for asset in self._assets}
        else:
            raise NotImplementedError
        for asset in self._assets:
            self._assets[asset]['target_weight'] = ret[asset]

    def _update_cov(self):
        return_matrix = None
        for asset in self._assets:
            price = np.array(self._hist_close[asset][:self._cov_window])[::-1]
            return_asset = np.diff(price) / price[:-1]
            return_matrix = return_asset if return_matrix is None else np.vstack((return_matrix, return_asset))

        self._moving_cov = np.cov(return_matrix)

    def handle_data(self):
        if self._count % self._tiaocang_freq == 0:
            self._update_cov()
            self._update_asset_target_weight()
            for sec in self.universe:
                if np.isnan(self._assets[sec]['target_weight']):
                    self._assets[sec]['target_weight'] = self._assets[sec]['default_weight']
                self.order_to_pct(sec, 1, self._assets[sec]['target_weight'])
                self.keep('target_weight_' + sec, self._assets[sec]['target_weight'])
        self._count += 1


def run_example():
    universe = ['510300.xshg', '510500.xshg', '511010.xshg', '518880.xshg']
    assets = {
        '510300.xshg': {'asset_class': AssetClass.EQUITY,
                        'current_pos': 0.0,
                        'target_weight': 0.0,
                        'default_weight': 0.075},

        '510500.xshg': {'asset_class': AssetClass.EQUITY,
                        'current_pos': 0.0,
                        'target_weight': 0.0,
                        'default_weight': 0.075},
        '511010.xshg': {'asset_class': AssetClass.BOND,
                        'current_pos': 0.0,
                        'target_weight': 0.0,
                        'default_weight': 0.75},
        '518880.xshg': {'asset_class': AssetClass.GOLD,
                        'current_pos': 0.0,
                        'target_weight': 0.0,
                        'default_weight': 0.1}
    }
    start_date = dt.datetime(2013, 8, 1)
    end_date = dt.datetime(2017, 2, 28)
    window = config('RISKPARITY_WINDOW', cast=float)
    tiaocang_freq = config('RISKPARITY_TIAOCANG_FREQ', cast=int)

    strategyRunner(userStrategy=RISKPARITY,
                   strategyParameters=(window, assets, tiaocang_freq),
                   symbolList=universe,
                   startDate=start_date,
                   endDate=end_date,
                   benchmark='000300.zicn',
                   dataSource=DataSource.WIND,
                   logLevel='info',
                   saveFile=True,
                   portfolioType=PortfolioType.CashManageable,
                   plot=True,
                   freq='D',
                   priceAdj='F')


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
