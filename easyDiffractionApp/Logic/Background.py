# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from easyCore import np, borg

from easyCore.Utils.io.xml import XMLSerializer
from PySide6.QtCore import QObject, Signal
from easyDiffractionLib.elements.Backgrounds.Point import PointBackground, BackgroundPoint


class BackgroundLogic(QObject):

    asXmlChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._background_as_xml = ""
        self.asXmlChanged.connect(self.updateChartBackground)
        self._bg_types = {
            'point': {
                'container': PointBackground,
                'element': BackgroundPoint
            }
        }
        self._default_type = 'point'
        self._background_as_obj = self._background_obj()

    def _background_obj(self):
        bgs = self.parent.sampleBackgrounds()
        itm = None
        if len(bgs) > 0:
            itm = bgs[0]
        return itm

    def removeAllPoints(self):
        for point_name in self._background_as_obj.names:
            self.removePoint(point_name, silently=True)
        self._background_as_obj = self._background_obj()
        self._setAsXml()

    def backgroundLoaded(self):
        self._background_as_obj = self._background_obj()
        if self._background_as_obj is None:
            return
        self._setAsXml()

    def onAsObjChanged(self):
        print(f"***** onAsObjChanged")
        self._background_as_obj = self._background_obj()
        if self._background_as_obj is None:
            return
        self._setAsXml()
        borg.stack.enabled = False
        self.parent.updateBackground(self._background_as_obj)
        borg.stack.enabled = True

    def _setAsXml(self):
        if self._background_as_obj is None:
            self._background_as_xml = XMLSerializer().encode({})
        else:
            background = np.array([item.as_dict() for item in self._background_as_obj])
            point_index = np.array([item.x.raw_value for item in self._background_as_obj]).argsort()
            self._background_as_xml = XMLSerializer().encode(background[point_index])
        self.asXmlChanged.emit()

    def setDefaultPoints(self):
        if self._background_as_obj is None:
            # TODO THIS IS NOT HOW TO DO THINGS!!!
            self.initializeContainer()
        # remove old points
        for point_name in self._background_as_obj.names:
            point_index = self._background_as_obj.names.index(point_name)
            del self._background_as_obj[point_index]

        # add new points
        min_point = BackgroundPoint.from_pars(x=0.0, y=200.0)
        max_point = BackgroundPoint.from_pars(x=140.0, y=200.0)
        self._background_as_obj.append(min_point)
        self._background_as_obj.append(max_point)

        self.onAsObjChanged()

    def initializeContainer(self, experiment_name: str = 'current_exp', container_type=None):
        container = None
        if container_type is None:
            container = self._bg_types[self._default_type]['container']
        self.parent.sampleBackgrounds().append(
            # TODO we will be the current exp name and use it here.
            container(linked_experiment=experiment_name)
        )
        self._background_as_obj = self._background_obj()

    def addPoint(self, x: float, y: float, silently: bool = False):
        print(f"+ add background point ({x}, {y})")
        if self._background_as_obj is None:
            # TODO THIS IS NOT HOW TO DO THINGS!!!
            self.initializeContainer()
        point = BackgroundPoint.from_pars(x=x, y=y)
        self._background_as_obj.append(point)
        if not silently:
            self.onAsObjChanged()

    def addPoints(self, xarray, yarray):
        if self._background_as_obj is None:
            self.initializeContainer()
        for x, y in zip(xarray, yarray):
            print(f"+ add background point ({x}, {y})")
            point = BackgroundPoint.from_pars(x=x, y=y)
            self._background_as_obj.append(point)
        self.onAsObjChanged()

    def addDefaultPoint(self):
        print(f"+ add default background point")
        x = 0.0
        y = 100.0
        if self._background_as_obj is not None and self._background_as_obj.x_sorted_points.size:
            x = self._background_as_obj.x_sorted_points[-1] + 10.0
        self.addPoint(x, y)

    def removePoint(self, point_name: str, silently: bool = False):
        print(f"+ removeBackgroundPoint for point_name: {point_name}")
        point_names = self._background_as_obj.names
        point_index = point_names.index(point_name)
        del self._background_as_obj[point_index]
        if not silently:
            self.onAsObjChanged()

    def updateChartBackground(self):
        if self._background_as_obj is None:
            return
        self.parent.setBackgroundData(
                            self._background_as_obj.x_sorted_points,
                            self._background_as_obj.y_sorted_points)
