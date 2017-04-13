# -*- coding: utf-8 -*-


import unittest
import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from pyStratAssetAlloc.strat.alloc import RISKPARITY
from pyStratAssetAlloc.enum import AssetWeight


class Test_Risk_Parity(unittest.TestCase):
    def setUp(self):
        universe = ['510300.xshg', '510500.xshg', '511010.xshg', '518880.xshg']
        csv_dir = 'data'
        assets1 = {
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
        assets2 = {
            '510300.xshg': {
                'target_weight': 0.0,
                'default_weight': 0.055},

            '510500.xshg': {
                'target_weight': 0.0,
                'default_weight': 0.095},
            '511010.xshg': {
                'target_weight': 0.0,
                'default_weight': 0.65},
            '518880.xshg': {
                'target_weight': 0.0,
                'default_weight': 0.2}
        }
        assets3 = {
            '510300.xshg': {
                'target_weight': 0.0,
                'default_weight': 0.045},

            '510500.xshg': {
                'target_weight': 0.0,
                'default_weight': 0.105},
            '511010.xshg': {
                'target_weight': 0.0,
                'default_weight': 0.7},
            '518880.xshg': {
                'target_weight': 0.0,
                'default_weight': 0.15}
        }
        data1 = {'universe': universe,
                 'csv_dir': csv_dir,
                 'assets': assets1,
                 'window': 50,
                 'tiaocang_freq': 10,
                 'weight_type': AssetWeight.RISK_PARITY}
        data2 = {'universe': universe,
                 'csv_dir': csv_dir,
                 'assets': assets2,
                 'window': 150,
                 'tiaocang_freq': 20,
                 'weight_type': AssetWeight.EQUAL}
        data3 = {'universe': universe,
                 'csv_dir': csv_dir,
                 'assets': assets3,
                 'window': 250,
                 'tiaocang_freq': 30,
                 'weight_type': AssetWeight.RISK_PARITY}
        self._data = [data1, data2, data3]

        expected_index = [u'annual_return', u'annual_volatiltiy', u'sortino_ratio',
                          u'sharp_ratio', u'max_draw_down', u'winning_days', u'lossing_days']
        expected_1 = pd.DataFrame(
            data=[[0.0622926980642], [0.0445555368383], [2.00824435682], [1.39809106756], [-0.0465932884823], [482],
                  [388]], index=expected_index,
            columns=['metrics'])
        expected_2 = pd.DataFrame(
            data=[[0.106198576591], [0.153107582476], [0.812291526721], [0.693620622008], [-0.265551032791], [474.0],
                  [396.0]], index=expected_index,
            columns=['metrics'])
        expected_3 = pd.DataFrame(
            data=[[0.064287113497], [0.0461884888264], [1.86254817286], [1.39184275412], [-0.0557657297607], [490],
                  [380]], index=expected_index,
            columns=['metrics'])

        self._expected = [expected_1,expected_2,expected_3]

    def Test_Risk_Parity_strat(self):
        expected1 = np.array(
            [[0.0622926980642], [0.0445555368383], [2.00824435682], [1.39809106756], [-0.0465932884823], [482], [388]])
        expected2 = np.array(
            [[0.106198576591], [0.153107582476], [0.812291526721], [0.693620622008], [-0.265551032791], [474.0],
             [396.0]])
        expected3 = np.array(
            [[0.064287113497], [0.0461884888264], [1.86254817286], [1.39184275412], [-0.0557657297607], [490], [380]])
        expected = [expected1, expected2, expected3]
        for i in range(len(self._data)):
            data = self._data[i]
            perf = strategyRunner(userStrategy=RISKPARITY,
                                     strategyParameters=(data['window'], data['assets'], data['tiaocang_freq'], data['weight_type']),
                                     symbolList=data['universe'],
                                     dataSource=DataSource.CSV,
                                     csvDir=data['csv_dir'],
                                     saveFile=False,
                                     portfolioType=PortfolioType.CashManageable,
                                     plot=False
                                     )['perf_metric']
            assert_frame_equal(perf, self._expected[i])
