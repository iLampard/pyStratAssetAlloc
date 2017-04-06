# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False
from pyStratAssetAlloc.enum import DataSource
from pyStratAssetAlloc.technical import RPS
from pyStratAssetAlloc.utils import get_sec_price

if __name__ == '__main__':
    data = get_sec_price('2013-01-01', '2017-01-01', ['000300.SH'], DataSource.WIND)  # 获取2016的HS300收盘数据
    ts = RPS(250, 9, '000300.SH')  # 定义rps模块
    res = ts.transform(data)  # 获取HS300的rps序列
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    p1,= ax1.plot(res,label='RPS')
    ax1.set_ylabel(u'RPS指数值')
    ax1.tick_params(axis='y', colors=p1.get_color())
    ax1.legend(['RPS'],loc=2)
    ax2 = ax1.twinx()  # this is the important function
    p2,= ax2.plot(res.index,data['000300.SH'][1:],'r',label='HS300')
    ax2.set_ylabel(u'市场指数值')
    ax2.tick_params(axis='y', colors=p2.get_color())
    ax2.legend(['HS300'],loc=3)
    plt.show()
