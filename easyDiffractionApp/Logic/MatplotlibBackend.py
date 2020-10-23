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

        # Set data
        self.style = Style()
        self.data = {}
        self.current_canvas = None

    def updateWithCanvas(self, canvas=None, data=None, style={}):
        """ initialize with the canvas for the figure
        """

        if data is None:
            data = {}

        if not (self.current_canvas and self.context) and not (canvas and self.context):
            raise RuntimeError
        if canvas:
            self.current_canvas = self.context.findChild(QtCore.QObject, canvas)

        if not data:
            data['x'] = np.linspace(0, 2 * np.pi, 100)
            data['y'] = np.sin(data['x'])

        self.data = data
        self.redraw(style=style)

    def redraw(self, style={}):

        self.style.set_style(style)

        self.figure = self.current_canvas.figure
        self.figure.clf()
        self.toolbar = NavigationToolbar2QtQuick(canvas=self.current_canvas)

        # make a small plot
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True)

        self.axes.plot(self.data['x'], self.data['y'])
        self.axes.set_xlabel('Two Theta (degrees)')
        self.axes.set_ylabel('Intensity (arb)')
        self.current_canvas.draw_idle()

        # connect for displaying the coordinates
        self.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

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

    # # Set style
    # def setStyle(self):
    #
    #     matplotlib.style.use('fivethirtyeight')
    #
    #     # matplotlib.rcParams["figure.figsize"] = (10, 6)
    #     matplotlib.rcParams['lines.linewidth'] = 1
    #
    #     SIZE = 7
    #     matplotlib.rcParams['axes.labelsize'] = SIZE
    #     matplotlib.rcParams['ytick.labelsize'] = SIZE
    #     matplotlib.rcParfacecolorams['xtick.labelsize'] = SIZE
    #     matplotlib.rcParams["font.size"] = SIZE
    #
    #     COLOR = '1'
    #     matplotlib.rcParams['text.color'] = COLOR
    #     matplotlib.rcParams['axes.labelcolor'] = COLOR
    #     matplotlib.rcParams['xtick.color'] = COLOR
    #     matplotlib.rcParams['ytick.color'] = COLOR
    #
    #     matplotlib.rcParams['grid.linewidth'] = 0.1
    #     matplotlib.rcParams['grid.color'] = "0.2"
    #     matplotlib.rcParams['lines.color'] = "0.5"
    #     matplotlib.rcParams['axes.edgecolor'] = "0.2"
    #     matplotlib.rcParams['axes.linewidth'] = 0.5
    #
    #     matplotlib.rcParams['figure.facecolor'] = "#101622"
    #     matplotlib.rcParams['axes.facecolor'] = "#101622"
    #     matplotlib.rcParams["savefig.dpi"] = 120
    #     dpi = matplotlib.rcParams["savefig.dpi"]
    #     width = 700
    #     height = 1200
    #     # matplotlib.rcParams['figure.figsize'] = height / dpi, width / dpi
    #     matplotlib.rcParams["savefig.facecolor"] = "#101622"
    #     matplotlib.rcParams["savefig.edgecolor"] = "#101622"
    #
    #     matplotlib.rcParams['legend.fontsize'] = SIZE
    #     matplotlib.rcParams['legend.title_fontsize'] = SIZE + 1
    #     matplotlib.rcParams['legend.labelspacing'] = 0.25
    #     matplotlib.rcParams['image.cmap'] = 'tab10'

    # Update style
    @QtCore.Slot(bool, 'QVariant')
    def updateStyle(self, is_dark_theme, rc_params):
        rc_params = rc_params.toVariant() # PySide2.QtQml.QJSValue -> dict
        print("is_dark_theme", is_dark_theme)
        print("rc_params", rc_params)
        #self.figure.clear()
        #self.figure.canvas.draw_idle()
        #self.figure.canvas.draw()
        self.redraw()


class Style:
    def __init__(self, dark_mode=False):
        self.dark_mode = dark_mode
        self.current_style = {}
        self._base_style()

    def set_style(self, style_override: dict = {}):
        if self.dark_mode:
            self._dark_style()
        self.current_style.update(style_override)
        matplotlib.rcParams.update(self.current_style)

    def _base_style(self) -> dict:
        # matplotlib.style.use('seaborn')

        bg_color = 'white'
        axis_color = 'white'
        text_color = 'black'

        style = {
            'figure.facecolor': bg_color,
            'axes.facecolor':   axis_color,
            'axes.labelcolor':  text_color,
            'xtick.color':      text_color,
            'ytick.color':      text_color,
            'lines.linewidth':  2,
            'axes.prop_cycle':  matplotlib.rcsetup.cycler(color=['#ff7f50']),
            'axes.edgecolor':   '#ddd',
            'grid.color':       '#ddd',
            'axes.xmargin':     0.
        }
        self.current_style = style

    def _dark_style(self):
        bg_color = '#4C4C4C'
        text_color = '#F4F4F4'
        axis_color = 'f0f0f0'

        self.current_style['figure.facecolor'] = bg_color
        self.current_style['axes.facecolor'] = axis_color
        self.current_style['axes.labelcolor'] = text_color
        self.current_style['xtick.color'] = text_color
        self.current_style['ytick.color'] = text_color
