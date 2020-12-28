__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import os

import matplotlib
from matplotlib_backend_qtquick.qt_compat import QtGui, QtQml, QtCore
from matplotlib_backend_qtquick.backend_qtquick import NavigationToolbar2QtQuick

from easyCore.Utils.classUtils import singleton
from easyAppLogic.Utils.Utils import generalizePath


@singleton
class DisplayBridge(QtCore.QObject):
    """
    A bridge class to interact with the plot in python
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.context = None
        self.display_adapters = {}
        self.font_path = ""
        self.style_params = {}

    # The toolbar commands

    @QtCore.Slot('QVariant')
    def pan(self, canvas):
        display_adapter = self.displayAdapter(canvas)
        if display_adapter is not None:
            display_adapter.toolbar.pan()

    @QtCore.Slot('QVariant')
    def zoom(self, canvas):
        display_adapter = self.displayAdapter(canvas)
        if display_adapter is not None:
            display_adapter.toolbar.zoom()

    @QtCore.Slot('QVariant')
    def home(self, canvas):
        display_adapter = self.displayAdapter(canvas)
        if display_adapter is not None:
            display_adapter.toolbar.home()

    @QtCore.Slot('QVariant')
    def back(self, canvas):
        display_adapter = self.displayAdapter(canvas)
        if display_adapter is not None:
            display_adapter.toolbar.back()

    @QtCore.Slot('QVariant')
    def forward(self, canvas):
        display_adapter = self.displayAdapter(canvas)
        if display_adapter is not None:
            display_adapter.toolbar.forward()

    # Misc

    @QtCore.Slot('QVariant')
    def setContext(self, context):
        self.context = context

    @QtCore.Slot(str)
    def setFont(self, font_path):
        self.font_path = font_path

    @QtCore.Slot('QVariant')
    def updateStyle(self, params):
        params = params.toVariant()  # PySide2.QtQml.QJSValue -> dict
        self.style_params.update(params)
        for display_adapter in self.display_adapters.values():
            display_adapter.updateStyle(self.style_params)
            display_adapter.initPlot()
            display_adapter.updateStyleAfterPlot()
            display_adapter.redrawCanvas()

    @QtCore.Slot('QVariant')
    def updateMargins(self, canvas):
        display_adapter = self.displayAdapter(canvas)
        if display_adapter is not None:
            display_adapter.updateMargins()
            display_adapter.redrawCanvas()

    @QtCore.Slot(bool, 'QVariant')
    def showLegend(self, show_legend, canvas):
        display_adapter = self.displayAdapter(canvas)
        if display_adapter is not None:
            display_adapter.showLegend(show_legend)
            display_adapter.redrawCanvas()

    def displayAdapter(self, canvas):
        canvas_name = hash(canvas)
        display_adapter = self.display_adapters.get(canvas_name, None)
        return display_adapter

    def clearDispalyAdapters(self):
        self.display_adapters.clear()

    def updateData(self, canvas, dataset):
        canvas_name = hash(canvas)

        # init and add display adapter
        if canvas_name not in self.display_adapters.keys():
            display_adapter = DisplayAdapter(canvas, dataset, parent=self)
            display_adapter.setFont(self.font_path)
            display_adapter.updateStyle(self.style_params)
            display_adapter.initPlot()
            display_adapter.updateStyleAfterPlot()
            display_adapter.updateMargins()
            self.display_adapters[canvas_name] = display_adapter

        # update data of existing adapter
        else:
            display_adapter = self.display_adapters[canvas_name]
            display_adapter.updateData(dataset)
            display_adapter.autoScale()

        # redraw
        display_adapter.redrawCanvas()


class DisplayAdapter(QtCore.QObject):
    """
    An adapter for every figure canvas created in QML
    """

    def __init__(self, canvas, dataset, parent=None):
        super().__init__(parent)

        self.canvas = canvas
        self.dataset = dataset

        self.toolbar = None

        self.figure = None
        self.axes = None
        self.lines = []

    def initPlot(self):
        self.toolbar = NavigationToolbar2QtQuick(canvas=self.canvas)

        self.figure = self.canvas.figure
        self.figure.clf()

        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel(self.dataset[-1].x_label)
        self.axes.set_ylabel(self.dataset[-1].y_label)

        self.lines.clear()
        for data in self.dataset:
            line, = self.axes.plot(data.x, data.y, label=data.name)
            self.lines.append(line)

        self.axes.legend(loc='upper right')

    def showLegend(self, show_legend):
        self.axes.get_legend().set_visible(show_legend)

    def updateMargins(self):
        # set margins (!!! should be calculated based on the font size from QML)
        bbox = self.figure.bbox
        width = bbox.width
        height = bbox.height
        left_margin = 90. / width
        right_margin = 15. / width
        top_margin = 10. / height
        bottom_margin = 55. / height
        self.figure.subplots_adjust(left=left_margin, right=1-right_margin, top=1-top_margin, bottom=bottom_margin)
        self.figure.tight_layout()

    def updateData(self, dataset):
        self.dataset = dataset
        for line, data in zip(self.lines, self.dataset):
            line.set_data(data.x, data.y)

    def autoScale(self):
        self.axes.relim()
        self.axes.autoscale_view()

    def redrawCanvas(self):
        #self.canvas.draw_idle()
        self.canvas.draw()

    def setFont(self, font_source):
        # https://stackoverflow.com/questions/35668219/how-to-set-up-a-custom-font-with-custom-path-to-matplotlib-global-font/43647344
        # https://stackoverflow.com/questions/16574898/how-to-load-ttf-file-in-matplotlib-using-mpl-rcparams

        font_path = generalizePath(font_source)  # url -> path
        font_dirs = [os.path.dirname(font_path)]
        font_files = matplotlib.font_manager.findSystemFonts(fontpaths=font_dirs)
        font_list = matplotlib.font_manager.createFontList(font_files)
        matplotlib.font_manager.fontManager.ttflist.extend(font_list)
        # print([f.name for f in matplotlib.font_manager.fontManager.ttflist])

        prop = matplotlib.font_manager.FontProperties(fname=font_path)
        matplotlib.rcParams['font.family'] = prop.get_name()

    def updateStyle(self, style_params):
        matplotlib.rcParams.update(style_params)

    def updateStyleAfterPlot(self):
        # Already automatically applied based on rcParams
        if False:
            # background
            self.axes.set_facecolor(matplotlib.rcParams['axes.facecolor'])
            # edges
            self.axes.spines['bottom'].set_color(matplotlib.rcParams['axes.edgecolor'])
            self.axes.spines['top'].set_color(matplotlib.rcParams['axes.edgecolor'])
            self.axes.spines['left'].set_color(matplotlib.rcParams['axes.edgecolor'])
            self.axes.spines['right'].set_color(matplotlib.rcParams['axes.edgecolor'])
            # axes labels
            self.axes.xaxis.label.set_color(matplotlib.rcParams['axes.labelcolor'])
            self.axes.yaxis.label.set_color(matplotlib.rcParams['axes.labelcolor'])
            # ticks and tick labels
            for e in self.axes.get_xticklabels():
                e.set_color(matplotlib.rcParams['xtick.color'])
            for e in self.axes.get_yticklabels():
                e.set_color(matplotlib.rcParams['ytick.color'])
            # grid lines
            for e in self.axes.get_xgridlines():
                e.set_color(matplotlib.rcParams['grid.color'])
            for e in self.axes.get_ygridlines():
                e.set_color(matplotlib.rcParams['grid.color'])

        # Manually applied based on rcParams
        self.figure.patch.set_color(matplotlib.rcParams['figure.facecolor'])
        self.axes.tick_params(width=0)
        self.axes.legend().get_frame().set_edgecolor(matplotlib.rcParams['grid.color'])  # doesn't work :(
        for e in self.axes.legend().get_texts():
            e.set_color(matplotlib.rcParams['axes.labelcolor'])
