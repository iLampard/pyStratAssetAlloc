# -*- coding: utf-8 -*-

import datetime as dt
from AlgoTrading.Strategy.Strategy import Strategy
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from decouple import config
from pyStratAssetAlloc.enum import AssetWeight


# TODO use moving correl matrix as signal

class RISKPARITY(Strategy):
    def __init__(self, window, weight=AssetWeight.RISK_PARITY):
        self._window = window
        self._weight = weight

    def handle_data(self):
        pass
