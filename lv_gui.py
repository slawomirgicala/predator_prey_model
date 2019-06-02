from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout, QSlider
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from numpy import *
import pylab as p
from PyQt5 import QtCore, QtWidgets, uic

import matplotlib
matplotlib.use('QT5Agg')

import matplotlib.pylab as plt

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class GUI(QWidget):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.a = 1.
        self.b = 0.1
        self.c = 1.5
        self.d = 0.75

        self.interface()

    def dX_dt(self, X, t=0):
        """ Return the growth rate of fox and rabbit populations. """
        return array([ self.a*X[0] -   self.b*X[0]*X[1] ,
		      -self.c*X[1] + self.d*self.b*X[0]*X[1] ])

    def d2X_dt2(self, X, t=0):
        """ Return the Jacobian matrix evaluated in X. """
        return array([[self.a -self.b*X[1],   -self.b*X[0]     ],
                      [self.b*self.d*X[1] ,   -self.c +self.b*self.d*X[0]] ])

    def draw_plot(self):

        X_f0 = array([     0. ,  0.])
        X_f1 = array([ self.c/(self.d*self.b), self.a/self.b])
        all(self.dX_dt(X_f0) == zeros(2) ) and all(self.dX_dt(X_f1) == zeros(2)) # => True
        
        A_f0 = self.d2X_dt2(X_f0) 
        
        A_f1 = self.d2X_dt2(X_f1)                    # >>> array([[ 0.  , -2.  ],
                                                #            [ 0.75,  0.  ]])
        # whose eigenvalues are +/- sqrt(c*a).j:
        lambda1, lambda2 = linalg.eigvals(A_f1) # >>> (1.22474j, -1.22474j)
        # They are imaginary numbers. The fox and rabbit populations are periodic as follows from further
        # analysis. Their period is given by:
        T_f1 = 2*pi/abs(lambda1)                # >>> 5.130199
        
        
        
        from scipy import integrate
        t = linspace(0, 15,  1000)              # time
        X0 = array([10, 5])                     # initials conditions: 10 rabbits and 5 foxes
        X, infodict = integrate.odeint(self.dX_dt, X0, t, full_output=True)
        infodict['message'] 
        
        
        rabbits, foxes = X.T
        self.fig = p.figure()
        p.plot(t, rabbits, 'r-', label='Rabbits')
        p.plot(t, foxes  , 'b-', label='Foxes')
        p.grid()
        p.legend(loc='best')
        p.xlabel('time')
        p.ylabel('population')
        p.title('Evolution of fox and rabbit populations')
        #p.show()




    def interface(self):

        layout = QGridLayout()
        self.label1 = QLabel("a:", self)
        self.s1 = QSlider(Qt.Horizontal)
        self.s1.setMinimum(0)
        self.s1.setMaximum(100)
        self.s1.setValue(100)
        #self.sl.setTickPosition(QSlider.TicksBelow)
        self.s1.setTickInterval(1)
        self.s1.valueChanged.connect(self.handle_s1)
        self.draw_plot()
        self.plotWidget = FigureCanvas(self.fig)

        layout.addWidget(self.label1)
        layout.addWidget(self.s1)
        layout.addWidget(self.plotWidget)
        self.setLayout(layout)

        self.setGeometry(20, 20, 300, 100)
        self.setWindowTitle("Lotki-Volterry model")
        self.show()

    def handle_s1(self):
        a = float(self.s1.value())/100.0
        self.update()

    def update(self):
        #p.close()
        p.clf()
        p.cla()
        #self.fig(clear=True)
        self.draw_plot()
        #self.plotWidget = FigureCanvas(self.fig)
        self.fig.canvas.draw_idle()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = GUI()
    sys.exit(app.exec_())
