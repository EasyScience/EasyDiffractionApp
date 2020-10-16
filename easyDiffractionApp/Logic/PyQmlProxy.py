import sys
import json
import numpy as np
from dicttoxml import dicttoxml
from distutils.util import strtobool
from urllib.parse import urlparse

from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCharts import QtCharts

from easyCore import borg

from easyCore.Fitting.Fitting import Fitter
from easyCore.Fitting.Constraints import ObjConstraint, NumericConstraint
from easyCore.Utils.classTools import generatePath

from easyExampleLib.interface import InterfaceFactory
from easyExampleLib.model import Sin, DummySin

from easyDiffractionLib.sample import Sample
from easyDiffractionLib import Crystals
from easyDiffractionLib.interface import InterfaceFactory
from easyDiffractionLib.Elements.Instruments.Instrument import Pattern

from easyDiffractionApp.Logic.QtDataStore import QtDataStore
from easyDiffractionApp.Logic.DisplayModels.DataModels import MeasuredDataModel, CalculatedDataModel


class PyQmlProxy(QObject):
    _borg = borg

    projectInfoChanged = Signal()
    constraintsChanged = Signal()
    calculatorChanged = Signal()
    minimizerChanged = Signal()
    statusChanged = Signal()

    phasesChanged = Signal()
    modelChanged = Signal()
    currentPhaseSitesChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface = InterfaceFactory()
        self.sample = Sample(parameters=Pattern(), interface=self.interface)
        x_data = np.linspace(5, 150, 400)
        self.data = QtDataStore(x_data, np.zeros_like(x_data), np.zeros_like(x_data), None)
        self._calculated_data_model = CalculatedDataModel(self.data)
        self.project_info = self.initProjectInfo()
        #self.updateCalculatedData()

        # when to emit status bar items cnahged
        self.calculatorChanged.connect(self.statusChanged)
        self.minimizerChanged.connect(self.statusChanged)

    # Data

    @Slot()
    def updateCalculatedData(self):
        #if self.crystal is None:
        #    return
        self.data.y_opt = self.interface.fit_func(self.data.x)
        self._calculated_data_model.updateData(self.data)
        self.modelChanged.emit()

    # Calculator

    @Property('QVariant', notify=calculatorChanged)
    def calculatorList(self):
        return self.interface.available_interfaces

    @Property(int, notify=calculatorChanged)
    def calculatorIndex(self):
        return self.calculatorList.index(self.interface.current_interface_name)

    @calculatorIndex.setter
    def setCalculator(self, index: int):
        self.model.switch_interface(self.calculatorList[index])
        self.updateCalculatedData()
        self.calculatorChanged.emit()

    # Charts

    @Slot(QtCharts.QXYSeries)
    def addMeasuredSeriesRef(self, series):
        self._measured_data_model.addSeriesRef(series)

    @Slot(QtCharts.QXYSeries)
    def addLowerMeasuredSeriesRef(self, series):
        self._measured_data_model.addLowerSeriesRef(series)

    @Slot(QtCharts.QXYSeries)
    def addUpperMeasuredSeriesRef(self, series):
        self._measured_data_model.addUpperSeriesRef(series)

    @Slot(QtCharts.QXYSeries)
    def setCalculatedSeriesRef(self, series):
        self._calculated_data_model.setSeriesRef(series)

    # Status

    @Property(str, notify=statusChanged)
    def statusModelAsXml(self):
        items = [ { "label": "Calculator", "value": self.interface.current_interface_name } ]
        xml = dicttoxml(items, attr_type=False)
        xml = xml.decode()
        return xml

    # App project info

    def initProjectInfo(self):
        return dict(name = "Example Project",
                    keywords = "diffraction, cfml, cryspy",
                    samples = "samples.cif",
                    experiments = "experiments.cif",
                    calculations = "calculation.cif",
                    modified = "18.09.2020, 09:24")

    @Property('QVariant', notify=projectInfoChanged)
    def projectInfoAsJson(self):
        return self.project_info

    @projectInfoAsJson.setter
    def setProjectInfoAsJson(self, json_str):
        self.project_info = json.loads(json_str)
        self.projectInfoChanged.emit()

    @Slot(str, str)
    def editProjectInfoByKey(self, key, value):
        self.project_info[key] = value
        self.projectInfoChanged.emit()

    # Phases

    @Property('QVariant', notify=phasesChanged)
    def phasesObj(self):
        phases = self.sample.phases.as_dict()['data']
        return phases

    #@phasesObj.setter
    #def setPhasesObj(self, json_str):
    #    self.phases = json.loads(json_str)
    #    self.phasesChanged.emit()

    @Property(str, notify=phasesChanged)
    def phasesXml(self):
        #if self.sample.phase is None:
        #     return []
        phases = self.sample.phases.as_dict()['data']
        #xml = dicttoxml(phases, attr_type=False)
        xml = dicttoxml(phases, attr_type=True)
        xml = xml.decode()
        return xml

    #@Slot(int, str, str)
    #def editPhase(self, phase_index, parameter_name, new_value):
        #print("----", phase_index, parameter_name, new_value)
    #    self.phases[phase_index][parameter_name] = new_value
    #    self.phasesChanged.emit()

    #@Slot(int, int, str, str)
    #def editPhaseParameter(self, phase_index, parameter_index, parameter_name, new_value):
        #print("----", phase_index, parameter_index, parameter_name, new_value)
    #    self.phases[phase_index]['parameters'][parameter_index][parameter_name] = new_value
    #    self.phasesChanged.emit()

    @Slot(str)
    def addSampleFromCif(self, cif_path):
        #print("cif_path", cif_path)
        cif_path = self.generalizePath(cif_path)
        crystals = Crystals.from_cif_file(cif_path)
        #print(self.crystal)
        #print(self.crystal.atoms)
        self.sample.phases = crystals
        self.interface.generate_sample_binding("filename", self.sample)
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.currentPhaseSitesChanged.emit()

    @Property(str, notify=phasesChanged)
    def phasesCif(self):
        #print("str(self.crystal.cif)", str(self.crystal.cif))
        #if self.crystal is None:
        #    return ""
        return str(self.sample.phases.cif)

    @Property('QVariant', notify=currentPhaseSitesChanged)
    def currentPhaseAllSites(self):
        #self.crystal.extent = np.array([2, 2, 2])
        #print(self.crystal.all_sites())
        #print(self.crystal.extent)
        #if self.crystal is None:
        #    return []
        all_sites = self.sample.phases[0].all_sites()
        # convert numpy lists to python lists for qml
        all_sites = { k: all_sites[k].tolist() for k in all_sites.keys() }
        return all_sites

    # Misc

    @Slot(str, float)
    def editParameterValue(self, obj_id: str, new_value: float):
        if not obj_id:
            return
        print("----0 obj_id, new_value", obj_id, new_value)
        obj = borg.map.get_item_by_key(int(obj_id))
        print("----1 obj.name, obj.value", obj.name, obj.value)
        obj.value = new_value
        print("----2 obj.name, obj.value", obj.name, obj.value)
        self.phasesChanged.emit()
        self.updateCalculatedData()

    def generalizePath(self, rcif_path: str) -> str:
        """
        Generalize the filepath to be platform-specific, so all file operations
        can be performed.
        :param URI rcfPath: URI to the file
        :return URI filename: platform specific URI
        """
        filename = urlparse(rcif_path).path
        if not sys.platform.startswith("win"):
            return filename
        if filename[0] == '/':
            filename = filename[1:].replace('/', os.path.sep)
        return filename




