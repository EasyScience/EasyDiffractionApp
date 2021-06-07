__author__ = 'github.com/AndrewSazonov'
__version__ = '0.0.1'

from PySide2.QtCore import QObject, Property, Signal, Slot

from easyDiffractionApp.Logic.Background import BackgroundLogic


class BackgroundProxy(QObject):

    asXmlChanged = Signal()
    dummySignal = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.logic = BackgroundLogic(self)
        self.logic.asXmlChanged.connect(self.asXmlChanged)

    @property
    def _background_as_obj(self):
        # this query needs to go to logic, communicating with LC
        return self.parent.lc._background_obj

    @Property('QVariant', notify=dummySignal)
    def asObj(self):
        return self._background_as_obj

    @Property(str, notify=asXmlChanged)
    def asXml(self):
        return self.logic._background_as_xml

    @Slot()
    def setDefaultPoints(self):
        self.logic.setDefaultPoints()

    @Slot()
    def addPoint(self):
        self.logic.addPoint()

    @Slot(str)
    def removePoint(self, point_name: str):
        self.logic.removePoint(point_name)
