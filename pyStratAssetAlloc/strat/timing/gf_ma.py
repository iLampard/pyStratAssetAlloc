# -*- coding: utf-8 -*-

# ref: 张超，利用均线间距变化提前预判趋势：交易性择时策略研究之九，广发证券，2017

import datetime as dt
from AlgoTrading.Strategy.Strategy import Strategy
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from PyFin.api import MA
from PyFin.api import DIFF
from enum import IntEnum
from enum import unique
from decouple import config


@unique
class Cross(IntEnum):
    None_x = 0
    Gold_x = 1
    Dead_x = 2


class GFMovingAverageCrossStrategy(Strategy):
    def __init__(self, ma_short, ma_long):
        distance = MA(ma_short, 'close') - MA(ma_long, 'close')
        indicator = DIFF(distance)
        self.diff_distance = indicator
        self.distance = distance
        self.prev_distance = distance.shift(1)
        self.cross = Cross.None_x

    def handle_data(self):
        for sec in self.universe:
            if self.cross == Cross.Dead_x:
                if self.secPos[sec] <= 0 <= self.diff_distance[sec]:  # 上一个为死叉且间距缩小(间距为负，故diff_distance为正)： 看多
                    self.order_to_pct(sec, 1, 1)
                elif self.diff_distance[sec] <= 0 <= self.secPos[sec]:  # 上一个为死叉且间距扩大(间距为负，故diff_distance为负)： 看空
                    self.order_to_pct(sec, -1, 1)
            elif self.cross == Cross.Gold_x:
                if self.secPos[sec] <= 0 <= self.diff_distance[sec]:  # 上一个为金叉且间距扩大(间距为正，故diff_distance为正)： 看多
                    self.order_to_pct(sec, 1, 1)
                elif self.diff_distance[sec] <= 0 <= self.secPos[sec]:  # 上一个为金叉且间距缩小(间距为正，故diff_distance为负)： 看空
                    self.order_to_pct(sec, -1, 1)

            # update cross status
            if self.prev_distance[sec] < 0 < self.distance[sec]:
                self.cross = Cross.Gold_x
            elif self.prev_distance[sec] > 0 > self.distance[sec]:
                self.cross = Cross.Dead_x


def run_example():
    universe = ['000300.zicn']
    start_date = dt.datetime(2005, 1, 1)
    end_date = dt.datetime(2017, 1, 1)
    ma_short = config('GF_MA_SHORT', default=20, cast=int)
    ma_long = config('GF_MA_LONG', default=90, cast=int)

    strategyRunner(userStrategy=GFMovingAverageCrossStrategy,
                   strategyParameters=(ma_short, ma_long),
                   symbolList=universe,
                   startDate=start_date,
                   endDate=end_date,
                   benchmark='000300.zicn',
                   dataSource=DataSource.WIND,
                   logLevel='info',
                   saveFile=True,
                   portfolioType=PortfolioType.CashManageable,
                   plot=True,
                   freq='D')


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
