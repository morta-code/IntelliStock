# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 19:04:58 2014

@author: Polcz Péter <ppolcz@gmail.com>
"""

from PyQt4.QtGui import *
import matplotlib as mpl
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import sys
import numpy as np
from threading import Lock

plot_widget_lock = Lock()


def synchronized(lock):
    """Synchronization decorator."""
    def wrap(f):
        def new_function(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return new_function
    return wrap


class PlotWidget(QWidget):
    def __init__(self, parent=None, rows=1, cols=1):
        QWidget.__init__(self, parent)

        # declare further attributes
        self.ts_t = self.ts_x = self.rows = self.cols = self.axes_list = self.axes = None

        self.fig = Figure(
            figsize=(4.0, 4.0),
            dpi = 100,
            facecolor = None,
            edgecolor = None,
            linewidth = 0.0,
            frameon = True,
            subplotpars = None,
            tight_layout = None)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.subplot(0, rows, cols)
        self.setup_ui()

    def setup_ui(self):
        """
        Override me
        """
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    @synchronized(plot_widget_lock)
    def clear(self):
        self.axes.clear()

    @synchronized(plot_widget_lock)
    def erase_line(self, ploth=None, plotnr=None):
        """
        @arg plotnr : int {1, 2, ...}
        @arg ploth - reference to a plot object (i.e. "plot handle")
        @return None if error occurred
        """
        # for k, v in self.axes.__dict__.items():
        #     print(k, v)
        #
        # print(dir(self.axes))
        # for d in dir(self.axes):
        #     print(d, getattr(self.axes, d), sep=" --- ")
        if plotnr is not None and plotnr < len(self.axes.lines):
            return self.axes.lines.pop(plotnr)
        elif ploth and self.axes.lines.count(ploth) > 0:
            self.axes.lines.remove(ploth)
            return True
        elif type(ploth) == list:
            ret = False
            for pl in ploth:
                if self.axes.lines.count(pl) > 0:
                    self.axes.lines.remove(pl)
                    ret = True
                if self.axes.patches.count(pl) > 0:
                    self.axes.patches.remove(pl)
                    ret = True
            return ret

    @synchronized(plot_widget_lock)
    def hide_line(self, ploth=None, plotnr=None, hide=True):
        """
        @arg plotnr : int {1, 2, ...}
        @arg ploth - reference to a plot object (i.e. "plot handle")
        @return None if error occurred
        """
        if plotnr is not None and plotnr < len(self.axes.lines):
            ploth = self.axes.lines[plotnr]
        if ploth:
            if type(ploth) == list:
                for plh in ploth:
                    plh._visible = not hide
            else:
                ploth._visible = not hide
        return ploth

    @synchronized(plot_widget_lock)
    def subplot(self, plotnr=1, rows=None, cols=None):
        """
        @arg plotnr : int {1, 2, ...}
        @return None if error occurred
        """
        # if rows and cols are not None and are greater zero - resplit the figure
        if rows and cols and rows > 0 and cols > 0:
            self.fig.clear()
            self.rows = rows
            self.cols = cols
            self.axes_list = [self.fig.add_subplot(rows, cols, cols * i + j + 1)
                              for i in range(rows)
                              for j in range(cols)]
            self.axes = self.axes_list[plotnr-1]
            return self.axes

        # just switch subplot
        if plotnr < self.rows + self.cols:
            self.axes = self.axes_list[plotnr-1]
            return self.axes

    @synchronized(plot_widget_lock)
    def set_axis_offset(self, value: bool=False):
        axis_formatter = mpl.ticker.ScalarFormatter(useOffset=value)
        self.axes.yaxis.set_major_formatter(axis_formatter)
        self.axes.xaxis.set_major_formatter(axis_formatter)

    @synchronized(plot_widget_lock)
    def set_axes_labels(self, xlabel: str="", ylabel: str=""):
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)

    @synchronized(plot_widget_lock)
    def plot(self, *args, **kargs):
        """
        @arg args - matplotlib-like arguments
        @return refference to the plot objects
        """
        return self.axes.plot(*args, **kargs)

    @synchronized(plot_widget_lock)
    def fill(self, *args, **kargs):
        """
        @arg args - matplotlib-like arguments
        @return refference to the plot objects
        """
        return self.axes.fill(*args, **kargs)

    @synchronized(plot_widget_lock)
    def legend(self, *args, **kwargs):
        self.axes.legend(prop={'size': 6}, *args, **kwargs)

    @synchronized(plot_widget_lock)
    def draw(self):
        """
        just like a `flush() method`
        """
        FigureCanvas.draw(self.canvas)

    # @synchronized(plot_widget_lock)
    # def get_axes(self):
    #     """BE AWARE! This is not thread-safe!"""
    #     return self.axes



#    @pyqtSlot()
#    def redraw(self):
#        self.draw()


# -------------------------------------------------------------------------------------------------------------------- #
# -- TEST ------------------------------------------------------------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #


def main_test():
    # Qt keretrendszer elinditasa (enelkul nem lehet widgeteket letrehozni)
    app = QApplication(sys.argv)

    w = PlotWidget()
    w.show()

    t = np.linspace(0, 2*np.pi, 1000)
    t2 = np.linspace(0.4, 1.5, 20)
    x = np.sin(t * 13)

    if not w.subplot(2, rows=2, cols=1):
        print("Assertion error: subplot - resplit figure")

    # test plot()
    p = w.plot(t, x)[0]
    w.plot(t, x*2)
    w.plot(t, x*2, 'g')
    q = w.plot(t2, np.ones_like(t2) * 0.5)[0]
    w.draw()
    w.clear()

    # test erase_line()
    if not w.erase_line(ploth=p):
        print("Assertion error: erase_line by ploth")
    if not w.erase_line(plotnr=0):
        print("Assertion error: erase_line by plotnr")
    w.draw()            
    
    # test hide_line()
    if not w.hide_line(ploth=q):
        print("Assertion error: erase_line by ploth")
    if not w.hide_line(plotnr=1, hide=False):
        print("Assertion error: erase_line by plotnr, set visible")
    w.plot(t, 0.5*x+0.5, 'b')
    w.draw()
    
    if not w.subplot(1):
        print("Assertion error: subplot - switch subplot")        
        
    w.plot(t, x)
    w.draw()

    d = p.__dict__
    for (k, v) in d.items():
        print(k)
    print(p.__dict__)

    print("---------------------")

    for (k, v) in w.axes.__dict__.items():
        print(k)
    print(w.axes.lines)

    w.clear()

    # Qt keretrendszer futtatasa (main loop)
    app.exec_()


if __name__ == "__main__":
    main_test()