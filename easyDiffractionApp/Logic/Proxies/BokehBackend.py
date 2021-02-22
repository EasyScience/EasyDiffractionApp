__author__ = 'github.com/andrewsazonov'
__version__ = '0.0.1'

import numpy as np

from PySide2.QtCore import QObject, Signal, Property


class BokehBridge(QObject):
    """
    A bridge class to interact with the plot
    """

    calculatedDataObjChanged = Signal()
    measuredDataObjChanged = Signal()
    differenceDataObjChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._measured_xarray = np.empty(0)
        self._measured_yarray = np.empty(0)
        self._measured_syarray = np.empty(0)
        self._calculated_xarray = np.empty(0)
        self._calculated_yarray = np.empty(0)
        self._difference_xarray = np.empty(0)
        self._difference_yarray = np.empty(0)

        self._measured_data_obj = {}
        self._calculated_data_obj = {}
        self._difference_data_obj = {}

    @Property('QVariant', notify=measuredDataObjChanged)
    def measuredDataObj(self):
        return self._measured_data_obj

    @Property('QVariant', notify=calculatedDataObjChanged)
    def calculatedDataObj(self):
        return self._calculated_data_obj

    @Property('QVariant', notify=calculatedDataObjChanged)
    def differenceDataObj(self):
        return self._difference_data_obj

    def setMeasuredData(self, xarray, yarray, syarray):
        self._measured_xarray = xarray
        self._measured_yarray = yarray
        self._measured_syarray = syarray
        self.replaceMeasuredDataObj()

    def setCalculatedData(self, xarray, yarray):
        self._calculated_xarray = xarray
        self._calculated_yarray = yarray
        self.replaceCalculatedDataObj()

        if len(self._measured_yarray):
            self._difference_yarray = self._measured_yarray - self._calculated_yarray
            self.replaceDifferenceDataObj()

    def replaceMeasuredDataObj(self):
        self._measured_data_obj = {'x': self.arrayToString(self._measured_xarray), 'y': self.arrayToString(self._measured_yarray)}
        self.measuredDataObjChanged.emit()

    def replaceCalculatedDataObj(self):
        self._calculated_data_obj = {'x': self.arrayToString(self._calculated_xarray), 'y': self.arrayToString(self._calculated_yarray)}
        self.calculatedDataObjChanged.emit()

    def replaceDifferenceDataObj(self):
        self._difference_data_obj = {'x': self.arrayToString(self._difference_xarray), 'y': self.arrayToString(self._difference_yarray)}
        self.differenceDataObjChanged.emit()

    def arrayToString(self, array):
        string = np.array2string(array, separator=',', suppress_small=True, max_line_width=99999, threshold=99999)
        string = string.replace(' ', '')
        return string
