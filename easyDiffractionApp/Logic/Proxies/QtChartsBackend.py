__author__ = 'github.com/andrewsazonov'
__version__ = '0.0.1'

import numpy as np

from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCore import QPointF
from PySide2.QtCharts import QtCharts


class QtChartsBridge(QObject):
    """
    A bridge class to interact with the plot
    """

    chartsRangesChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._experiment_measured_lower = None
        self._experiment_measured_upper = None

        self._analysis_measured_lower = None
        self._analysis_measured_upper = None
        self._analysis_calculated = None
        self._analysis_difference_lower = None
        self._analysis_difference_upper = None

        self._measured_xarray = np.empty(0)
        self._measured_yarray = np.empty(0)
        self._measured_syarray = np.empty(0)
        self._calculated_xarray = np.empty(0)
        self._calculated_yarray = np.empty(0)
        self._difference_xarray = np.empty(0)
        self._difference_yarray = np.empty(0)

        self._experiment_xmin = 0.
        self._experiment_xmax = 100.
        self._experiment_ymin = 0.
        self._experiment_ymax = 100.
        self._analysis_xmin = 0.
        self._analysis_xmax = 100.
        self._analysis_ymin = 0.
        self._analysis_ymax = 100.
        self._difference_ymin = 0.
        self._difference_ymax = 100.

    @Slot(QtCharts.QXYSeries)
    def setExperimentMeasuredLower(self, series):
        self._experiment_measured_lower = series

    @Slot(QtCharts.QXYSeries)
    def setExperimentMeasuredUpper(self, series):
        self._experiment_measured_upper = series

    @Slot(QtCharts.QXYSeries)
    def setAnalysisMeasuredLower(self, series):
        self._analysis_measured_lower = series

    @Slot(QtCharts.QXYSeries)
    def setAnalysisMeasuredUpper(self, series):
        self._analysis_measured_upper = series

    @Slot(QtCharts.QXYSeries)
    def setAnalysisCalculated(self, series):
        self._analysis_calculated = series

    @Slot(QtCharts.QXYSeries)
    def setAnalysisDifferenceLower(self, series):
        self._analysis_difference_lower = series

    @Slot(QtCharts.QXYSeries)
    def setAnalysisDifferenceUpper(self, series):
        self._analysis_difference_upper = series

    @Property(float, notify=chartsRangesChanged)
    def experimentXmin(self):
        return self._experiment_xmin

    @Property(float, notify=chartsRangesChanged)
    def experimentXmax(self):
        return self._experiment_xmax

    @Property(float, notify=chartsRangesChanged)
    def experimentYmin(self):
        return self._experiment_ymin

    @Property(float, notify=chartsRangesChanged)
    def experimentYmax(self):
        return self._experiment_ymax

    @Property(float, notify=chartsRangesChanged)
    def analysisXmin(self):
        return self._analysis_xmin

    @Property(float, notify=chartsRangesChanged)
    def analysisXmax(self):
        return self._analysis_xmax

    @Property(float, notify=chartsRangesChanged)
    def analysisYmin(self):
        return self._analysis_ymin

    @Property(float, notify=chartsRangesChanged)
    def analysisYmax(self):
        return self._analysis_ymax

    @Property(float, notify=chartsRangesChanged)
    def differenceYmin(self):
        return self._difference_ymin

    @Property(float, notify=chartsRangesChanged)
    def differenceYmax(self):
        return self._difference_ymax

    @experimentXmin.setter
    def experimentXminSetter(self, value):
        if self._experiment_xmin == value:
            return

        self._experiment_xmin = value
        self.chartsRangesChanged.emit()

    @experimentXmax.setter
    def experimentXmaxSetter(self, value):
        if self._experiment_xmax == value:
            return

        self._experiment_xmax = value
        self.chartsRangesChanged.emit()

    @experimentYmin.setter
    def experimentYminSetter(self, value):
        if self._experiment_ymin == value:
            return

        self._experiment_ymin = value
        self.chartsRangesChanged.emit()

    @experimentYmax.setter
    def experimentYmaxSetter(self, value):
        if self._experiment_ymax == value:
            return

        self._experiment_ymax = value
        self.chartsRangesChanged.emit()

    @analysisXmin.setter
    def analysisXminSetter(self, value):
        if self._analysis_xmin == value:
            return

        self._analysis_xmin = value
        self.chartsRangesChanged.emit()

    @analysisXmax.setter
    def analysisXmaxSetter(self, value):
        if self._analysis_xmax == value:
            return

        self._analysis_xmax = value
        self.chartsRangesChanged.emit()

    @analysisYmin.setter
    def analysisYminSetter(self, value):
        if self._analysis_ymin == value:
            return

        self._analysis_ymin = value
        self.chartsRangesChanged.emit()

    @analysisYmax.setter
    def analysisYmaxSetter(self, value):
        if self._analysis_ymax == value:
            return

        self._analysis_ymax = value
        self.chartsRangesChanged.emit()

    @differenceYmin.setter
    def differenceYminSetter(self, value):
        if self._difference_ymin == value:
            return

        self._difference_ymin = value
        self.chartsRangesChanged.emit()

    @differenceYmax.setter
    def differenceYmaxSetter(self, value):
        if self._difference_ymax == value:
            return

        self._difference_ymax = value
        self.chartsRangesChanged.emit()

    def setMeasuredData(self, xarray, yarray, syarray):
        self._measured_xarray = xarray
        self._measured_yarray = yarray
        self._measured_syarray = syarray
        self.replaceMeasuredDataOnChart()
        self.changeExperimentChartXRange()
        self.changeExperimentChartYRange()

    def setCalculatedData(self, xarray, yarray):
        self._calculated_xarray = xarray
        self._calculated_yarray = yarray
        self.replaceCalculatedDataOnChart()
        self.changeAnalysisChartXRange()
        self.changeAnalysisChartYRange()

        if len(self._measured_yarray):
            self._difference_yarray = self._measured_yarray - self._calculated_yarray
            self.replaceDifferenceDataOnChart()
            self.changeDifferenceChartYRange()

    def replaceMeasuredDataOnChart(self):
        lower_points = [QPointF(x, y) for x, y in zip(self._measured_xarray, self._measured_yarray - self._measured_syarray)]
        upper_points = [QPointF(x, y) for x, y in zip(self._measured_xarray, self._measured_yarray + self._measured_syarray)]
        self._experiment_measured_lower.replace(lower_points)
        self._experiment_measured_upper.replace(upper_points)
        self._analysis_measured_lower.replace(lower_points)
        self._analysis_measured_upper.replace(upper_points)

    def replaceCalculatedDataOnChart(self):
        points = [QPointF(x, y) for x, y in zip(self._calculated_xarray, self._calculated_yarray)]
        self._analysis_calculated.replace(points)

    def replaceDifferenceDataOnChart(self):
        lower_points = [QPointF(x, y) for x, y in zip(self._measured_xarray, self._difference_yarray - self._measured_syarray)]
        upper_points = [QPointF(x, y) for x, y in zip(self._measured_xarray, self._difference_yarray + self._measured_syarray)]
        self._analysis_difference_lower.replace(lower_points)
        self._analysis_difference_upper.replace(upper_points)

    def changeExperimentChartXRange(self):
        min_x = self._measured_xarray.min()
        max_x = self._measured_xarray.max()

        self.experimentXmin = float(min_x)
        self.experimentXmax = float(max_x)

    def changeExperimentChartYRange(self):
        min_y = self._measured_yarray.min()
        max_y = self._measured_yarray.max()

        range_y = max_y - min_y
        min_y = min_y - 0.05 * range_y
        max_y = max_y + 0.05 * range_y

        self.experimentYmin = float(min_y)
        self.experimentYmax = float(max_y)

    def changeAnalysisChartXRange(self):
        if len(self._measured_yarray):
            min_x = min(self._calculated_xarray.min(), self._measured_xarray.min())
            max_x = max(self._calculated_xarray.max(), self._measured_xarray.max())
        else:
            min_x = self._calculated_xarray.min()
            max_x = self._calculated_xarray.max()

        self.analysisXmin = float(min_x)
        self.analysisXmax = float(max_x)

    def changeAnalysisChartYRange(self):
        if len(self._measured_yarray):
            min_y = min(self._calculated_yarray.min(), self._measured_yarray.min())
            max_y = max(self._calculated_yarray.max(), self._measured_yarray.max())
        else:
            min_y = self._calculated_yarray.min()
            max_y = self._calculated_yarray.max()

        range_y = max_y - min_y
        min_y = min_y - 0.05 * range_y
        max_y = max_y + 0.05 * range_y

        self.analysisYmin = float(min_y)
        self.analysisYmax = float(max_y)

    def changeDifferenceChartYRange(self):
        min_y = (self._difference_yarray - self._measured_syarray).min()
        max_y = (self._difference_yarray + self._measured_syarray).max()

        range_y = max_y - min_y
        min_y = min_y - 0.05 * range_y
        max_y = max_y + 0.05 * range_y

        self.differenceYmin = float(min_y)
        self.differenceYmax = float(max_y)

    def updateAllCharts(self):
        self.replaceMeasuredDataOnChart()
        self.replaceCalculatedDataOnChart()
        self.replaceDifferenceDataOnChart()