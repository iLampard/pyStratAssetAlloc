# -*- coding: utf-8 -*-


import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from pyStratAssetAlloc.strat.timing import GFMovingAverageCrossStrategy


class Test_GF_MA(unittest.TestCase):
    def setUp(self):
        self._data = [1] * 3
        self._expected = [1] * 3
        universe = ['000300.zicn']
        csv_dir = 'data'
        self._data[0] = {'universe': universe,
                         'csv_dir': csv_dir,
                         'ma_short': 10,
                         'ma_long': 60}
        self._data[1] = {'universe': universe,
                         'csv_dir': csv_dir,
                         'ma_short': 20,
                         'ma_long': 60}
        self._data[2] = {'universe': universe,
                         'csv_dir': csv_dir,
                         'ma_short': 20,
                         'ma_long': 90}
        expected_index = ['annual_return', 'annual_volatiltiy', 'sortino_ratio',
                          'sharp_ratio', 'max_draw_down', 'winning_days', 'lossing_days']
        self._expected[0] = pd.DataFrame(
            data=[[0.0334119531608], [0.0378788034489], [1.11422822125], [0.882075200868], [-0.0971445013859], [568.0],
                  [511.0]], index=expected_index,
            columns=['metrics'])
        self._expected[1] = pd.DataFrame(
            data=[[0.0392246180704], [0.0397974178228], [1.30798716006], [0.985607112627], [-0.0465460814751], [543.0],
                  [494.0]], index=expected_index,
            columns=['metrics'])
        self._expected[2] = pd.DataFrame(
            data=[[0.0222488042899], [0.0408943901087], [0.702893022311], [0.544055168222], [-0.0653831830083],
                  [523.0],
                  [503.0]], index=expected_index,
            columns=['metrics'])

    def test_gf_ma_strat(self):
        for i in range(len(self._data)):
            data = self._data[i]
            perf = strategyRunner(userStrategy=GFMovingAverageCrossStrategy,
                                  strategyParameters=(data['ma_short'], data['ma_long']),
                                  symbolList=data['universe'],
                                  dataSource=DataSource.CSV,
                                  csvDir=data['csv_dir'],
                                  saveFile=False,
                                  portfolioType=PortfolioType.CashManageable,
                                  plot=False
                                  )['perf_metric']
            assert_frame_equal(perf, self._expected[i])
