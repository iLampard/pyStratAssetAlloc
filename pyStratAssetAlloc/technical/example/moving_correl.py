# -*- coding: utf-8 -*-

from pyStratAssetAlloc.technical import MOVING_CORREL_MAT
from pyStratAssetAlloc.utils import get_sec_price
from pyStratAssetAlloc.enum import DataSource

if __name__ == '__main__':
    data = get_sec_price('2016-01-01', '2017-01-01', ['000300.SH', '000905.SH'], DataSource.WIND)
    correl = MOVING_CORREL_MAT(window=20, dependency='close')
    for i in range(len(data)):
        temp = {'close': {'close': [data['000300.SH'][i], data['000905.SH'][i]]}}
        correl.push(temp)
        print correl.value
