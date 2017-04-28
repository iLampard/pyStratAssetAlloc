# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from pyStratAssetAlloc.enum import DataSource
from pyStratAssetAlloc.technical import LLT
from pyStratAssetAlloc.utils import get_sec_price
from pyStratAssetAlloc.utils import find_in_interval

try:
    from interval import interval
    from interval import inf
except ImportError:
    pass

_dict_stage = {0: 'down',
               1: 'volatile',
               2: 'up'}


def plot_llt_simple(start_date, end_date, sec_id, data_source=DataSource.WIND):
    data = get_sec_price(start_date, end_date, sec_id, data_source)  # 获取2016的HS300收盘数据
    ts = LLT(alpha=2.0 / 61.0, dependency=sec_id[0])  # 定义llt模块
    res = ts.transform(data)  # 获取HS300的llt序列
    plt.xlabel('date')
    plt.ylabel('index')
    plt.plot(res, label='LLT')
    plt.plot(data[sec_id[0]], label=sec_id[0])
    plt.legend()
    plt.show()


def plot_llt_by_state(start_date, sec_id, **kwargs):
    end_date = kwargs.get('end_date', None)
    data_source = kwargs.get('data_source', DataSource.WIND)
    llt_alpha = kwargs.get('llt_alpha', 2.0 / 61.0)
    llt_quantile = kwargs.get('llt_quantile', [0.4, 0.6])

    if end_date is None:
        end_date = str(date.today())
    data = get_sec_price(start_date, end_date, sec_id, data_source)

    ts = LLT(alpha=llt_alpha, dependency=sec_id[0])
    res = ts.transform(data, name='LLT')
    res['LLT_slope'] = res['LLT'].pct_change()
    res.dropna(inplace=True)
    llt_break = [np.percentile(res['LLT_slope'], int(quantile * 100)) for quantile in llt_quantile]

    res['type'] = res['LLT_slope'].apply(find_in_interval, interval_list=[interval([-inf, llt_break[0]]),
                                                                          interval([llt_break[0], llt_break[1]]),
                                                                          interval([llt_break[1], inf])])

    plt.figure(figsize=(14, 6))
    for i in range(len(llt_break) + 1):
        plt.plot(res.loc[res['type'] == i, 'LLT'], 'o',
                 label='stage {0}-LLT'.format(_dict_stage[i]), lw=3)

    plt.xlabel('date')
    plt.ylabel('index')
    plt.plot(data[sec_id[0]], label=sec_id[0])
    plt.legend(loc='best')
    plt.title('{0} and LLT: LLT is painted with diff color based on slope by quantile {1} and {2}'.format(sec_id[0],
                                                                                                          llt_quantile[
                                                                                                              0],
                                                                                                          llt_quantile[
                                                                                                              1]))
    plt.show()


if __name__ == '__main__':
    plot_llt_by_state(start_date='2016-01-01',
                      sec_id=['000300.SH'])
