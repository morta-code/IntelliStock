# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 14:23:08 2014

@author: wondercsabo
"""

import datetime

"""Entry point for access all data related methods."""

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

def strdate_to_day(d: str, beginning: str = None):
    class state:
        format = '%Y%m%d%H%M%S'
        beg = datetime.strptime('20000101000000', format)
    if beginning:
        state.beg = datetime.strptime(beginning, state.format)
    dt = datetime.strptime(d, state.format) - state.beg
    return dt.days + dt.seconds / 86400

def get_trades_PCZ_DEMO(begin: tuple, end: tuple):
    """"""
