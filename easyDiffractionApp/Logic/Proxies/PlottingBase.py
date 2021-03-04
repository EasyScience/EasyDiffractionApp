__author__ = 'github.com/andrewsazonov'
__version__ = '0.0.1'

import numpy as np

from PySide2.QtCore import QObject, Signal, Property


class BaseProxy(QObject):
    """
    A base bridge class to interact between the QML plot and Python datasets.
    """

    measuredDataObjChanged = Signal()
    calculatedDataObjChanged = Signal()
    differenceDataObjChanged = Signal()
    braggDataObjChanged = Signal()

    experimentPlotRangesObjChanged = Signal()
    analysisPlotRangesObjChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Ranges
        self._measured_min_x = np.Inf
        self._measured_max_x = -np.Inf
        self._measured_min_y = np.Inf
        self._measured_max_y = -np.Inf

        self._calculated_min_x = np.Inf
        self._calculated_max_x = -np.Inf
        self._calculated_min_y = np.Inf
        self._calculated_max_y = -np.Inf

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

        self._bragg_xarray = np.empty(0)
        self._bragg_yarray = np.empty(0)

        # Ranges and data containers for GUI
        self._measured_data_obj = {}
        self._calculated_data_obj = {}
        self._difference_data_obj = {}
        self._bragg_data_obj = {}
        self._experiment_plot_ranges_obj = {}
        self._analysis_plot_ranges_obj = {}

    # Public: QML frontend

    @Property('QVariant', notify=measuredDataObjChanged)
    def measuredDataObj(self):
        return self._measured_data_obj

    @Property('QVariant', notify=calculatedDataObjChanged)
    def calculatedDataObj(self):
        return self._calculated_data_obj

    @Property('QVariant', notify=differenceDataObjChanged)
    def differenceDataObj(self):
        return self._difference_data_obj

    @Property('QVariant', notify=braggDataObjChanged)
    def braggDataObj(self):
        return self._bragg_data_obj

    @Property('QVariant', notify=experimentPlotRangesObjChanged)
    def experimentPlotRangesObj(self):
        return self._experiment_plot_ranges_obj

    @Property('QVariant', notify=analysisPlotRangesObjChanged)
    def analysisPlotRangesObj(self):
        return self._analysis_plot_ranges_obj

    # Public: Python backend

    def setMeasuredData(self, xarray, yarray, syarray=None):
        self._setMeasuredDataArrays(xarray, yarray, syarray)
        self._setMeasuredDataRanges()
        self._setMeasuredDataObj()
        self._setExperimentPlotRanges()
        self._setAnalysisPlotRanges()

    def setCalculatedData(self, xarray, yarray):
        self._setCalculatedDataArrays(xarray, yarray)
        self._setCalculatedDataRanges()
        self._setCalculatedDataObj()
        self._setAnalysisPlotRanges()
        if self._measured_xarray.size:
            self._setDifferenceDataArrays()
            self._setDifferenceDataRanges()
            self._setDifferenceDataObj()

    def setBraggData(self, xarray):
        self._setBraggDataArrays(xarray)
        self._setBraggDataObj()

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

    def _setBraggDataArrays(self, xarray):
        self._bragg_xarray = xarray
        self._bragg_yarray = np.zeros(self._bragg_xarray.size)

    def _setMeasuredDataObj(self):
        raise NotImplementedError('Must be implemented in subclass.')

    def _setCalculatedDataObj(self):
        raise NotImplementedError('Must be implemented in subclass.')

    def _setDifferenceDataObj(self):
        raise NotImplementedError('Must be implemented in subclass.')

    def _setBraggDataObj(self):
        raise NotImplementedError('Must be implemented in subclass.')

    # Private: range setters

    def _setMeasuredDataRanges(self):
        self._measured_min_x = BaseProxy.arrayMin(self._measured_xarray)
        self._measured_max_x = BaseProxy.arrayMax(self._measured_xarray)
        self._measured_min_y = BaseProxy.arrayMin(self._measured_yarray_lower)
        self._measured_max_y = BaseProxy.arrayMax(self._measured_yarray_upper)

    def _setCalculatedDataRanges(self):
        self._calculated_min_x = BaseProxy.arrayMin(self._calculated_xarray)
        self._calculated_max_x = BaseProxy.arrayMax(self._calculated_xarray)
        self._calculated_min_y = BaseProxy.arrayMin(self._calculated_yarray)
        self._calculated_max_y = BaseProxy.arrayMax(self._calculated_yarray)

    def _setDifferenceDataRanges(self):
        self._difference_min_y = BaseProxy.arrayMin(self._difference_yarray_lower)
        self._difference_max_y = BaseProxy.arrayMax(self._difference_yarray_upper)
        self._difference_median_y = BaseProxy.arrayMedian(self._difference_yarray)

    def _yAxisMin(self, min_y, max_y):
        return min_y - self._y_axis_range_extension * max_y

    def _yAxisMax(self, max_y):
        return max_y + self._y_axis_range_extension * max_y

    def _setExperimentPlotRanges(self):
        self._experiment_plot_ranges_obj = {
            'min_x': BaseProxy.aroundX(self._measured_min_x),
            'max_x': BaseProxy.aroundX(self._measured_max_x),
            'min_y': BaseProxy.aroundY(self._yAxisMin(self._measured_min_y, self._measured_max_y)),
            'max_y': BaseProxy.aroundY(self._yAxisMax(self._measured_max_y))
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
            'min_x': BaseProxy.aroundX(min_x),
            'max_x': BaseProxy.aroundX(max_x),
            'min_y': BaseProxy.aroundY(self._yAxisMin(min_y, max_y)),
            'max_y': BaseProxy.aroundY(self._yAxisMax(max_y))
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
        return BaseProxy.around(a, decimals=2)

    @staticmethod
    def aroundY(a):
        return BaseProxy.around(a, decimals=1)

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
