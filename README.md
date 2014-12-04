IntelliStock
============

A Python software to view and predict Budapest Stock Exchange stocks.<br>
This is a collaborative assignment project of PPCU's [Scientific Python course](http://users.itk.ppke.hu/~oroszgy/?scipy-2014) in 2014/2015 autumn.

## Requirements
- PyQt4
- Matplotlib with Qt4 backend
- Numpy

# Reference

## MainWindow (class)
Gui component of IntelliStock. It is created and managed by the application class.
### construction
    window = MainWindow(application)
- *application* is the application of the currently running instance. It must have the following methods:
`new_plotter`, `kill_plotter` and `start_simulation`


### initialization
    window.initialize(initial_stocks)
- *initial_stock* is a dict with all stocks and last values.
 
### methods
    update_stocks(updated_stock: dict) -> None
Call it when new trades arrived. *updated_stocks* is a names (str) keyed price values.
