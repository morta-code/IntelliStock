# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 00:18:49 2014

@author: Polcz Péter <ppolcz@gmail.com>
"""

import sys
import numpy as np

from PyQt4.QtGui import QVBoxLayout, QMessageBox, QApplication
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from intellistock.ui.plotwidget import PlotWidget


class NavigatorPlotWidget(PlotWidget):
    def __init__(self, parent=None, cols=1, rows=1):
        """"""
        PlotWidget.__init__(self, parent, cols, rows)
        self.mpl_toolbar = None
        
    def setup_ui(self):
        # Bind the 'pick' event for clicking on one of the bars
        self.canvas.mpl_connect('pick_event', self.on_pick)
        
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.mpl_toolbar)
        self.setLayout(layout)

    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coordinates:\n %s" % box_points
        
        QMessageBox.information(self, "Click!", msg)

    def on_draw(self):
        self.canvas.draw()

# -------------------------------------------------------------------------------------------------------------------- #
# -- TEST ------------------------------------------------------------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #


def main_test():
    # Qt keretrendszer elinditasa (enelkul nem lehet widgeteket letrehozni)
    app = QApplication(sys.argv)

    w = NavigatorPlotWidget()
    w.show()

    t = np.linspace(0, 2*np.pi, 1000)
    t2 = np.linspace(0.4, 1.5, 20)
    x = np.sin(t * 13)

    if not w.subplot(2, rows=2, cols=2):
        print("Assertion error: subplot - resplit figure")

    # test plot()
    w.clear()
    p = w.plot(t, x)[0]
    w.plot(t, x*2)
    w.plot(t, x*2, 'g')
    q = w.plot(t2, np.ones_like(t2) * 0.5)[0]
    w.draw()

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

    w.subplot(3)
    t = np.linspace(0, 10, 1000)
    x = np.sin(t) + np.cos(t * 10) * 0.5 + np.cos(t * 10 + 0.2) * 0.5 + np.cos(t * 11 + 0.2) * 0.5 + np.random.rand(x.shape[0])
    w.plot(t, x)

    # Qt keretrendszer futtatasa (main loop)
    app.exec_()

if __name__ == "__main__":
    main_test()