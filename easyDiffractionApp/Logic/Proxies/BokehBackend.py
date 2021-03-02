__author__ = 'github.com/andrewsazonov'
__version__ = '0.0.1'

import numpy as np

from PySide2.QtCore import QObject, Signal, Property


class BokehBridge(QObject):
    """
    A bridge class to interact with the Bokeh plot
    """

    measuredDataObjChanged = Signal()
    calculatedDataObjChanged = Signal()
    braggDataObjChanged = Signal()
    differenceDataObjChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Internal data arrays
        self._measured_xarray = np.empty(0)
        self._measured_yarray = np.empty(0)
        self._measured_syarray = np.empty(0)

        # Data containers for GUI
        self._measured_data_obj = {}
        self._calculated_data_obj = {}
        self._bragg_data_obj = {}
        self._difference_data_obj = {}

    @Property('QVariant', notify=measuredDataObjChanged)
    def measuredDataObj(self):
        return self._measured_data_obj

    @Property('QVariant', notify=calculatedDataObjChanged)
    def calculatedDataObj(self):
        return self._calculated_data_obj

    @Property('QVariant', notify=braggDataObjChanged)
    def braggDataObj(self):
        return self._bragg_data_obj

    @Property('QVariant', notify=differenceDataObjChanged)
    def differenceDataObj(self):
        return self._difference_data_obj

    def setMeasuredData(self, xarray, yarray, syarray):
        top_yarray = np.add(yarray, syarray)
        bottom_yarray = np.subtract(yarray, syarray)
        self._measured_data_obj = {
            'x': self.arrayToString(xarray),
            'y': self.arrayToString(yarray),
            'y_top': self.arrayToString(top_yarray),
            'y_bottom': self.arrayToString(bottom_yarray),
            'max_x': np.amax(xarray).item(),
            'min_x': np.amin(xarray).item(),
            'max_y': np.amax(top_yarray).item(),
            'min_y': np.amin(bottom_yarray).item()
        }
        self._measured_xarray = xarray
        self._measured_yarray = yarray
        self._measured_syarray = syarray
        self.measuredDataObjChanged.emit()

    def setCalculatedData(self, xarray, yarray):
        self._calculated_data_obj = {
            'x': self.arrayToString(xarray),
            'y': self.arrayToString(yarray),
            'max_x': np.amax(xarray).item(),
            'min_x': np.amin(xarray).item(),
            'max_y': np.amax(yarray).item(),
            'min_y': np.amin(yarray).item()
        }
        self.calculatedDataObjChanged.emit()

        self._bragg_data_obj = {
            'x': self.arrayToString(np.array([20., 35., 100.])),
            'y': self.arrayToString(np.array([0., 0., 0.]))
        }
        self.braggDataObjChanged.emit()

        if len(self._measured_yarray):
            difference_yarray = np.subtract(self._measured_yarray, yarray)
            difference_top_yarray = np.add(difference_yarray, self._measured_syarray)
            difference_bottom_yarray = np.subtract(difference_yarray, self._measured_syarray)
            self._difference_data_obj = {
                'x': self.arrayToString(self._measured_xarray),
                'y': self.arrayToString(difference_yarray),
                'y_top': self.arrayToString(difference_top_yarray),
                'y_bottom': self.arrayToString(difference_bottom_yarray),
                'max_x': np.amax(xarray).item(),
                'min_x': np.amin(xarray).item(),
                'max_y': np.amax(difference_top_yarray).item(),
                'min_y': np.amin(difference_bottom_yarray).item(),
                'median_y': np.median(difference_yarray).item()
            }
            self.differenceDataObjChanged.emit()

    def arrayToString(self, array):
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
