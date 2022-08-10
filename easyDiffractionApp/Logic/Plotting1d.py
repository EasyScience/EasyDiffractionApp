# SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import numpy as np
import scipy

from PySide6.QtCore import QObject, Qt, QPointF, Signal
from PySide6.QtGui import QImage, QBrush
from PySide6.QtQml import QJSValue
from PySide6.QtCharts import QLineSeries, QScatterSeries


class Plotting1dLogic(QObject):
    dummySignal = Signal()

    # Lib
    currentLibChanged = Signal()

    # Ranges
    experimentPlotRangesObjChanged = Signal()
    analysisPlotRangesObjChanged = Signal()

    # Data containers
    bokehMeasuredDataObjChanged = Signal()
    bokehCalculatedDataObjChanged = Signal()
    bokehDifferenceDataObjChanged = Signal()
    bokehBraggDataObjChanged = Signal()
    bokehBackgroundDataObjChanged = Signal()
    bokehPhasesDataObjChanged = Signal()

    qtchartsMeasuredDataObjChanged = Signal()
    qtchartsCalculatedDataObjChanged = Signal()
    qtchartsDifferenceDataObjChanged = Signal()
    qtchartsBraggDataObjChanged = Signal()
    qtchartsBackgroundDataObjChanged = Signal()

    def __init__(self, parent, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        # Lib
        self._libs = ['bokeh', 'qtcharts']
        self._current_lib = 'bokeh'
        self.currentLibChanged.connect(self.onCurrentLibChanged)

        # Ranges
        self._measured_min_x = 999999
        self._measured_max_x = -999999
        self._measured_min_y = 999999
        self._measured_max_y = -999999

        self._calculated_min_x = 999999
        self._calculated_max_x = -999999
        self._calculated_min_y = 999999
        self._calculated_max_y = -999999

        self._difference_min_y = 0
        self._difference_max_y = 1
        self._difference_median_y = 0.5

        self._y_axis_range_extension = 0.1

        # Data containers
        self._measured_xarray = np.empty(0)
        self._measured_yarray = np.empty(0)
        self._measured_syarray = np.empty(0)
        self._measured_yarray_upper = np.empty(0)
        self._measured_yarray_lower = np.empty(0)

        self._calculated_xarray = np.empty(0)
        self._calculated_yarray = np.empty(0)

        self._difference_yarray = np.empty(0)
        self._difference_yarray_upper = np.empty(0)
        self._difference_yarray_lower = np.empty(0)

        self._bragg_arrays = {}

        self._background_xarray = np.empty(0)
        self._background_yarray = np.empty(0)

        # Ranges for GUI
        self._experiment_plot_ranges_obj = {}
        self._analysis_plot_ranges_obj = {}

        # Data containers for GUI
        self._bokeh_measured_data_obj = {}
        self._bokeh_calculated_data_obj = {}
        self._bokeh_difference_data_obj = {}
        self._bokeh_bragg_data_obj = {}
        self._bokeh_background_data_obj = {}
        self._bokeh_phases_data_obj = {}

        self._qtcharts_measured_data_obj = {}
        self._qtcharts_calculated_data_obj = {}
        self._qtcharts_difference_data_obj = {}
        self._qtcharts_bragg_data_obj = {}
        self._qtcharts_background_data_obj = {}

    def currentLib(self, lib):
        if self._current_lib == lib:
            return
        self._current_lib = lib
        self.currentLibChanged.emit()

    def clearBackendState(self):

        # Ranges
        self._measured_min_x = 999999
        self._measured_max_x = -999999
        self._measured_min_y = 999999
        self._measured_max_y = -999999

        self._calculated_min_x = 999999
        self._calculated_max_x = -999999
        self._calculated_min_y = 999999
        self._calculated_max_y = -999999

        self._difference_min_y = 0
        self._difference_max_y = 1
        self._difference_median_y = 0.5

        self._y_axis_range_extension = 0.1

        # Data containers
        self._measured_xarray = np.empty(0)
        self._measured_yarray = np.empty(0)
        self._measured_syarray = np.empty(0)
        self._measured_yarray_upper = np.empty(0)
        self._measured_yarray_lower = np.empty(0)

        self._calculated_xarray = np.empty(0)
        self._calculated_yarray = np.empty(0)

        self._difference_yarray = np.empty(0)
        self._difference_yarray_upper = np.empty(0)
        self._difference_yarray_lower = np.empty(0)

        self._bragg_arrays = {}

        self._background_xarray = np.empty(0)
        self._background_yarray = np.empty(0)

    def clearFrontendState(self):

        # Ranges for GUI
        self._experiment_plot_ranges_obj = {}
        self._analysis_plot_ranges_obj = {}

        # Data containers for GUI
        self._bokeh_measured_data_obj = {}
        self._bokeh_calculated_data_obj = {}
        self._bokeh_difference_data_obj = {}
        self._bokeh_bragg_data_obj = {}
        self._bokeh_background_data_obj = {}
        self._bokeh_phases_data_obj = {}

        self._qtcharts_measured_data_obj = {}
        self._qtcharts_calculated_data_obj = {}
        self._qtcharts_difference_data_obj = {}
        self._qtcharts_bragg_data_obj = {}
        self._qtcharts_background_data_obj = {}

        # Ranges
        self.experimentPlotRangesObjChanged.emit()
        self.analysisPlotRangesObjChanged.emit()

        # Data containers
        self.bokehMeasuredDataObjChanged.emit()
        self.bokehCalculatedDataObjChanged.emit()
        self.bokehDifferenceDataObjChanged.emit()
        self.bokehBraggDataObjChanged.emit()
        self.bokehBackgroundDataObjChanged.emit()
        self.bokehPhasesDataObjChanged.emit()

        self.qtchartsMeasuredDataObjChanged.emit()
        self.qtchartsCalculatedDataObjChanged.emit()
        self.qtchartsDifferenceDataObjChanged.emit()
        self.qtchartsBraggDataObjChanged.emit()
        self.qtchartsBackgroundDataObjChanged.emit()

    # Public: Python backend

    def setMeasuredData(self, xarray, yarray, syarray=None):
        self._setMeasuredDataArrays(xarray, yarray, syarray)
        self._setMeasuredDataRanges()
        self._setExperimentPlotRanges()
        self._setAnalysisPlotRanges()
        self._setBokehMeasuredDataObj()
        if self.currentLib == 'qtcharts':
            self._setQtChartsMeasuredDataObj()

    def setCalculatedData(self, xarray, yarray):
        self._setCalculatedDataArrays(xarray, yarray)
        self._setCalculatedDataRanges()
        self._setAnalysisPlotRanges()
        self._setBokehCalculatedDataObj()
        self._setBokehPhasesDataObj()
        if self.currentLib == 'qtcharts':
            self._setQtChartsCalculatedDataObj()
        if self._measured_xarray.size:
            self._setDifferenceDataArrays()
            self._setDifferenceDataRanges()
            self._setBokehDifferenceDataObj()
            if self.currentLib == 'qtcharts':
                self._setQtChartsDifferenceDataObj()

    def setBraggData(self, phase_index, xarray, harray, karray, larray):
        self._setBraggDataArrays(phase_index, xarray, harray, karray, larray)
        self._setBokehBraggDataObj(phase_index)
        if self.currentLib == 'qtcharts':
            self._setQtChartsBraggDataObj()

    def setBackgroundData(self, xarray, yarray):
        if not xarray.size:
            return
        interp_func = scipy.interpolate.interp1d(xarray, yarray, fill_value="extrapolate")
        extrapolated_y = interp_func(self._measured_xarray)
        if len(extrapolated_y) == 0:
            return
        self._setBackgroundDataArrays(self._measured_xarray, extrapolated_y)
        self._setBokehBackgroundDataObj()
        self._setBokehPhasesDataObj()
        if self.currentLib == 'qtcharts':
            self._setQtChartsBackgroundDataObj()

    def onCurrentLibChanged(self):
        if self.currentLib == 'qtcharts':
            self._setQtChartsCalculatedDataObj()
            self._setQtChartsBraggDataObj()
            self._setQtChartsBackgroundDataObj()
            if self._measured_xarray.size:
                self._setQtChartsMeasuredDataObj()
                self._setQtChartsDifferenceDataObj()

    def lineSeriesCustomReplace(self, line_series, points):
        if not isinstance(line_series, (QLineSeries, QScatterSeries)):
            return
        if points is None:
            return
        if isinstance(points, QJSValue):
            points = points.toVariant()
        if isinstance(points, list):
            line_series.replace(points)

    def verticalLine(self, size, color):
        width = size
        height = size
        textureImage = QImage(width, height, QImage.Format_ARGB32)
        # Transparent background
        for row in range(height):
            for column in range(width):
                textureImage.setPixelColor(column, row, Qt.transparent)
        # Vertical line
        for row in range(height):
            column = int(width/2)
            textureImage.setPixelColor(column, row, color)
        brush = QBrush()
        brush.setTextureImage(textureImage)
        return brush

    # Private: data array setters

    def _setMeasuredDataArrays(self, xarray, yarray, syarray=None):
        self._measured_xarray = xarray
        self._measured_yarray = yarray
        if syarray is not None:
            self._measured_syarray = syarray
        else:
            self._measured_syarray = np.ones_like(yarray)
        self._measured_yarray_upper = np.add(self._measured_yarray, self._measured_syarray)
        self._measured_yarray_lower = np.subtract(self._measured_yarray, self._measured_syarray)

    def _setCalculatedDataArrays(self, xarray, yarray):
        self._calculated_xarray = xarray
        self._calculated_yarray = yarray

    def _setDifferenceDataArrays(self):
        self._difference_yarray = np.subtract(self._measured_yarray, self._calculated_yarray)
        self._difference_yarray_upper = np.add(self._difference_yarray, self._measured_syarray)
        self._difference_yarray_lower = np.subtract(self._difference_yarray, self._measured_syarray)

    def _setBraggDataArrays(self, phase_index, xarray, harray, karray, larray):
        self._bragg_arrays[phase_index] = {
            'x': xarray,
            'y': np.full(xarray.size, -phase_index),
            'h': harray,
            'k': karray,
            'l': larray
        }

    def _setBackgroundDataArrays(self, xarray, yarray):
        self._background_xarray = xarray
        self._background_yarray = yarray

    def _setBokehMeasuredDataObj(self):
        self._bokeh_measured_data_obj = {
            'x': Plotting1dLogic.aroundX(self._measured_xarray),
            'y': Plotting1dLogic.aroundY(self._measured_yarray),
            'sy': Plotting1dLogic.aroundY(self._measured_syarray),
            'y_upper': Plotting1dLogic.aroundY(self._measured_yarray_upper),
            'y_lower': Plotting1dLogic.aroundY(self._measured_yarray_lower)
        }
        self.bokehMeasuredDataObjChanged.emit()

    def _setBokehPhasesDataObj(self):
        for phase_index in range(len(self.parent.l_phase.phases)):
            # skip this step with try-except block until instrumental parameters are defined/loaded
            try:
                if not self.parent.l_experiment.spin_polarized:
                    yarray = self._interface.get_calculated_y_for_phase(phase_index)
                    is_diff = False
                else:
                    phases_y = list(self._interface.get_component('phases').values())[phase_index]
                    component = self.parent.l_experiment.spinComponent()
                    is_diff = False
                    if component == "Sum":
                        yarray = phases_y["components"]["up"] + phases_y["components"]["down"]
                    elif component == "Difference":
                        yarray = phases_y["components"]["up"] - phases_y["components"]["down"]
                        is_diff = True
                    elif component == "Up":
                        yarray = phases_y["components"]["up"]
                    elif component == "Down":
                        yarray = phases_y["components"]["down"]

                if self._background_yarray.size and not is_diff:
                    self._bokeh_phases_data_obj[f'{phase_index}'] = {
                        'x': Plotting1dLogic.aroundX(self._calculated_xarray),
                        'y_upper': Plotting1dLogic.aroundY(yarray + self._background_yarray),
                        'y_lower': Plotting1dLogic.aroundY(self._background_yarray)
                    }
                else:
                    self._bokeh_phases_data_obj[f'{phase_index}'] = {
                        'x': Plotting1dLogic.aroundX(self._calculated_xarray),
                        'y_upper': Plotting1dLogic.aroundY(yarray),
                        'y_lower': Plotting1dLogic.aroundY(np.zeros_like(yarray))
                    }
            except Exception:
                continue
        self.bokehPhasesDataObjChanged.emit()

    def setCalculatedDataForPhase(self):
        self._setBokehPhasesDataObj()

    def setTotalDataForPhases(self):
        new_xarray, new_yarray = self._interface.get_total_y_for_phases()
        self._measured_yarray = new_yarray
        self._measured_xarray = new_xarray
        self.setMeasuredData(self._measured_xarray, self._measured_yarray)

    def _setBokehCalculatedDataObj(self):
        self._bokeh_calculated_data_obj = {
            'x': Plotting1dLogic.aroundX(self._calculated_xarray),
            'y': Plotting1dLogic.aroundY(self._calculated_yarray)
        }
        self.bokehCalculatedDataObjChanged.emit()

    def _setBokehDifferenceDataObj(self):
        self._bokeh_difference_data_obj = {
            'x': Plotting1dLogic.aroundY(self._measured_xarray),
            'y': Plotting1dLogic.aroundY(self._difference_yarray),
            'y_upper': Plotting1dLogic.aroundY(self._difference_yarray_upper),
            'y_lower': Plotting1dLogic.aroundY(self._difference_yarray_lower)
        }
        self.bokehDifferenceDataObjChanged.emit()

    def _setBokehBraggDataObj(self, phase_index):
        self._bokeh_bragg_data_obj[f'{phase_index}'] = {
            'x': Plotting1dLogic.aroundX(self._bragg_arrays[phase_index]['x']),
            'y': Plotting1dLogic.aroundY(self._bragg_arrays[phase_index]['y']),
            'h': Plotting1dLogic.aroundHkl(self._bragg_arrays[phase_index]['h']),
            'k': Plotting1dLogic.aroundHkl(self._bragg_arrays[phase_index]['k']),
            'l': Plotting1dLogic.aroundHkl(self._bragg_arrays[phase_index]['l'])
        }
        self.bokehBraggDataObjChanged.emit()

    def _setBokehBackgroundDataObj(self):
        self._bokeh_background_data_obj = {
            'x': Plotting1dLogic.aroundX(self._background_xarray),
            'y': Plotting1dLogic.aroundY(self._background_yarray)
        }
        self.bokehBackgroundDataObjChanged.emit()

    def _setQtChartsMeasuredDataObj(self):
        self._qtcharts_measured_data_obj = {
            'xy': Plotting1dLogic.arraysToPoints(self._measured_xarray, self._measured_yarray),
            'xy_upper': Plotting1dLogic.arraysToPoints(self._measured_xarray, self._measured_yarray_upper),
            'xy_lower': Plotting1dLogic.arraysToPoints(self._measured_xarray, self._measured_yarray_lower)
        }
        self.qtchartsMeasuredDataObjChanged.emit()

    def _setQtChartsCalculatedDataObj(self):
        self._qtcharts_calculated_data_obj = {
            'xy': Plotting1dLogic.arraysToPoints(self._calculated_xarray, self._calculated_yarray)
        }
        self.qtchartsCalculatedDataObjChanged.emit()

    def _setQtChartsDifferenceDataObj(self):
        self._qtcharts_difference_data_obj = {
            'xy': Plotting1dLogic.arraysToPoints(self._measured_xarray, self._difference_yarray),
            'xy_upper': Plotting1dLogic.arraysToPoints(self._measured_xarray, self._difference_yarray_upper),
            'xy_lower': Plotting1dLogic.arraysToPoints(self._measured_xarray, self._difference_yarray_lower)
        }
        self.qtchartsDifferenceDataObjChanged.emit()

    def _setQtChartsBraggDataObj(self):
        self._qtcharts_bragg_data_obj = {
            'xy': Plotting1dLogic.arraysToPoints(self._bragg_xarray, self._bragg_yarray),
            'h': Plotting1dLogic.aroundHkl(self._bragg_harray),
            'k': Plotting1dLogic.aroundHkl(self._bragg_karray),
            'l': Plotting1dLogic.aroundHkl(self._bragg_larray)
        }
        self.qtchartsBraggDataObjChanged.emit()

    def _setQtChartsBackgroundDataObj(self):
        self._qtcharts_background_data_obj = {
            'xy': Plotting1dLogic.arraysToPoints(self._background_xarray, self._background_yarray)
        }
        self.qtchartsBackgroundDataObjChanged.emit()

    # Private: range setters

    def _setMeasuredDataRanges(self):
        self._measured_min_x = Plotting1dLogic.arrayMin(self._measured_xarray)
        self._measured_max_x = Plotting1dLogic.arrayMax(self._measured_xarray)
        self._measured_min_y = Plotting1dLogic.arrayMin(self._measured_yarray_lower)
        self._measured_max_y = Plotting1dLogic.arrayMax(self._measured_yarray_upper)

    def _setCalculatedDataRanges(self):
        self._calculated_min_x = Plotting1dLogic.arrayMin(self._calculated_xarray)
        self._calculated_max_x = Plotting1dLogic.arrayMax(self._calculated_xarray)
        self._calculated_min_y = Plotting1dLogic.arrayMin(self._calculated_yarray)
        self._calculated_max_y = Plotting1dLogic.arrayMax(self._calculated_yarray)

    def _setDifferenceDataRanges(self):
        self._difference_min_y = Plotting1dLogic.arrayMin(self._difference_yarray_lower)
        self._difference_max_y = Plotting1dLogic.arrayMax(self._difference_yarray_upper)
        self._difference_median_y = Plotting1dLogic.arrayMedian(self._difference_yarray)

    def _yAxisMin(self, min_y, max_y):
        return min_y - self._y_axis_range_extension * max_y

    def _yAxisMax(self, max_y):
        return max_y + self._y_axis_range_extension * max_y

    def _setExperimentPlotRanges(self):
        self._experiment_plot_ranges_obj = {
            'min_x': Plotting1dLogic.aroundX(self._measured_min_x),
            'max_x': Plotting1dLogic.aroundX(self._measured_max_x),
            'min_y': Plotting1dLogic.aroundY(self._yAxisMin(self._measured_min_y, self._measured_max_y)),
            'max_y': Plotting1dLogic.aroundY(self._yAxisMax(self._measured_max_y))
        }
        self.experimentPlotRangesObjChanged.emit()

    def _setAnalysisPlotRanges(self):
        min_x = self._calculated_min_x
        max_x = self._calculated_max_x
        min_y = self._calculated_min_y
        max_y = self._calculated_max_y
        if self._measured_xarray.size:
            min_x = self._measured_min_x
            max_x = self._measured_max_x
            min_y = min(self._measured_min_y, self._calculated_min_y)
            max_y = max(self._measured_max_y, self._calculated_max_y)
        self._analysis_plot_ranges_obj = {
            'min_x': Plotting1dLogic.aroundX(min_x),
            'max_x': Plotting1dLogic.aroundX(max_x),
            'min_y': Plotting1dLogic.aroundY(self._yAxisMin(min_y, max_y)),
            'max_y': Plotting1dLogic.aroundY(self._yAxisMax(max_y))
        }
        self.analysisPlotRangesObjChanged.emit()

    # Static methods

    @staticmethod
    def around(a, decimals=2):
        rounded = np.around(a, decimals=decimals)
        if isinstance(rounded, (int, float)):
            return rounded.item()
        elif isinstance(rounded, np.ndarray):
            return rounded.tolist()

    @staticmethod
    def aroundX(a):
        return Plotting1dLogic.around(a, decimals=2)

    @staticmethod
    def aroundY(a):
        return Plotting1dLogic.around(a, decimals=2)

    @staticmethod
    def aroundHkl(a):
        return Plotting1dLogic.around(a, decimals=3)

    @staticmethod
    def arrayMin(array):
        if array.size:
            return np.amin(array).item()
        return 0

    @staticmethod
    def arrayMax(array):
        if array.size:
            return np.amax(array).item()
        return 1

    @staticmethod
    def arrayMedian(array):
        if array.size:
            return np.median(array).item()
        return 0.5

    @staticmethod
    def arrayToString(array):
        string = np.array2string(
            array,
            separator=',',
            precision=2,
            suppress_small=True,
            max_line_width=99999,
            threshold=99999
        )
        string = string.replace(' ', '')
        return string

    @staticmethod
    def stringToFloatList(string):
        array = np.fromstring(
            string,
            separator=',',
            dtype=float
        )
        float_list = array.tolist()
        return float_list

    @staticmethod
    def arraysToPoints(xarray, yarray):
        xarray = Plotting1dLogic.aroundX(xarray)
        yarray = Plotting1dLogic.aroundY(yarray)
        return [QPointF(x, y) for x, y in zip(xarray, yarray)]
