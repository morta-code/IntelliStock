# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 14:23:08 2014

@author: wondercsabo
"""

from datetime import datetime

"""Entry point for access all data related methods."""

sql_date_format = '%Y%m%d%H%M%S'

DB_PATH = "IntelliStock.sqlite"
conn = None

stocks = set()


def get_stocks():
    """Returns the stocks currently stored in the database."""
    return stocks


def get_stocks_with_last_close():
    """Returns the last close for all stocks."""
    cur = conn.execute("SELECT StockData.paper_name, close FROM (SELECT MAX(id) as max_id, paper_name FROM StockData GROUP BY paper_name) AS MAX_IDS INNER JOIN StockData ON MAX_IDS.paper_name = StockData.paper_name AND StockData.id = MAX_IDS.max_id")
    
    return cur.fetchall()


def start_polling():
    """Starts the polling of the BSE page for new data."""


def stop_polling():
    """Stops polling of the BSE page."""


def update_stocks():
    """This will call the mediator to update the gui with new data."""


def get_trades(begin: int, end: int, paper_name: str=None):
    """
    example: select paper_name, datetime, close from StockData where paper_name = 'OTP' and datetime between 20100104100000 and 20100104110000 group by datetime;
    """
    cols = " paper_name, datetime, close from StockData "
    filter_by_paper_name = " paper_name = '" + paper_name + "' "
    filter_by_date = " datetime between " + str(begin) + " and " + str(end) + " "
    group_by_date = " group by datetime "
    if paper_name:
        sql = "select" + cols + "where" + filter_by_paper_name + "and" + filter_by_date + group_by_date
    else:
        sql = "select" + cols + "where" + filter_by_date + group_by_date
    cur = conn.execute(sql)
    return cur.fetchall()


def get_close(date: int, paper_name: str):
    cur = conn.execute("SELECT close FROM (SELECT MAX(id) as max_id, paper_name FROM StockData WHERE datetime <= ? GROUP BY paper_name) AS MAX_IDS INNER JOIN StockData ON MAX_IDS.paper_name = StockData.paper_name AND StockData.id = MAX_IDS.max_id AND StockData.paper_name = ?",
                       (date, paper_name))

    return cur.fetchone()[0]


# -------- time conversions ---------- #


def date2year(d: datetime):
    beg = datetime.strptime('20000101000000', sql_date_format)
    return d.year + (d.timetuple().tm_yday + (d - beg).seconds / 86400) / (365 + int(d.year % 4 == 0) + 1)


def int2year(d: int):
    d = datetime(int(d // 1e10), int(d // 1e8 % 100), int(d // 1e6 % 100), int(d // 1e4 % 100), int(d // 1e2 % 100), int(d % 100))
    return date2year(d)


def datetime_to_dbdatetime(dt: datetime):
    datestr = str(dt.year) + "%02d" % dt.month + "%02d" % dt.day
    tt = dt.timetuple()
    timestr = "%02d" % tt.tm_hour + "%02d" % tt.tm_min +  "%02d" % tt.tm_sec
    return int(datestr) * 1000000 + int(timestr)
