# -*- coding: utf-8 -*-
# ref: http://tushare.org/trading.html#id3

import pandas as pd
import tushare as ts
from PyFin.Utilities import pyFinAssert
from empyrical import cum_returns
from pyStratAssetAlloc.enum import DfReturnType
from pyStratAssetAlloc.enum import FreqType


class TSMarketDataHandler(object):
    def __init__(self, sec_ids, start_date, end_date, freq=None, fields=None,
                 return_type=DfReturnType.DateIndexAndSecIDCol):
        self._secID = sec_ids
        self._startDate = start_date
        self._endDate = end_date
        self._freq = FreqType.EOD if freq is None else freq
        self._fields = ['open', 'high', 'low', 'close', 'volume'] if fields is None else fields
        self._returnType = return_type

    @classmethod
    def get_sec_price_on_date(cls, start_date, end_date, sec_ids, freq=FreqType.EOD, field=['close'],
                              return_type=DfReturnType.DateIndexAndSecIDCol):
        """
        :param start_date: str, start date of the query period
        :param end_date: str, end date of the query period
        :param sec_ids: list of str, sec IDs
        :param freq: FreqType
        :param return_type: DfReturnType
        :param field: str, filed of data to be queried
        :return: pd.DataFrame, index = date, col = sec ID
        """

        pyFinAssert(freq == FreqType.EOD, ValueError, "for the moment the function only accepts freq type = EOD")
        start_date = str(start_date) if not isinstance(start_date, basestring) else start_date
        end_date = str(end_date) if not isinstance(end_date, basestring) else end_date

        ret = pd.DataFrame()
        for s in sec_ids:
            raw_data = ts.get_h_data(s, start_date, end_date)
            if return_type == DfReturnType.DateIndexAndSecIDCol:
                ret = pd.concat([ret, raw_data[field]], axis=1)
            else:
                raise NotImplementedError

        if return_type == DfReturnType.DateIndexAndSecIDCol:
            ret.columns = sec_ids
            ret.index.name = 'tradeDate'
            ret.sort_index(ascending=True, inplace=True)

        return ret

    @classmethod
    def get_sec_return_on_date(cls, start_date, end_date, sec_ids, freq=FreqType.EOD, field=['close'],
                               return_type=DfReturnType.DateIndexAndSecIDCol, is_cumul=False):
        """
        :param start_date: str, start date of the query period
        :param end_date: str, end date of the query period
        :param sec_ids: list of str, sec IDs
        :param field: str, filed of data to be queried
        :param return_type
        :param freq: FreqType
        :param is_cumul: return is cumul or not
        :return: pd.DataFrame, index = date, col = sec ID
        """
        ret = TSMarketDataHandler.get_sec_price_on_date(start_date, end_date, sec_ids, freq, field, return_type)
        ret = ret.pct_change()
        if is_cumul:
            ret = ret.fillna(0)
            ret = cum_returns(ret, starting_value=1.0)
        else:
            ret = ret.dropna()
        return ret


if __name__ == "__main__":
    print TSMarketDataHandler.get_sec_price_on_date(start_date='2010-10-10',
                                                    end_date='2010-11-10',
                                                    sec_ids=['002022', '000001'])
    print TSMarketDataHandler.get_sec_return_on_date(start_date='2010-10-10',
                                                     end_date='2010-11-10',
                                                     sec_ids=['002022', '000001'])
