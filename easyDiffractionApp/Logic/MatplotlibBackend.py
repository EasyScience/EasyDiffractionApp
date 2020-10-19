__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

from easyCore import np
from easyCore.Utils.classUtils import singleton

import matplotlib
from matplotlib_backend_qtquick.qt_compat import QtGui, QtQml, QtCore
from matplotlib_backend_qtquick.backend_qtquick import (
    NavigationToolbar2QtQuick)


@singleton
class DisplayBridge(QtCore.QObject):
    """ A bridge class to interact with the plot in python
    """
    coordinatesChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # The figure and toolbar
        self.figure = None
        self.toolbar = None

        # Add context
        self.context = None

        # this is used to display the coordinates of the mouse in the window
        self._coordinates = ""

    def updateWithCanvas(self, canvas, data=None):
        """ initialize with the canvas for the figure
        """
        if data is None:
            data = {}

        if not (canvas and self.context):
            raise RuntimeError

        canvas = self.context.findChild(QtCore.QObject, canvas)

        self.figure = canvas.figure
        self.figure.clf()
        self.toolbar = NavigationToolbar2QtQuick(canvas=canvas)

        # make a small plot
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True)

        if not data:
            data['x'] = np.linspace(0, 2 * np.pi, 100)
            data['y'] = np.sin(data['x'])
        self.axes.plot(data['x'], data['y'])
        canvas.draw_idle()

        # connect for displaying the coordinates
        self.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

        # set plot style
        self.setStyle()

    # define the coordinates property
    # (I have had problems using the @QtCore.Property directy in the past)
    def getCoordinates(self):
        return self._coordinates

    def setCoordinates(self, coordinates):
        self._coordinates = coordinates
        self.coordinatesChanged.emit(self._coordinates)

    coordinates = QtCore.Property(str, getCoordinates, setCoordinates,
                                  notify=coordinatesChanged)

    # The toolbar commands
    @QtCore.Slot()
    def pan(self, *args):
        """Activate the pan tool."""
        self.toolbar.pan(*args)

    @QtCore.Slot()
    def zoom(self, *args):
        """activate zoom tool."""
        self.toolbar.zoom(*args)

    @QtCore.Slot()
    def home(self, *args):
        self.toolbar.home(*args)

    @QtCore.Slot()
    def back(self, *args):
        self.toolbar.back(*args)

    @QtCore.Slot()
    def forward(self, *args):
        self.toolbar.forward(*args)

    def on_motion(self, event):
        """
        Update the coordinates on the display
        """
        if event.inaxes == self.axes:
            self.coordinates = f"({event.xdata:.2f}, {event.ydata:.2f})"

    # Set style
    def setStyle(self):
        matplotlib.rcParams['lines.linewidth'] = 2
        matplotlib.rcParams['axes.prop_cycle'] = matplotlib.rcsetup.cycler(color=['#ff7f50'])
        matplotlib.rcParams['axes.edgecolor'] = '#ddd'
        matplotlib.rcParams['grid.color'] = '#ddd'
        matplotlib.rcParams['axes.xmargin'] = 0.

    # Update style
    @QtCore.Slot(bool)
    def updateStyle(self, is_dark_theme):
        print("is_dark_theme", is_dark_theme)
        #self.figure.clear()
        #self.figure.canvas.draw_idle()
        #self.figure.canvas.draw()
