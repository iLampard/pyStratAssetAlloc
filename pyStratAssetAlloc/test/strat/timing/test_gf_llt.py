# -*- coding: utf-8 -*-


import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from pyStratAssetAlloc.strat.timing import GFLLT


class Test_GF_LLT(unittest.TestCase):
    def setUp(self):
        self._data = [1] * 2
        self._expected = [1] * 2
        universe = ['000300.zicn']
        csv_dir = 'data'
        self._data[0] = {'universe': universe,
                         'csv_dir': csv_dir,
                         'alpha': 2.0 / 61.0}
        self._data[1] = {'universe': universe,
                         'csv_dir': csv_dir,
                         'alpha': 20.0 / 61.0}
        expected_index = ['annual_return', 'annual_volatiltiy', 'sortino_ratio',
                          'sharp_ratio', 'max_draw_down', 'winning_days', 'lossing_days']
        self._expected[0] = pd.DataFrame(
            data=[[0.0312444883243], [0.0400511680075], [1.03412067824], [0.780114285768], [-0.0393086330663], [572.0],
                  [546.0]], index=expected_index,
            columns=['metrics'])
        self._expected[1] = pd.DataFrame(
            data=[[-0.00779766097657], [0.0429844125603], [-0.211985661959], [-0.181406712622], [-0.0739925824059],
                  [508.0],
                  [513.0]], index=expected_index,
            columns=['metrics'])

    def test_gf_llt_strat(self):
        for i in range(len(self._data)):
            data = self._data[i]
            perf = strategyRunner(userStrategy=GFLLT,
                                  strategyParameters=(data['alpha'],),
                                  symbolList=data['universe'],
                                  dataSource=DataSource.CSV,
                                  csvDir=data['csv_dir'],
                                  saveFile=False,
                                  portfolioType=PortfolioType.CashManageable,
                                  plot=False
                                  )['perf_metric']
            assert_frame_equal(perf, self._expected[i])
