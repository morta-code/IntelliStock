IntelliStock
============

A Python software to view and predict Budapest Stock Exchange stocks.

## Requirements
- PyQt4
- Matplotlib with Qt4 backend
- Numpy

# Reference

## MainWindow (class)
Gui component of IntelliStock. Must be created and managed by the "main" component of the program.
### construction
    window = MainWindow(initial_stocks, get_stock_datas_cb)

- *initial_stock* is a dict with all stocks and last values.
- *get_stock_datas_cb* is a callback for request datas for a specified stock and date. `get_stock_datas_cb(stock, 
date)`
 
### methods
    update_stocks(updated_stock: dict) -> None
Call it when new trades arrived. *updated_stocks* is a names (str) keyed price values.
    
    stock_values(stock: str, datas: list)
Call it to show a time serie for the given stock. *name* is the name of stock, *datas* is a list of the following 
tuples: *(date: datetime, price: int, amount: int)*

### using
    app = QApplication(sys.argv)
    window = MainWindow(initial_stocks, get_stock_datas_cb)
    window.show()
    app.exec()
