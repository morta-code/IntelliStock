# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 00:18:49 2014

@author: Polcz Péter <ppolcz@gmail.com>
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

from .plotwidget import PlotWidget

class NavigatorPlotWidget(PlotWidget):
    def __init__(self, parent = None, cols = 1, rows = 1):
        PlotWidget.__init__(self, parent, cols, rows)
        
    def setupUi(self):            
        # Bind the 'pick' event for clicking on one of the bars
        self.canvas.mpl_connect('pick_event', self.pcz_onPick)
        
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        self.setLayout(vbox)

    def pcz_onPick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points
        
        QMessageBox.information(self, "Click!", msg)

    def pcz_onDraw(self):
        self.canvas.draw()

def main_test():
    # Qt keretrendszer elinditasa (enelkul nem lehet widgeteket letrehozni)
    app = QApplication(sys.argv)
    
    w = NavigatorPlotWidget()
    w.show()

    t = np.linspace(0, 2*np.pi, 1000)
    t2 = np.linspace(0.4, 1.5, 20)
    x = np.sin(t * 13)

    if not w.subplot(2, rows = 2, cols = 2):
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
    if not w.hideLine(plotNr = 1, hide = False):
        print("Assertion error: eraseLine by plotNr, set visible")
    w.plot(t, 0.5*x+0.5, 'b')
    w.draw()
    
    if not w.subplot(1):
        print("Assertion error: subplot - switch subplot")        
        
    w.plot(t,x)    
    w.draw()

    w.subplot(3)
    t = np.linspace(0, 10, 1000)
    x = np.sin(t) + np.cos(t * 10) * 0.5 + np.cos(t * 10 + 0.2) * 0.5 + np.cos(t * 11 + 0.2) * 0.5 + np.random.rand(x.shape[0])
    w.plot(t,x)

    # Qt keretrendszer futtatasa (main loop)
    app.exec_()

if __name__ == "__main__":
    main_test()