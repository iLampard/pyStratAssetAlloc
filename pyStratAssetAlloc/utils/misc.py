# -*- coding: utf-8 -*-

import pandas as pd
from pyStratAssetAlloc.enum import DataSource
from pyStratAssetAlloc.enum import DfReturnType
from pyStratAssetAlloc.enum import FreqType
from pyStratAssetAlloc.utils.data_provider import TSMarketDataHandler
from pyStratAssetAlloc.utils.data_provider import WindMarketDataHandler


def get_sec_price(start_date, end_date, sec_ids, data_source, freq=FreqType.EOD, field=['close'],
                  return_type=DfReturnType.DateIndexAndSecIDCol, csv_path=None):
    """
    :param start_date: datetime, start date of query date
    :param end_date: datetime, end date of query date
    :param sec_ids: list of str, sec ids
    :param data_source: enum, source of data
    :param freq: FreqType
    :param field: price type
    :param return_type: DfReturnType
    :param csv_path: str, path of csv file if data_source = csv
    :return: pd.DataFrame
    """
    if data_source == DataSource.WIND:
        price_data = WindMarketDataHandler.get_sec_price_on_date(start_date=start_date,
                                                                 end_date=end_date,
                                                                 sec_ids=sec_ids,
                                                                 freq=freq,
                                                                 field=field,
                                                                 return_type=return_type)
    elif data_source == DataSource.TUSHARE:
        price_data = TSMarketDataHandler.get_sec_price_on_date(start_date=start_date,
                                                               end_date=end_date,
                                                               sec_ids=sec_ids,
                                                               freq=freq,
                                                               field=field,
                                                               return_type=return_type)
    elif data_source == DataSource.CSV:
        price_data = pd.read_csv(csv_path, index_col=0)
        price_data.index = pd.to_datetime(price_data.index)
    else:
        raise NotImplementedError

    return price_data