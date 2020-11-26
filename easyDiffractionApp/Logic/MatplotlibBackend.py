__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import os
from typing import Union, List

import matplotlib

from easyCore import np
from easyCore.Utils.classUtils import singleton

from easyDiffractionApp.Logic.DataStore import DataStore, DataSet1D
from easyAppLogic.Utils.Utils import generalizePath

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
        # Add context
        self.context = None
        # Set data
        self.canvas_data = {}

    def updateWithCanvas(self, canvas=None, dataset=None):
        canvas_ = self.context.findChild(QtCore.QObject, canvas)
        if canvas not in self.canvas_data.keys():
            self.canvas_data[canvas] = DisplayAdapter(canvas_, dataset, parent=self)
        else:
            self.canvas_data[canvas].current_canvas_data = dataset
        self.redraw()

    def redraw(self, items: List['DisplayAdapter'] = None):
        if items is None:
            items = [self.canvas_data[key] for key in self.canvas_data.keys()]
        if not isinstance(items, list):
            items = [items]
        for item in items:
            item.redraw()

    # Update style
    @QtCore.Slot(bool, 'QVariant', str)
    def updateStyle(self, is_dark_theme, rc_params, canvas):
        rc_params = rc_params.toVariant()  # PySide2.QtQml.QJSValue -> dict
        _canvas: DisplayAdapter = self.canvas_data.get(canvas, None)
        if _canvas is not None:
            _canvas.updateStyle(is_dark_theme, rc_params)

    @QtCore.Slot(str, str)
    def updateFont(self, font_path, canvas):
        _canvas: DisplayAdapter = self.canvas_data.get(canvas, None)
        if _canvas is not None:
            _canvas.updateFont(font_path)

    @QtCore.Slot(bool, str)
    def showLegend(self, show_legend, canvas):
        _canvas: DisplayAdapter = self.canvas_data.get(canvas, None)
        if _canvas is not None:
            _canvas.showLegend(show_legend)

    # The toolbar commands
    @QtCore.Slot(str)
    def pan(self, canvas, *args):
        """Activate the pan tool."""
        _canvas: DisplayAdapter = self.canvas_data.get(canvas, None)
        if _canvas is not None:
            _canvas.toolbar.pan(*args)

    @QtCore.Slot(str)
    def zoom(self, canvas, *args):
        """activate zoom tool."""
        _canvas: DisplayAdapter = self.canvas_data.get(canvas, None)
        if _canvas is not None:
            _canvas.toolbar.zoom(*args)

    @QtCore.Slot(str)
    def home(self, canvas, *args):
        _canvas: DisplayAdapter = self.canvas_data.get(canvas, None)
        if _canvas is not None:
            _canvas.toolbar.home(*args)

    @QtCore.Slot(str)
    def back(self, canvas, *args):
        _canvas: DisplayAdapter = self.canvas_data.get(canvas, None)
        if _canvas is not None:
            _canvas.toolbar.back(*args)

    @QtCore.Slot(str)
    def forward(self, canvas, *args):
        _canvas: DisplayAdapter = self.canvas_data.get(canvas, None)
        if _canvas is not None:
            _canvas.toolbar.forward(*args)


class DisplayAdapter(QtCore.QObject):
    """ A bridge class to interact with the plot in python
    """
    coordinatesChanged = QtCore.Signal(str)

    def __init__(self, canvas, dataset, parent=None):
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

        self.show_legend = True

        self.current_canvas = canvas
        self.current_canvas_data = dataset

    def redraw(self):

        dataset = self.current_canvas_data

        if not isinstance(dataset, list):
            dataset = [dataset]

        self.style.set_style()

        if self.current_canvas is None:
            return

        self.figure = self.current_canvas.figure
        self.figure.patch.set_color(self.style.current_style['figure.facecolor'])
        self.figure.clf()
        self.toolbar = NavigationToolbar2QtQuick(canvas=self.current_canvas)

        # make a small plot
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True)
        self.axes.tick_params(width=0)

        for data in dataset:
            self.axes.plot(data.x, data.y, label=data.name)
        if self.show_legend:
            self.axes.legend(loc="upper right")
        self.axes.set_xlabel(dataset[0].x_label)
        self.axes.set_ylabel(dataset[0].y_label)
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

    def zoom(self, *args):
        """activate zoom tool."""
        self.toolbar.zoom(*args)

    def home(self, *args):
        self.toolbar.home(*args)

    def back(self, *args):
        self.toolbar.back(*args)

    def forward(self, *args):
        self.toolbar.forward(*args)

    def on_motion(self, event):
        """
        Update the coordinates on the display
        """
        if event.inaxes == self.axes:
            self.coordinates = f"({event.xdata:.2f}, {event.ydata:.2f})"

    # Update style
    def updateStyle(self, is_dark_theme, rc_params):
        self.style.style_override = rc_params
        self.style.dark_mode = is_dark_theme
        self.redraw()

    def updateFont(self, font_path):
        font_path = generalizePath(font_path)
        self.style.set_font(font_path)
        self.redraw()

    def showLegend(self, show_legend):
        self.data.show_legend = show_legend
        self.redraw()


class Style:
    def __init__(self, dark_mode=False):
        self.dark_mode = dark_mode
        self.current_style = {}
        self.style_override = {}
        self._base_style()

    def set_font(self, font_path):
        # https://stackoverflow.com/questions/35668219/how-to-set-up-a-custom-font-with-custom-path-to-matplotlib-global-font/43647344
        # https://stackoverflow.com/questions/16574898/how-to-load-ttf-file-in-matplotlib-using-mpl-rcparams

        font_dirs = [os.path.dirname(font_path)]
        font_files = matplotlib.font_manager.findSystemFonts(fontpaths=font_dirs)
        font_list = matplotlib.font_manager.createFontList(font_files)
        matplotlib.font_manager.fontManager.ttflist.extend(font_list)
        # print([f.name for f in matplotlib.font_manager.fontManager.ttflist])

        prop = matplotlib.font_manager.FontProperties(fname=font_path)
        matplotlib.rcParams['font.family'] = prop.get_name()

    def set_style(self):
        self._base_style()
        if self.dark_mode:
            self._dark_style()
        self.current_style.update(self.style_override)
        matplotlib.rcParams.update(self.current_style)

    def _base_style(self):
        # matplotlib.style.use('seaborn')

        # self.set_font()

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
            'axes.labelpad':    12,
            'axes.prop_cycle':  matplotlib.rcsetup.cycler(color=['#00a3e3', '#ff7f50', '#6b8e23']),
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
