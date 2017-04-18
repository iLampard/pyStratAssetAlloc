# -*- coding: utf-8 -*-

import os
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from pyStratAssetAlloc.strat.timing import GXRPS


class TestGXRPS(unittest.TestCase):
    def setUp(self):
        self._data = [1] * 4
        self._expected = [1] * 4
        universe = ['000300.zicn']
        dir_name = os.path.dirname(os.path.abspath(__file__))
        csv_dir = os.path.join(dir_name, 'data/')
        self._data[0] = {'universe': universe,
                         'csv_dir': csv_dir,
                         'window_min_max': 200,
                         'window_ma': 5,
                         'vol_diff_slice': True}
        self._data[1] = {'universe': universe,
                         'csv_dir': csv_dir,
                         'window_min_max': 200,
                         'window_ma': 10,
                         'vol_diff_slice': False}
        self._data[2] = {'universe': universe,
                         'csv_dir': csv_dir,
                         'window_min_max': 250,
                         'window_ma': 10,
                         'vol_diff_slice': True}
        self._data[3] = {'universe': universe,
                         'csv_dir': csv_dir,
                         'window_min_max': 300,
                         'window_ma': 15,
                         'vol_diff_slice': False}
        expected_index = ['annual_return', 'annual_volatiltiy', 'sortino_ratio',
                          'sharp_ratio', 'max_draw_down', 'winning_days', 'lossing_days']
        self._expected[0] = pd.DataFrame(
            data=[[0.052933970658], [0.0380450295394], [1.76057707769], [1.39135049437], [-0.0342795726663], [493.0],
                  [426.0]], index=expected_index,
            columns=['metrics'])
        self._expected[1] = pd.DataFrame(
            data=[[0.0469136099053], [0.0377867675413], [1.57136939051], [1.2415354093], [-0.0429676392916], [479.0],
                  [431.0]], index=expected_index,
            columns=['metrics'])
        self._expected[2] = pd.DataFrame(
            data=[[0.053849451349], [0.0372297858191], [1.75578580001], [1.44640776637], [-0.0252256227179],
                  [473.0],
                  [395.0]], index=expected_index,
            columns=['metrics'])
        self._expected[3] = pd.DataFrame(
            data=[[0.0423011391782], [0.0379338431333], [1.29162493847], [1.11512927993], [-0.0377172],
                  [417.0],
                  [387.0]], index=expected_index,
            columns=['metrics'])

    def test_gx_rps_strat(self):
        for i in range(len(self._data)):
            data = self._data[i]
            perf = strategyRunner(userStrategy=GXRPS,
                                  strategyParameters=(
                                  data['window_min_max'], data['window_ma'], data['vol_diff_slice']),
                                  symbolList=data['universe'],
                                  dataSource=DataSource.CSV,
                                  csvDir=data['csv_dir'],
                                  saveFile=False,
                                  portfolioType=PortfolioType.CashManageable,
                                  plot=False
                                  )['perf_metric']
            assert_frame_equal(perf, self._expected[i])
