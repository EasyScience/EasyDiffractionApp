from easyCore import np
from dicttoxml import dicttoxml

from PySide2.QtCore import QObject, Signal
from easyDiffractionLib.Elements.Backgrounds.Point import PointBackground, BackgroundPoint


class BackgroundLogic(QObject):

    asObjChanged = Signal('QVariant')
    asXmlChanged = Signal()

    def __init__(self, parent, sample=None):
        super().__init__(parent)
        self.parent = parent
        self._sample = sample
        self._background_as_xml = ""
        self.asObjChanged.connect(self.onAsObjChanged)
        self._bg_types = {
            'point': {
                'container': PointBackground,
                'element': BackgroundPoint
            }
        }
        self._default_type = 'point'

    def removeAllPoints(self):
        for point_name in self._background_as_obj.names:
            self.removePoint(point_name)
        # self.asObjChanged.emit(self._background_as_obj)

    def onAsObjChanged(self):
        print(f"***** onAsObjChanged")
        self._setAsXml()

    def _setAsXml(self):
        if self.parent._background_as_obj is None:
            self._background_as_xml = dicttoxml({}, attr_type=False).decode()
        else:
            background = np.array([item.as_dict() for item in self.parent._background_as_obj])
            point_index = np.array([item.x.raw_value for item in self.parent._background_as_obj]).argsort()
            self._background_as_xml = dicttoxml(background[point_index], attr_type=False).decode()
        self.asXmlChanged.emit()

    def setDefaultPoints(self):
        print("+ setDefaultPoints")

        if self.parent._background_as_obj is None:
            # TODO THIS IS NOT HOW TO DO THINGS!!!
            self.initializeContainer()
        # remove old points
        for point_name in self.parent._background_as_obj.names:
            point_index = self.parent._background_as_obj.names.index(point_name)
            del self.parent._background_as_obj[point_index]

        # add new points
        min_point = BackgroundPoint.from_pars(x=0.0, y=200.0)
        max_point = BackgroundPoint.from_pars(x=140.0, y=200.0)
        self.parent._background_as_obj.append(min_point)
        self.parent._background_as_obj.append(max_point)

        self.asObjChanged.emit(self.parent._background_as_obj)

    def initializeContainer(self, experiment_name: str = 'current_exp', container_type=None):
        container = None
        if container_type is None:
            container = self._bg_types[self._default_type]['container']
        self._sample.pattern.backgrounds.append(
            # TODO we will be the current exp name and use it here.
            container(linked_experiment=experiment_name)
        )

    def addPoint(self):
        print(f"+ addBackgroundPoint")
        if self.parent._background_as_obj is None:
            # TODO THIS IS NOT HOW TO DO THINGS!!!
            self.initializeContainer()
        x = 0.0
        y = 100.0
        if self.parent._background_as_obj.x_sorted_points.size:
            x = self.parent._background_as_obj.x_sorted_points[-1] + 10.0
        point = BackgroundPoint.from_pars(x=x, y=y)
        self.parent._background_as_obj.append(point)
        self.asObjChanged.emit(self.parent._background_as_obj)

    def removePoint(self, point_name: str):
        print(f"+ removeBackgroundPoint for point_name: {point_name}")
        point_names = self.parent._background_as_obj.names
        point_index = point_names.index(point_name)
        del self.parent._background_as_obj[point_index]

        self.asObjChanged.emit(self.parent._background_as_obj)
