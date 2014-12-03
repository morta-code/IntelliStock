# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 19:04:58 2014

@author: Polcz Péter <ppolcz@gmail.com>
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

class PlotWidget(FigureCanvas):
    def __init__(self, rows = 1, cols = 1):
        self.fig = Figure(
            figsize = (4.0, 4.0),
            dpi = 100,
            facecolor = None,
            edgecolor = None,
            linewidth = 0.0,
            frameon = True,
            subplotpars = None,
            tight_layout = None)

        FigureCanvas.__init__(self, self.fig)

        self.subplot(0, rows, cols)

    def clear(self):
        self.axis.clear()
        
    def eraseLine(self, plotH = None, plotNr = None):
        """
            @arg plotNr - int
            @arg plotH - refference to a plot object (i.e. "plot handle")
            @return None if error occured
        """
        if plotNr is not None and plotNr < len(self.axis.lines):
            return self.axis.lines.pop(plotNr)
        elif plotH and self.axis.lines.count(plotH) > 0:
            self.axis.lines.remove(plotH)
            return True
                
    def hideLine(self, plotH = None, plotNr = None, hide = True):
        """
            @arg plotNr - int
            @arg plotH - refference to a plot object (i.e. "plot handle")
            @return None if error occured
        """
        if plotNr is not None and plotNr < len(self.axis.lines):
            plotH = self.axis.lines[plotNr]
        if plotH:
            plotH._visible = not hide
        return plotH
                
        
    def subplot(self, axisNr = 0, rows = None, cols = None):
        """
            @arg axisNr - index of subplot
            @return None if error occured
        """
        # if rows and cols are not None and are greater zero
        if rows and cols and rows > 0 and cols > 0:
            self.rows = rows;
            self.cols = cols;
            self.axes = [];
            self.axes = [self.fig.add_subplot(rows, cols, rows * i + j) 
                for i in range(rows) 
                for j in range(cols)]
            self.axis = self.axes[axisNr]
            return self.axis

        if (axisNr < self.rows + self.cols):
            print(axisNr)
            print(self.axes)
            print([self.axis])
            self.axis = self.axes[axisNr]
            print([self.axis])
            return self.axis
        
    def plot(self, *args, **kargs):
        """
            @arg index - int
            @arg args - matplotlib-like
            @return refference to the plot objects 
        """
        return self.axis.plot(*args, **kargs)
    
    def draw(self):
        """
            just like a `flush() method`
        """
        FigureCanvas.draw(self)
        
        
#    @pyqtSlot()
#    def redraw(self):
#        self.draw()


def main():
    # Qt keretrendszer elinditasa (enelkul nem lehet widgeteket letrehozni)
    app = QApplication(sys.argv)

    w = PlotWidget()
    w.show()

    t = np.linspace(0, 2*np.pi, 1000)
    t2 = np.linspace(0.4, 1.5, 20)
    x = np.sin(t * 13)

    if not w.subplot(1,2,1):
        print("Assertion error: subplot - resplit figure")

    # test plot()
    w.clear()    
    p = w.plot(t, x)[0]
    w.plot(t, x*2)
    w.plot(t, x*2, 'g')
    q = w.plot(t2,np.ones_like(t2) * 0.5)[0]
    w.draw()
    
    # test eraseLine()
    if not w.eraseLine(plotH = p):
        print("Assertion error: eraseLine by plotH")
    if not w.eraseLine(plotNr = 0):
        print("Assertion error: eraseLine by plotNr")
    w.draw()            
    
    # test hideLine()
    if not w.hideLine(plotH = q):
        print("Assertion error: eraseLine by plotH")
    if not w.hideLine(plotNr = 0, hide = False):
        print("Assertion error: eraseLine by plotNr, set visible")
    w.draw()
    
    if not w.subplot(0):
        print("Assertion error: subplot - switch subplot")        
        
    w.plot(t,x)    
    w.draw()
        
    
#    d = p[0].__dict__
#    for (k,v) in d.iteritems():
#        print(k)
#
#    print("---------------------")
#
#    for (k,v) in w.axis.__dict__.iteritems():
#        print(k)
#    print(w.axis.lines)

    # Qt keretrendszer futtatasa (main loop)
    app.exec_()


if __name__ == "__main__":
    main()