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

def get_trades(begin, end):
    """Returns the trades between dates begin and end."""
        
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


# -------- time conversions ---------- #

def date2year(d: datetime):
    beg = datetime.strptime('20000101000000', format)
    return d.year + (d.timetuple().tm_yday + (d - beg).seconds / 86400) / (365 + int(d.year % 4 == 0) + 1)

def strdate2year(d: str):
    d = datetime.strptime(d, sql_date_format)
    return date2year(d)

def strdate2date(d: str):
    return datetime.strptime(d, sql_date_format)

def year2date(d: float):
    pass

def get_trades_PCZ_DEMO(begin: float, end: float):
    """"""
