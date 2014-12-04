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

from plotwidget import PlotWidget

class NavigatorPlotWidget(PlotWidget):
    def __init__(self, parent = None, cols = 1, rows = 1):
        PlotWidget.__init__(self, parent, cols, rows)
        
    def setupUi(self):            
        # Bind the 'pick' event for clicking on one of the bars
        #
        self.canvas.mpl_connect('pick_event', self.pcz_onPick)
        
        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        
#        # Other GUI controls
#        # 
#        self.textbox = QLineEdit()
#        self.textbox.setMinimumWidth(200)
#        self.connect(self.textbox, SIGNAL('editingFinished()'), self.pcz_onDraw)
#        
#        self.draw_button = QPushButton("&Draw")
#        self.connect(self.draw_button, SIGNAL('clicked()'), self.pcz_onDraw)
#        
#        self.grid_cb = QCheckBox("Show &Grid")
#        self.grid_cb.setChecked(False)
#        self.connect(self.grid_cb, SIGNAL('stateChanged(int)'), self.pcz_onDraw)
#        
#        slider_label = QLabel('Bar width (%):')
#        self.slider = QSlider(Qt.Horizontal)
#        self.slider.setRange(1, 100)
#        self.slider.setValue(20)
#        self.slider.setTracking(True)
#        self.slider.setTickPosition(QSlider.TicksBothSides)
#        self.connect(self.slider, SIGNAL('valueChanged(int)'), self.pcz_onDraw)
        
        #
        # Layout with box sizers
        # 
#        hbox = QHBoxLayout()
#        
#        for w in [self.textbox, self.draw_button, self.grid_cb, slider_label, self.slider]:
#            hbox.addWidget(w)
#            hbox.setAlignment(w, Qt.AlignVCenter)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
#        vbox.addLayout(hbox)
        
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
#        """ Redraws the figure
#        """
#        # python3 vs python2
#        try:
#            s = str(self.textbox.text())
#        except:
#            s = unicode(self.textbox.text())
#        
#        self.data = map(int, s.split())
#
#        # python3 vs python2
#        if ispy3(): self.data = list(self.data)
#        
#        x = range(len(self.data))
#
#        # clear the ax_bars and redraw the plot anew
#        #
#        self.ax_bars.clear()        
#        self.ax_bars.grid(self.grid_cb.isChecked())
#        self.ax_bars.bar(
#            left = x, 
#            height = self.data, 
#            width = self.slider.value() / 100.0, 
#            align = 'center', 
#            alpha = 0.44,
#            picker = 0)
#
#        n = 1000
#        t0 = 0
#        t1 = 3*3.1415
#        f = lambda x : math.sin(x * self.slider.value())
#        t = map(lambda k: t0 + (k * (t1-t0)) / n, range(n))
#        if (ispy3()): t = list(t)
#        x = map(f, t)
#        if (ispy3()): 
#            x = list(x)
#
#        self.ax_plot.clear()
#        self.ax_plot.plot(t,x)

        self.canvas.draw()

def main_test():
    # Qt keretrendszer elinditasa (enelkul nem lehet widgeteket letrehozni)
    app = QApplication(sys.argv)
    
    w = NavigatorPlotWidget()
    w.show()

    t = np.linspace(0, 2*np.pi, 1000)
    t2 = np.linspace(0.4, 1.5, 20)
    x = np.sin(t * 13)

    if not w.subplot(2, rows = 2, cols = 1):
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

    # Qt keretrendszer futtatasa (main loop)
    app.exec_()

if __name__ == "__main__":
    main_test()