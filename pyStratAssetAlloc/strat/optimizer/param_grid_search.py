# -*- coding: utf-8 -*-

import numpy as np
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.api import PortfolioType
import pandas as pd




def run_param_grid_search(strat, universe, start_date, end_date, para_range, para_name, **kwargs):
    universe = universe
    start_date = start_date
    end_date = end_date
    benchmark = kwargs.get('benchmark', universe[0])
    logLevel = kwargs.get('logLevel', 'critical')
    portfolioType = kwargs.get('portfolioType', PortfolioType.CashManageable)
    freq = kwargs.get('freq', 'D')
    record = pd.DataFrame()
    for params in para_range:
        result = strategyRunner(userStrategy=strat,
                                strategyParameters=params,
                                symbolList=universe,
                                startDate=start_date,
                                endDate=end_date,
                                benchmark=benchmark,
                                logLevel=logLevel,
                                portfolioType=portfolioType,
                                freq=freq,
                                plot=False,
                                saveFile=False)['perf_metric']

        row = pd.Series(index=para_name, data=np.array(params))
        row_to_append = pd.concat([result['metrics'], row], axis=0)
        record = pd.concat([record, row_to_append], axis=1)
    record = record.T
    record.to_csv('optimizing_result.csv')