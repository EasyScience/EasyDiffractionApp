import sys
import os
import json
import numpy as np
from dicttoxml import dicttoxml
from distutils.util import strtobool
from urllib.parse import urlparse

from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCharts import QtCharts

from easyCore import borg

# borg.debug = True

from easyCore.Symmetry.tools import SpacegroupInfo
from easyCore.Fitting.Fitting import Fitter
from easyCore.Fitting.Constraints import ObjConstraint, NumericConstraint
from easyCore.Utils.classTools import generatePath

from easyExampleLib.interface import InterfaceFactory

from easyDiffractionLib.sample import Sample
from easyDiffractionLib import Crystals
from easyDiffractionLib.interface import InterfaceFactory
from easyDiffractionLib.Elements.Instruments.Instrument import Pattern

from easyDiffractionApp.Logic.QtDataStore import QtDataStore
from easyDiffractionApp.Logic.DisplayModels.DataModels import MeasuredDataModel, CalculatedDataModel

from easyDiffractionApp.Logic.MatplotlibBackend import DisplayBridge

from easyCore.Symmetry.groups import SpaceGroup

sgs = [op['hermann_mauguin_fmt'] for op in SpaceGroup.SYMM_OPS]


class PyQmlProxy(QObject):
    _borg = borg

    bridge = DisplayBridge()

    projectInfoChanged = Signal()
    constraintsChanged = Signal()
    calculatorChanged = Signal()
    minimizerChanged = Signal()
    statusChanged = Signal()
    phasesChanged = Signal()
    modelChanged = Signal()
    currentPhaseChanged = Signal()
    currentPhaseSitesChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface = InterfaceFactory()

        self.sample = Sample(parameters=Pattern(), interface=self.interface)
        self.sample.parameters.u_resolution=0.4
        self.sample.parameters.v_resolution=-0.5
        self.sample.parameters.w_resolution=0.9
        self.sample.parameters.x_resolution=0.0
        self.sample.parameters.y_resolution=0.0

        x_data = np.linspace(5, 150, 1000)
        self.data = QtDataStore(x_data, np.zeros_like(x_data), np.zeros_like(x_data), None)
        self._calculated_data_model = CalculatedDataModel(self.data)

        self.project_info = self.initProjectInfo()

        self._current_phase_index = 0

        # when to emit status bar items cnahged
        self.calculatorChanged.connect(self.statusChanged)
        self.minimizerChanged.connect(self.statusChanged)

    # Calculated data

    @Slot()
    def updateCalculatedData(self):
        self.sample.output_index = self.currentPhaseIndex
        self.data.y_opt = self.interface.fit_func(self.data.x)
        self._calculated_data_model.updateData(self.data)
        self.bridge.updateWithCanvas('figure', {'x': self.data.x,
                                                'y': self.data.y_opt})
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
        self.interface.switch(self.calculatorList[index])
        self.sample._updateInterface()
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
        items = [{"label": "Calculator", "value": self.interface.current_interface_name}]
        xml = dicttoxml(items, attr_type=False)
        xml = xml.decode()
        return xml

    # App project info

    def initProjectInfo(self):
        return dict(name="Example Project",
                    keywords="diffraction, cfml, cryspy",
                    samples="samples.cif",
                    experiments="experiments.cif",
                    calculations="calculation.cif",
                    modified="18.09.2020, 09:24")

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

    @Slot(str)
    def addSampleFromCif(self, cif_path):
        cif_path = self.generalizePath(cif_path)
        crystals = Crystals.from_cif_file(cif_path)
        crystals.name = 'Phases'
        self.sample.phases = crystals
        self.interface.generate_sample_binding("filename", self.sample)
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.currentPhaseSitesChanged.emit()

    @Property(str, notify=phasesChanged)
    def phasesAsXml(self):
        phases = self.sample.phases.as_dict()['data']
        xml = dicttoxml(phases, attr_type=True)
        xml = xml.decode()
        return xml

    @Property(str, notify=phasesChanged)
    def phasesAsCif(self):
        cif = str(self.sample.phases.cif)
        return cif

    @phasesAsCif.setter
    def setPhasesAsCif(self, cif_str):
       # print("Set phases from GUI cif string")
       self.phases = Crystals.from_cif_str(cif_str)
       self.sample.phases = self.phases
       self.updateCalculatedData()
       self.phasesChanged.emit()
       self.currentPhaseSitesChanged.emit()

    @Property('QVariant', notify=currentPhaseSitesChanged)
    def currentPhaseAllSites(self):
        all_sites = self.sample.phases[0].all_sites()
        # convert numpy lists to python lists for qml
        all_sites = { k: all_sites[k].tolist() for k in all_sites.keys() }
        return all_sites

    @Property(int, notify=currentPhaseChanged)
    def currentPhaseIndex(self):
        return self._current_phase_index

    @currentPhaseIndex.setter
    def setCurrentPhaseIndex(self, index: int):
        self._current_phase_index = index
        self.phasesChanged.emit()
        self.updateCalculatedData()
        self.currentPhaseChanged.emit()

    # Space groups

    @Property('QVariant', notify=phasesChanged)
    def spaceGroupsSystems(self):
        return SpacegroupInfo.get_all_systems()

    @Slot(result='QVariant')
    def spaceGroupsInts(self, system: str):
        ints = SpacegroupInfo.get_ints_from_system(system)
        out_list = ['{}  {:s}'.format(this_int, SpacegroupInfo.get_symbol_from_int_number(this_int)) for this_int in ints]
        print('HEllo THeres')
        print(out_list)
        return out_list

    @Slot(result='QVariant')
    def spaceGroupsOpts(self, system_int: int):
        opts = SpacegroupInfo.get_compatible_HM_from_int(system_int)
        return opts

    @Property('QVariant', notify=phasesChanged)
    def spaceGroups(self):
        return sgs

    # Fitables

    def _fitablesList(self):
        fitables_list = []
        pars_id, pars_path = generatePath(self.sample, True)
        for index, par_path in enumerate(pars_path):
            id = pars_id[index]
            par = borg.map.get_item_by_key(id)
            fitables_list.append(
                {"id": str(id),
                 "number": index + 1,
                 "label":  par_path,
                 "value":  par.raw_value,
                 "unit":   '{:~P}'.format(par.unit),
                 "error":  par.error,
                 "fit":    int(not par.fixed)}
            )
        return fitables_list

    @Property(str, notify=modelChanged)
    def fitablesListAsXml(self):
        xml = dicttoxml(self._fitablesList(), attr_type=False)
        xml = xml.decode()
        return xml

    # Edit parameter or descriptor

    def _editValue(self, obj_id, new_value):
        if not obj_id:
            return
        obj_id = int(obj_id)
        obj = borg.map.get_item_by_key(obj_id)
        obj.value = new_value
        self.phasesChanged.emit()
        self.updateCalculatedData()

    @Slot(str, float)
    def editParameterValue(self, obj_id: str, new_value: float):
        self._editValue(obj_id, new_value)

    @Slot(str, str)
    def editDescriptorValue(self, obj_id: str, new_value: str):
        self._editValue(obj_id, new_value)

    # Utils

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
