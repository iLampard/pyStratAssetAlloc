# -*- coding: utf-8 -*-

import pandas as pd
from PyFin.api import nthWeekDay
from PyFin.api import advanceDateByCalendar
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


def find_in_interval(element, interval_list):
    """
    :param element: float
    :param interval_list: list of interval class type
    :return: the index of the interval that contains the element
    """
    check_interval = [element in interval for interval in interval_list]
    return check_interval.index(True)


def get_continuous_future_contract(universe, current_date, del_rule, contract_prefix_len=2):
    """
    :param universe: dict, key = maturity month, value = contract id
    :param current_date: datetime, current datetime
    :param del_rule: dict, termination rule of fut contract
    :param contract_prefix_len: int, optional, length of the prefix of contract ids
    :return: the contract id to use, given current date
    """

    year = current_date.year
    month = current_date.month
    del_day = nthWeekDay(nth=del_rule['nth'],
                         dayOfWeek=del_rule['day_of_week'],
                         month=month,
                         year=year)
    del_date = advanceDateByCalendar(holidayCenter='China.SSE',
                                     referenceDate=del_day,
                                     period='-1b')
    contract_month = month if current_date < del_date else month + 1
    contract_year = year - 2000
    if contract_month > 12:
        contract_month -= 12
        contract_year += 1

    suffix = universe[0].split('.')[1]
    prefix = universe[0].split('.')[0][:contract_prefix_len]
    contract_id = '%s%02d%02d.%s' % (prefix, contract_year, contract_month, suffix)
    return contract_id
