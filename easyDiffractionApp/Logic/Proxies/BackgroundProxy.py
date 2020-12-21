__author__ = 'github.com/AndrewSazonov'
__version__ = '0.0.1'

import timeit
from dicttoxml import dicttoxml

from PySide2.QtCore import QObject, Property, Signal, Slot

from easyCore import np
from easyDiffractionLib.Elements.Backgrounds.Point import PointBackground, BackgroundPoint


class BackgroundProxy(QObject):

    backgroundChanged = Signal()
    backgroundAsXmlChanged = Signal()

    def __init__(self, sample, parent=None):
        super().__init__(parent)

        self._sample = sample

        self._background_as_obj = self._defaultBackground()
        self._background_as_xml = ""

        self.backgroundChanged.connect(self._onBackgroundChanged)

    @Property('QVariant', constant=True)
    def asObj(self):
        #print("+ backgroundAsObj")
        return self._background_as_obj

    @Property(str, notify=backgroundAsXmlChanged)
    def asXml(self):
        #print("+ backgroundAsXml")
        return self._background_as_xml

    @Slot()
    def addPoint(self):
        print(f"+ addBackgroundPoint")
        self._sample.remove_background(self._background_as_obj)
        point = BackgroundPoint.from_pars(x=180.0, y=0.0)
        self._background_as_obj.append(point)
        self._sample.set_background(self._background_as_obj)
        self.backgroundChanged.emit()

    @Slot(str)
    def removePoint(self, background_point_x_name: str):
        print(f"+ removeBackgroundPoint for background_point_x_name: {background_point_x_name}")
        self._sample.remove_background(self._background_as_obj)
        names = self._background_as_obj.names
        del self._background_as_obj[names.index(background_point_x_name)]
        self._sample.set_background(self._background_as_obj)
        self.backgroundChanged.emit()

    def _defaultBackground(self):
        print("+ _defaultBackground")
        background = PointBackground(
            BackgroundPoint.from_pars(0, 200),
            BackgroundPoint.from_pars(140, 200),
            linked_experiment='NEED_TO_CHANGE'
        )
        return background

    def _setBackgroundAsXml(self):
        start_time = timeit.default_timer()
        background = np.array([item.as_dict() for item in self._background_as_obj])
        idx = np.array([item.x.raw_value for item in self._background_as_obj]).argsort()
        self._background_as_xml = dicttoxml(background[idx], attr_type=False).decode()
        print("+ _setBackgroundAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.backgroundAsXmlChanged.emit()

    def _onBackgroundChanged(self):
        print(f"***** _onBackgroundChanged")
        self._setBackgroundAsXml()
