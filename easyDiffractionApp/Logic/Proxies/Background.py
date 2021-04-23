__author__ = 'github.com/AndrewSazonov'
__version__ = '0.0.1'

import timeit
from dicttoxml import dicttoxml

from PySide2.QtCore import QObject, Property, Signal, Slot

from easyCore import np
from easyDiffractionLib.Elements.Backgrounds.Point import PointBackground, BackgroundPoint


class BackgroundProxy(QObject):

    asObjChanged = Signal('QVariant')
    asXmlChanged = Signal()
    dummySignal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._background_as_obj = PointBackground(linked_experiment='NEED_TO_CHANGE')
        self._background_as_xml = ""

        self.asObjChanged.connect(self.onAsObjChanged)

    @Property('QVariant', notify=dummySignal)
    def asObj(self):
        #print("+ backgroundAsObj")
        return self._background_as_obj

    @Property(str, notify=asXmlChanged)
    def asXml(self):
        #print("+ backgroundAsXml")
        return self._background_as_xml

    @Slot()
    def setDefaultPoints(self):
        print("+ setDefaultPoints")

        # remove old points
        for point_name in self._background_as_obj.names:
            point_index = self._background_as_obj.names.index(point_name)
            del self._background_as_obj[point_index]

        # add new points
        min_point = BackgroundPoint.from_pars(x=0.0, y=200.0)
        max_point = BackgroundPoint.from_pars(x=140.0, y=200.0)
        self._background_as_obj.append(min_point)
        self._background_as_obj.append(max_point)

        self.asObjChanged.emit(self._background_as_obj)

    @Slot()
    def addPoint(self):
        print(f"+ addBackgroundPoint")
        x = 0.0
        y = 100.0
        if self._background_as_obj.x_sorted_points.size:
            x = self._background_as_obj.x_sorted_points[-1] + 10.0
        point = BackgroundPoint.from_pars(x=x, y=y)
        self._background_as_obj.append(point)

        self.asObjChanged.emit(self._background_as_obj)

    @Slot(str)
    def removePoint(self, point_name: str):
        print(f"+ removeBackgroundPoint for point_name: {point_name}")
        point_names = self._background_as_obj.names
        point_index = point_names.index(point_name)
        del self._background_as_obj[point_index]

        self.asObjChanged.emit(self._background_as_obj)

    def removeAllPoints(self):
        for point_name in self._background_as_obj.names:
            self.removePoint(point_name)
        #self.asObjChanged.emit(self._background_as_obj)

    def onAsObjChanged(self):
        print(f"***** onAsObjChanged")
        self._setAsXml()

    def _setAsXml(self):
        start_time = timeit.default_timer()

        background = np.array([item.as_dict() for item in self._background_as_obj])
        point_index = np.array([item.x.raw_value for item in self._background_as_obj]).argsort()
        self._background_as_xml = dicttoxml(background[point_index], attr_type=False).decode()

        print("+ _setAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))

        self.asXmlChanged.emit()
