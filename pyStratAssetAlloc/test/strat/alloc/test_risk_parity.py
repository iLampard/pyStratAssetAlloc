# -*- coding: utf-8 -*-

import unittest
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from pyStratAssetAlloc.strat.alloc.risk_parity import RISKPARITY
from numpy.testing import assert_array_almost_equal

class Test_risk_parity(unittest.TestCase):
    def test_strat_perf(self):
        universe = ['510300.xshg', '510500.xshg', '511010.xshg', '518880.xshg']
        assets = {
            '510300.xshg': {
                            'target_weight': 0.0,
                            'default_weight': 0.075},

            '510500.xshg': {
                            'target_weight': 0.0,
                            'default_weight': 0.075},
            '511010.xshg': {
                            'target_weight': 0.0,
                            'default_weight': 0.75},
            '518880.xshg': {
                            'target_weight': 0.0,
                            'default_weight': 0.1}
        }
        window = 250
        csvDir = "data"
        tiaocang_freq = 20
        perf =  strategyRunner(userStrategy=RISKPARITY,
                         strategyParameters=(window, assets,tiaocang_freq),
                         symbolList=universe,
                         dataSource=DataSource.CSV,
                         csvDir=csvDir,
                         saveFile=False,
                         portfolioType=PortfolioType.CashManageable,
                         plot=False
                         )['perf_metric']
        assert_array_almost_equal(perf.values[0], 0.060158)
        assert_array_almost_equal(perf.values[1], 0.045429)
        assert_array_almost_equal(perf.values[2], 1.742323)
        assert_array_almost_equal(perf.values[3], 1.324199)
