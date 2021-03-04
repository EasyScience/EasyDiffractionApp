__author__ = 'github.com/andrewsazonov'
__version__ = '0.0.1'

from easyDiffractionApp.Logic.Proxies.PlottingBase import BaseProxy


class BokehProxy(BaseProxy):
    """
    A bridge class to interact between the QML Bokeh plot and Python datasets.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def _setMeasuredDataObj(self):
        self._measured_data_obj = {
            'x': BaseProxy.aroundX(self._measured_xarray),
            'y': BaseProxy.aroundY(self._measured_yarray),
            'sy': BaseProxy.aroundY(self._measured_syarray),
            'y_upper': BaseProxy.aroundY(self._measured_yarray_upper),
            'y_lower': BaseProxy.aroundY(self._measured_yarray_lower)
        }
        self.measuredDataObjChanged.emit()

    def _setCalculatedDataObj(self):
        self._calculated_data_obj = {
            'x': BaseProxy.aroundX(self._calculated_xarray),
            'y': BaseProxy.aroundY(self._calculated_yarray)
        }
        self.calculatedDataObjChanged.emit()

    def _setDifferenceDataObj(self):
        self._difference_data_obj = {
            'y': BaseProxy.aroundY(self._difference_yarray),
            'y_upper': BaseProxy.aroundY(self._difference_yarray_upper),
            'y_lower': BaseProxy.aroundY(self._difference_yarray_lower),
            'max_y': BaseProxy.aroundY(self._difference_max_y),
            'min_y': BaseProxy.aroundY(self._difference_min_y),
            'median_y': BaseProxy.aroundY(self._difference_median_y)
        }
        self.differenceDataObjChanged.emit()

    def _setBraggDataObj(self):
        self._bragg_data_obj = {
            'x': BaseProxy.aroundX(self._bragg_xarray),
            'y': BaseProxy.aroundY(self._bragg_yarray),
        }
        self.braggDataObjChanged.emit()
