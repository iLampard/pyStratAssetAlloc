# -*- coding: utf-8 -*-

# ref: 魏刚，股指期货程序化交易研究之七：Dual Thrust日间策略，华泰证券，2012

import datetime as dt
from collections import defaultdict
from AlgoTrading.Strategy.Strategy import Strategy
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Enums import DataSource
from AlgoTrading.api import PortfolioType
from PyFin.api import OPEN
from PyFin.api import HIGH
from PyFin.api import LOW
from PyFin.api import CLOSE
from decouple import config
from pyStratAssetAlloc.utils import get_continuous_future_contract


class DualThrust(Strategy):
    def __init__(self, window_up, multi_up, window_down, multi_down, **kwargs):
        self._window_up = int(window_up)
        self._multi_up = multi_up
        self._window_down = int(window_down)
        self._multi_down = multi_down
        self._open = OPEN()
        self._close = CLOSE()
        self._high = HIGH()
        self._low = LOW()
        self._price_daily = defaultdict(lambda: defaultdict(list))
        self._thrust = defaultdict(lambda: defaultdict(list))
        self._day_count = 0
        self._update_date = None
        self._save_thrust = kwargs.get('save_thrust', True)
        self._del_rule = kwargs.get('del_rule', {'nth': 3, 'day_of_week': 6})
        self._main_contract = None

    def handle_data(self):
        self._update_thrust()
        current_date = self.current_datetime
        fut_id = get_continuous_future_contract(self.universe, current_date, self._del_rule)
        if fut_id != self._main_contract and self.secPos[self._main_contract] != 0:
            self.order_to(self._main_contract, 1, 0)

        if len(self._thrust[fut_id]['thrust_up']) == 0 or len(self._thrust[fut_id]['thrust_down']) == 0:
            return
        signal = 1 if self._close[fut_id] > self._thrust[fut_id]['thrust_up'][-1] else -1 \
            if self._close[fut_id] < self._thrust[fut_id]['thrust_down'][-1] else 0
        if signal > 0 >= self.secPos[fut_id]:
            self.order_to(fut_id, 1, 1)
        elif signal < 0 <= self.secPos[fut_id]:
            self.order_to(fut_id, -1, 1)

    def _update_thrust(self):
        if self._update_date != self.current_date:  # 开始新的一天
            self._append_price()
            self._update_date = self.current_date
            self._calc_thrust()

        elif self._update_date == self.current_date:  # 如果还在同一天
            self._update_price_daily_on_same_day()

    def _append_price(self):
        for sec in self.universe:
            self._price_daily[sec]['open'].append(self._open[sec])
            self._price_daily[sec]['high'].append(self._high[sec])
            self._price_daily[sec]['low'].append(self._low[sec])
            self._price_daily[sec]['close'].append(self._close[sec])

    def _update_price_daily_on_same_day(self):
        # 如果还在同一天
        for sec in self.universe:
            if len(self._price_daily[sec]['open']) == 0:  # 特殊情况：整个策略读取的第一根bar
                self._append_price()
                return
            else:
                if self._high[sec] > self._price_daily[sec]['high'][-1]:
                    self._price_daily[sec]['high'][-1] = self._high[sec]
                if self._low[sec] < self._price_daily[sec]['low'][-1]:
                    self._price_daily[sec]['low'][-1] = self._low[sec]
                self._price_daily[sec]['close'][-1] = self._close[sec]

    def _calc_range(self, sec, window):
        # N日high的最高价
        hh = max(self._price_daily[sec]['high'][-window:-1])
        # N日close的最高价
        hc = max(self._price_daily[sec]['close'][-window:-1])
        # N日close的最低价
        lc = min(self._price_daily[sec]['close'][-window:-1])
        # N日low的最低价
        ll = min(self._price_daily[sec]['low'][-window:-1])

        calc_range = max(hh - lc, hc - ll)
        return calc_range

    def _calc_thrust(self):
        for sec in self.universe:
            if len(self._price_daily[sec]['high']) >= self._window_up + 1:
                thrust_up = self._open[sec] + self._multi_up * self._calc_range(sec, self._window_up)
                thrust_down = self._open[sec] - self._multi_down * self._calc_range(sec, self._window_down)
                self._thrust[sec]['thrust_up'].append(thrust_up)
                self._thrust[sec]['thrust_down'].append(thrust_down)
                if self._save_thrust:
                    self.keep('thrust_up_' + sec, thrust_up)
                    self.keep('thrust_down_' + sec, thrust_down)


def run_example():
    # universe = ['if15%02d.ccfx' % i for i in range(1, 13)]
    universe = ['if15%02d.ccfx' % i for i in range(10, 13)] + ['if16%02d.ccfx' % i for i in range(1, 4)]
    start_date = dt.datetime(2015, 11, 10)
    end_date = dt.datetime(2016, 2, 1)

    window_up = config('DT_WINDOW_UP', cast=float)
    multi_up = config('DT_MULTI_UP', cast=float)
    window_down = config('DT_WINDOW_DOWN', cast=float)
    multi_down = config('DT_MULTI_DOWN', cast=float)

    strategyRunner(userStrategy=DualThrust,
                   strategyParameters=(window_up, multi_up, window_down, multi_down),
                   symbolList=universe,
                   startDate=start_date,
                   endDate=end_date,
                   benchmark='000300.zicn',
                   dataSource=DataSource.WIND,
                   logLevel='info',
                   saveFile=True,
                   plot=True,
                   freq='min5')


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
