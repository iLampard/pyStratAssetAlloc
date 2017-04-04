# -*- coding: utf-8 -*-

from pyStratAssetAlloc.technical import LLT
from pyStratAssetAlloc.utils import get_sec_price
from pyStratAssetAlloc.enum import DataSource
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = get_sec_price('2016-01-01', '2017-01-01', ['000300.SH'], DataSource.WIND)  # 获取2016的HS300收盘数据
    ts = LLT(alpha=2.0/61.0, dependency='000300.SH')  # 定义llt模块
    res = ts.transform(data)  # 获取HS300的llt序列
    plt.xlabel("date")
    plt.ylabel("index")
    plt.plot(res, label="LLT")
    plt.plot(data['000300.SH'], label="HS300")
    plt.legend()
    plt.show()
