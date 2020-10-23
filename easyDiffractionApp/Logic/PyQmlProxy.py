import sys
import os
import json
from dicttoxml import dicttoxml
from urllib.parse import urlparse

from PySide2.QtCore import QObject, Slot, Signal, Property

from easyCore import np
from easyCore import borg
# borg.debug = True

from easyCore.Symmetry.tools import SpacegroupInfo
from easyCore.Fitting.Fitting import Fitter
from easyCore.Fitting.Constraints import ObjConstraint, NumericConstraint
from easyCore.Utils.classTools import generatePath
from easyDiffractionApp.Logic.DataStore import DataSet1D

from easyDiffractionLib.sample import Sample
from easyDiffractionLib import Crystals, Crystal, Cell, Site, Atoms, SpaceGroup
from easyDiffractionLib.interface import InterfaceFactory
from easyDiffractionLib.Elements.Instruments.Instrument import Pattern

from easyDiffractionApp.Logic.MatplotlibBackend import DisplayBridge


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
    spaceGroupChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface = InterfaceFactory()

        self.sample = Sample(parameters=Pattern.default(), interface=self.interface)
        self.sample.parameters.u_resolution=0.4
        self.sample.parameters.v_resolution=-0.5
        self.sample.parameters.w_resolution=0.9
        self.sample.parameters.x_resolution=0.0
        self.sample.parameters.y_resolution=0.0
        x_data = np.linspace(5, 150, 1000)
        self.bridge.data.x_label = '2theta (deg)'
        self.bridge.data.y_label = 'Intensity (arb. units)'
        self.bridge.data.append(
            DataSet1D(name='Simulator {:s}'.format(self.interface.current_interface_name),
                      x=x_data, y=np.zeros_like(x_data))
        )
        self.data = self.bridge.data[0]

        self.project_info = self.initProjectInfo()
        self._current_phase_index = 0

        # when to emit status bar items cnahged
        self.calculatorChanged.connect(self.statusChanged)
        self.minimizerChanged.connect(self.statusChanged)

    # Calculated data

    @Slot()
    def updateCalculatedData(self):
        self.sample.output_index = self.currentPhaseIndex
        self.data.y = self.interface.fit_func(self.data.x)
        self.bridge.updateWithCanvas('figure')
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
        self.data.name = 'Simulator {:s}'.format(self.interface.current_interface_name)
        self.sample._updateInterface()
        self.updateCalculatedData()
        self.calculatorChanged.emit()

    # Charts

    # @Slot(QtCharts.QXYSeries)
    # def addMeasuredSeriesRef(self, series):
    #     self._measured_data_model.addSeriesRef(series)
    #
    # @Slot(QtCharts.QXYSeries)
    # def addLowerMeasuredSeriesRef(self, series):
    #     self._measured_data_model.addLowerSeriesRef(series)
    #
    # @Slot(QtCharts.QXYSeries)
    # def addUpperMeasuredSeriesRef(self, series):
    #     self._measured_data_model.addUpperSeriesRef(series)
    #
    # @Slot(QtCharts.QXYSeries)
    # def setCalculatedSeriesRef(self, series):
    #     self._calculated_data_model.setSeriesRef(series)

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
    def phaseList(self):
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
        self.currentPhaseChanged.emit()
        self.currentPhaseSitesChanged.emit()
        self.spaceGroupChanged.emit()

    @Slot()
    def addSampleManual(self):
        cell = Cell.from_pars(8.56, 8.56, 6.12, 90, 90, 90)
        spacegroup = SpaceGroup.from_pars('P 42/n c m')
        atom = Site.from_pars(label='Cl1', specie='Cl', fract_x=0.125, fract_y=0.167, fract_z=0.107)
        atom.add_adp('Uiso', Uiso=0.0)
        crystal = Crystal('Dichlorine', spacegroup=spacegroup, cell=cell)
        crystal.add_atom(atom)
        self.sample.phases = crystal
        self.sample.phases.name = 'Phases'
        self.interface.generate_sample_binding("filename", self.sample)
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.currentPhaseChanged.emit()
        self.currentPhaseSitesChanged.emit()
        self.spaceGroupChanged.emit()

    @Slot(str)
    def removePhase(self, phase_name: str):
        del self.sample.phases[phase_name]
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.currentPhaseChanged.emit()
        self.currentPhaseSitesChanged.emit()
        self.spaceGroupChanged.emit()

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
       self.phases = Crystals.from_cif_str(cif_str)
       self.sample.phases = self.phases
       self.updateCalculatedData()
       self.phasesChanged.emit()
       self.currentPhaseChanged.emit()
       self.currentPhaseSitesChanged.emit()
       self.spaceGroupChanged.emit()

    @Slot(str)
    def modifyPhaseName(self, new_value: str):
        self.sample.phases[self.currentPhaseIndex].name = new_value
        self.phasesChanged.emit()

    @Property('QVariant', notify=currentPhaseSitesChanged)
    def currentPhaseAllSites(self):
        if not self.sample.phases:
            return {}
        all_sites = self.sample.phases[0].all_sites()
        # convert numpy lists to python lists for qml
        all_sites = { k: all_sites[k].tolist() for k in all_sites.keys() }
        return all_sites

    @Property(int, notify=currentPhaseChanged)
    def currentPhaseIndex(self):
        return self._current_phase_index

    @currentPhaseIndex.setter
    def setCurrentPhaseIndex(self, index: int):
        if index == -1:
            return
        self._current_phase_index = index
        self.phasesChanged.emit()
        self.updateCalculatedData()
        self.currentPhaseChanged.emit()

    # Space groups

    @Property('QVariant', notify=spaceGroupChanged)
    def spaceGroupsSystems(self):
        return [group[0].upper() + group[1:] for group in SpacegroupInfo.get_all_systems()]

    @Property(str, notify=spaceGroupChanged)
    def spaceGroupSystem(self):
        if len(self.sample.phases) == 0:
            return ''
        system = self.sample.phases[self.currentPhaseIndex].spacegroup.crystal_system
        return system[0].upper() + system[1:]

    @spaceGroupSystem.setter
    def setSpaceGroupSystem(self, new_system: str):
        ints = SpacegroupInfo.get_ints_from_system(new_system.lower())
        name = SpacegroupInfo.get_symbol_from_int_number(ints[0])
        self._setCurrentSpaceGroup(name)

    ##

    @Property('QVariant', notify=spaceGroupChanged)
    def spaceGroupsInts(self):
        ints = SpacegroupInfo.get_ints_from_system(self.spaceGroupSystem.lower())
        out_list = ["<font color='#999'>{}</font> {:s}".format(this_int, SpacegroupInfo.get_symbol_from_int_number(this_int)) for this_int in ints]
        out = {'display': out_list, 'index': ints }
        return out
        #ints = SpacegroupInfo.get_ints_from_system(self.spaceGroupSystem)
        #out_list = ["<font color='#999'>{}</font> {:s}".format(this_int, SpacegroupInfo.get_symbol_from_int_number(this_int)) for this_int in ints]
        #display_list =  ["<font color='#999'>{}</font> {:s}".format(i, value) for i, value in enumerate(self._currentSpaceGroupSettingList())]
        #return out

    @Property(int, notify=spaceGroupChanged)
    def spaceGroupInt(self):
        if len(self.sample.phases) == 0:
            return -1
        this_int = self.sample.phases[self.currentPhaseIndex].spacegroup.int_number
        idx = 0
        ints: list = self.spaceGroupsInts['index']
        if this_int in ints:
            idx = ints.index(this_int)
        return idx

    @spaceGroupInt.setter
    def setSpaceGroupInt(self, idx: int):
        ints: list = self.spaceGroupsInts['index']
        name = SpacegroupInfo.get_symbol_from_int_number(ints[idx])
        self._setCurrentSpaceGroup(name)

    ## Setting

    def _currentSpaceGroupSettingList(self):
        if len(self.sample.phases) == 0:
            return []
        space_group_index = self.sample.phases[self.currentPhaseIndex].spacegroup.int_number
        setting_list = SpacegroupInfo.get_compatible_HM_from_int(space_group_index)
        return setting_list

    @Property('QVariant', notify=spaceGroupChanged)
    def currentSpaceGroupSettingList(self):
        display_list =  ["<font color='#999'>{}</font> {:s}".format(i+1, value) for i, value in enumerate(self._currentSpaceGroupSettingList())]
        return display_list

    @Property(int, notify=spaceGroupChanged)
    def curentSpaceGroupSettingIndex(self):
        if len(self.sample.phases) == 0:
            return 0
        setting = self.sample.phases[self.currentPhaseIndex].spacegroup.space_group_HM_name.raw_value
        i = self._currentSpaceGroupSettingList().index(setting)
        return i

    @curentSpaceGroupSettingIndex.setter
    def setCurrentSpaceGroupSettingIndex(self, i: int):
        name = self._currentSpaceGroupSettingList()[i]
        self._setCurrentSpaceGroup(name)

    ##

    def _setCurrentSpaceGroup(self, name: str):
        self.sample.phases[self.currentPhaseIndex].spacegroup.space_group_HM_name = name
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.currentPhaseChanged.emit()
        self.currentPhaseSitesChanged.emit()
        self.spaceGroupChanged.emit()

    # Atoms
    @Slot(str)
    def removeAtom(self, atom_label: str):
        del self.sample.phases[self.currentPhaseIndex].atoms[atom_label]
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.currentPhaseChanged.emit()
        self.currentPhaseSitesChanged.emit()

    @Slot()
    def addAtom(self):
        try:
            atom = Site.default('Label2', 'H')
            atom.add_adp('Uiso', Uiso=0.0)
            self.sample.phases[self.currentPhaseIndex].add_atom(atom)

        except AttributeError:
            return
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.currentPhaseChanged.emit()
        self.currentPhaseSitesChanged.emit()

    # Fitables

    def _fitablesList(self):
        fitables_list = []
        pars_id, pars_path = generatePath(self.sample, True)
        for index, par_path in enumerate(pars_path):
            id = pars_id[index]
            par = borg.map.get_item_by_key(id)
            if not par.enabled:
                continue
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
