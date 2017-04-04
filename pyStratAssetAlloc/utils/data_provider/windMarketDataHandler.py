# -*- coding: utf-8 -*-
# 从wind服务器读取数据的初版，希望完善后能合并入Algo-Trading package中
# http://image.dajiangzhang.com/djz/download/20140928/WindMatlab.pdf
# http://image.dajiangzhang.com/djz/download/20140928/WindAPIFAQ.pdf

import pandas as pd
from PyFin.Utilities import pyFinAssert
from empyrical import cum_returns
from pyStratAssetAlloc.enum import FreqType
from pyStratAssetAlloc.enum.df_return import DfReturnType

try:
    from WindPy import w
except ImportError:
    pass


class WindMarketDataHandler(object):
    def __init__(self):
        pass

    @classmethod
    def get_sec_price_on_date(cls, start_date, end_date, sec_ids, freq=FreqType.EOD, field=['close'],
                              return_type=DfReturnType.DateIndexAndSecIDCol):
        """
        :param start_date: str, start date of the query period
        :param end_date: str, end date of the query period
        :param sec_ids: list of str, sec IDs
        :param freq: FreqType
        :param field: str, filed of data to be queried
        :param return_type: dfReturnType
        :return: pd.DataFrame, index = date, col = sec ID
        """
        if not w.isconnected():
            w.start()

        pyFinAssert(freq == FreqType.EOD, ValueError, "for the moment the function only accepts freq type = EOD")
        start_date = str(start_date) if not isinstance(start_date, basestring) else start_date
        end_date = str(end_date) if not isinstance(end_date, basestring) else end_date

        raw_data = w.wsd(sec_ids, field, start_date, end_date, 'PriceAdj=F', 'Fill=Previous')
        ret = format_raw_data(raw_data, sec_ids, freq, field, return_type)

        return ret

    @classmethod
    def get_sec_return_on_date(cls, start_date, end_date, sec_ids, freq=FreqType.EOD, field=['close'],
                               return_type=DfReturnType.DateIndexAndSecIDCol, is_cumul=False):
        """
        :param start_date: str, start date of the query period
        :param end_date: str, end date of the query period
        :param sec_ids: list of str, sec IDs
        :param field: str, filed of data to be queried
        :param freq: FreqType
        :param return_type
        :param is_cumul: return is cumul or not
        :return: pd.DataFrame, index = date, col = sec ID
        """
        if not w.isconnected():
            w.start()

        ret = WindMarketDataHandler.get_sec_price_on_date(start_date, end_date, sec_ids, freq, field, return_type)
        ret = ret.pct_change()
        if is_cumul:
            ret = ret.fillna(0)
            ret = cum_returns(ret, starting_value=1.0)
        else:
            ret = ret.dropna()
        return ret


def format_raw_data(raw_data, sec_ids, freq, fields, return_type):
    ret = pd.DataFrame()
    if len(raw_data.Data) > 0:
        if return_type == DfReturnType.DateIndexAndSecIDCol:
            pyFinAssert(len(fields) == 1, ValueError,
                        "length of query fields must be 1 under DateIndexAndSecIDCol return type")
            output = {'tradeDate': raw_data.Times}
            for secID in sec_ids:
                output[secID] = raw_data.Data[sec_ids.index(secID)]
            ret = pd.DataFrame(output)
            if freq == FreqType.EOD:
                ret['tradeDate'] = ret['tradeDate'].apply(lambda x: x.strftime('%Y-%m-%d'))
                ret['tradeDate'] = pd.to_datetime(ret['tradeDate'])
            ret = ret.set_index('tradeDate')
        else:
            raise NotImplementedError

    return ret


