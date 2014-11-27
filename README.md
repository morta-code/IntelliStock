IntelliStock
============

A Python software to view and predict „Budapesti Értéktőzsde” stocks.

## Requirements
- PyQt4
- Matplotlib with Qt4 backend
- Numpy

# Reference

## MainWindow (class)
Gui component of IntelliStock. Must be created and managed by the "main" component of the program.
### construction
    window = MainWindow(initial_stocks, get_stock_datas_cb)

Where

- *initial_stock* is a dict with all stocks and last values.
- *get_stock_datas_cb* is a callback for request datas for a specified stock and date. `get_stock_datas_cb(stock, 
date)`
 
### methods
    update_stocks(updated_stock: dict) -> None
Call it when new trades arrived. *updated_stocks* is a names (str) keyed prize values.
    
    stock_values(stock: str, IDE VALAMI ADATSZERKEZET)
Call it to show a time serie for the given stock.
