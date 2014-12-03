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
    def __init__(self):
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
            
        self.axes = self.fig.add_subplot(111)


def main():
    # Qt keretrendszer elinditasa (enelkul nem lehet widgeteket letrehozni)
    app = QApplication(sys.argv)

    w = PlotWidget()
    w.show()
    
    # Qt keretrendszer futtatasa (main loop)
    app.exec_()


if __name__ == "__main__":
    main()