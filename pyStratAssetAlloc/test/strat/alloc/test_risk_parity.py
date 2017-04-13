# -*- coding: utf-8 -*-


import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from pyStratAssetAlloc.strat.alloc import RISKPARITY


class Test_risk_parity(unittest.TestCase):
    def setUp(self):
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
        csv_dir = 'data'
        window1 = 50
        window2 = 250
        tiaocang_freq1 = 10
        tiaocang_freq2 = 30
        self.data = {'universe': universe,
                     'assets': assets,
                     'csv_dir': csv_dir,
                     'window1': window1,
                     'window2': window2,
                     'tiaocang_freq1': tiaocang_freq1,
                     'tiaocang_freq2': tiaocang_freq2}

    def test_strat_perf1(self):
        universe = self.data['universe']
        assets = self.data['assets']
        window = self.data['window1']
        tiaocang_freq = self.data['tiaocang_freq1']
        csv_dir = self.data['csv_dir']
        perf = strategyRunner(userStrategy=RISKPARITY,
                              strategyParameters=(window, assets, tiaocang_freq),
                              symbolList=universe,
                              dataSource=DataSource.CSV,
                              csvDir=csv_dir,
                              saveFile=False,
                              portfolioType=PortfolioType.CashManageable,
                              plot=False
                              )['perf_metric']
        expected = np.array([[0.062293], [0.044556], [2.008244], [1.398091], [-0.046593], [482], [388]])
        assert_array_almost_equal(perf.values, expected)

    def test_strat_perf2(self):
        universe = self.data['universe']
        assets = self.data['assets']
        window = self.data['window2']
        tiaocang_freq = self.data['tiaocang_freq2']
        csv_dir = self.data['csv_dir']
        perf = strategyRunner(userStrategy=RISKPARITY,
                              strategyParameters=(window, assets, tiaocang_freq),
                              symbolList=universe,
                              dataSource=DataSource.CSV,
                              csvDir=csv_dir,
                              saveFile=False,
                              portfolioType=PortfolioType.CashManageable,
                              plot=False
                              )['perf_metric']
        expected = np.array([[0.064036], [0.046573], [1.850819], [1.374968], [-0.056908], [486], [384]])
        assert_array_almost_equal(perf.values, expected)
