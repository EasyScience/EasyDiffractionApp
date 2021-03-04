__author__ = 'github.com/andrewsazonov'
__version__ = '0.0.1'

from PySide2.QtCore import Slot
from PySide2.QtCore import QPointF

from easyDiffractionApp.Logic.Proxies.PlottingBase import BaseProxy


class QtChartsProxy(BaseProxy):
    """
    A bridge class to interact between the QML QtChart plot and Python datasets.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot('QVariant', 'QVariant')
    def lineSeriesCustomReplace(self, line_series, points):
        if points is None:
            return
        line_series.replace(points.toVariant())

    def _setMeasuredDataObj(self):
        self._measured_data_obj = {
            'xy': QtChartsProxy.arraysToPoints(self._measured_xarray, self._measured_yarray),
            'xy_upper': QtChartsProxy.arraysToPoints(self._measured_xarray, self._measured_yarray_upper),
            'xy_lower': QtChartsProxy.arraysToPoints(self._measured_xarray, self._measured_yarray_lower)
        }
        self.measuredDataObjChanged.emit()

    def _setCalculatedDataObj(self):
        self._calculated_data_obj = {
            'xy': QtChartsProxy.arraysToPoints(self._calculated_xarray, self._calculated_yarray)
        }
        self.calculatedDataObjChanged.emit()

    def _setDifferenceDataObj(self):
        self._difference_data_obj = {
            'xy': QtChartsProxy.arraysToPoints(self._measured_xarray, self._difference_yarray),
            'xy_upper': QtChartsProxy.arraysToPoints(self._measured_xarray, self._difference_yarray_upper),
            'xy_lower': QtChartsProxy.arraysToPoints(self._measured_xarray, self._difference_yarray_lower),
            'min_y': BaseProxy.aroundY(self._difference_min_y),
            'max_y': BaseProxy.aroundY(self._difference_max_y),
            'median_y': BaseProxy.aroundY(self._difference_median_y)
        }
        self.differenceDataObjChanged.emit()

    def _setBraggDataObj(self):
        self._bragg_data_obj = {
            'x': BaseProxy.aroundX(self._bragg_xarray),
            'y': BaseProxy.aroundY(self._bragg_yarray),
        }
        self.braggDataObjChanged.emit()

    @staticmethod
    def arraysToPoints(xarray, yarray):
        xarray = BaseProxy.aroundX(xarray)
        yarray = BaseProxy.aroundY(yarray)
        return [QPointF(x, y) for x, y in zip(xarray, yarray)]
