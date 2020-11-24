import json
from dicttoxml import dicttoxml

from PySide2.QtCore import QObject, Slot, Signal, Property

from easyCore import np
from easyCore import borg
# borg.debug = True

from easyCore.Symmetry.tools import SpacegroupInfo
from easyCore.Fitting.Fitting import Fitter
from easyCore.Fitting.Constraints import ObjConstraint, NumericConstraint
from easyCore.Utils.classTools import generatePath
from easyDiffractionLib.Elements.Backgrounds.Point import PointBackground, BackgroundPoint

from easyDiffractionLib.sample import Sample
from easyDiffractionLib import Phases, Phase, Lattice, Site, Atoms, SpaceGroup
from easyDiffractionLib.interface import InterfaceFactory
from easyDiffractionLib.Elements.Experiments.Experiment import Pars1D
from easyDiffractionLib.Elements.Experiments.Pattern import Pattern1D

from easyAppLogic.Utils.Utils import generalizePath

from easyDiffractionApp.Logic.DataStore import DataSet1D, DataStore
from easyDiffractionApp.Logic.MatplotlibBackend import DisplayBridge


class PyQmlProxy(QObject):
    _borg = borg

    matplotlib_bridge = DisplayBridge()

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
    backgroundChanged = Signal()
    instrumentResolutionChanged = Signal()
    experimentDataChanged = Signal()

    parameterChanged = Signal()
    fitResultsChanged = Signal()
    experimentLoadedChanged = Signal()
    simulationParametersChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.experiments = []
        self.interface = InterfaceFactory()
        self.vtkHandler = None
        self.sample = Sample(parameters=Pars1D.default(), pattern=Pattern1D.default(), interface=self.interface)
        self.sample.pattern.zero_shift = 0.0
        self.sample.pattern.scale = 1.0
        self.sample.parameters.wavelength = 1.912
        self.sample.parameters.resolution_u = 0.14
        self.sample.parameters.resolution_v = -0.42
        self.sample.parameters.resolution_w = 0.38
        self.sample.parameters.resolution_x = 0.0
        self.sample.parameters.resolution_y = 0.0

        #self.background = PointBackground(linked_experiment='NEED_TO_CHANGE')
        self.background = PointBackground(BackgroundPoint.from_pars(0, 200), BackgroundPoint.from_pars(140, 200), linked_experiment='NEED_TO_CHANGE')

        self._simulation_parameters = { "x_min": 10.0, "x_max": 150.0, "x_step": 0.1 }
        x_min = self._simulation_parameters['x_min']
        x_max = self._simulation_parameters['x_max']
        x_step = self._simulation_parameters['x_step']
        num_points = int((x_max - x_min) / x_step + 1)
        x_data = np.linspace(x_min, x_max, num_points)
        self.data = DataStore()
        self.data.append(
            DataSet1D(name='D1A@ILL data',
                      x=x_data, y=np.zeros_like(x_data),
                      x_label='2theta (deg)', y_label='Intensity (arb. units)',
                      data_type='experiment')
        )
        self.data.append(
            DataSet1D(name='{:s} engine'.format(self.interface.current_interface_name),
                      x=x_data, y=np.zeros_like(x_data),
                      x_label='2theta (deg)', y_label='Intensity (arb. units)',
                      data_type='simulation')
        )
        self.project_info = self.initProjectInfo()
        self._current_phase_index = 0
        self._fitables_list = []
        self._filter_criteria = ""

        self._experiment_figure_obj_name = None
        self._analysis_figure_obj_name = None

        self._fit_results = { "success": None, "nvarys": None, "GOF": None, "redchi": None }
        self._experiment_loaded = False

        self.fitter = Fitter(self.sample, self.interface.fit_func)

        # when to emit status bar items cnahged
        self.calculatorChanged.connect(self.statusChanged)
        self.minimizerChanged.connect(self.statusChanged)
        self.parameterChanged.connect(self.experimentDataChanged)

        #
        #self.experimentLoadedChanged.connect(self.onExperimentLoaded)
        self.simulationParametersChanged.connect(self.onSimulationParametersChanged)

        # Create a connection between this signal and a receiver, the receiver can be a Python callable, a Slot or a
        # Signal. But why does it not work :-(
        # self.phaseChanged.connect(self.updateStructureView)
        # self.currentPhaseChanged.connect(self.updateStructureView)

    # Structure view

    @Property(bool, notify=False)
    def showBonds(self):
        if self.vtkHandler is None:
            return True
        return self.vtkHandler.show_bonds

    @showBonds.setter
    def setShowBonds(self, show_bonds: bool):
        if self.vtkHandler is None:
            return
        self.vtkHandler.show_bonds = show_bonds
        self.updateStructureView()

    @Property(float, notify=False)
    def maxDistance(self):
        if self.vtkHandler is None:
            return 2.0
        return self.vtkHandler.max_distance

    @maxDistance.setter
    def setMaxDistance(self, max_distance: float):
        if self.vtkHandler is None:
            return
        self.vtkHandler.max_distance = max_distance
        self.updateStructureView()

    def updateStructureView(self):
        if self.vtkHandler is None or len(self.sample.phases) == 0:
            return
        self.vtkHandler.clearScene()
        self.vtkHandler.plot_system2(self.sample.phases[0])

    # Experimental data

    @Property(str, notify=experimentDataChanged)
    def experimentDataAsXml(self):
        xml = dicttoxml(self.experiments, attr_type=False)
        xml = xml.decode()
        return xml

    @Slot(str)
    def loadExperimentDataFromTxt(self, file_path):
        file_path = generalizePath(file_path)
        print(f"Load data from: {file_path}")
        #print("---1---self.simulationParameters", self._simulation_parameters)
        data = self.data.experiments[0]
        data.x, data.y, data.e = np.loadtxt(file_path, unpack=True)
        x_min = data.x[0]
        x_max = data.x[-1]
        x_step = (x_max - x_min) / (len(data.x) - 1)
        self.simulationParameters = json.dumps({ "x_min": x_min, "x_max": x_max, "x_step": x_step })
        #print("---2---self.simulationParameters", self._simulation_parameters)
        self.matplotlib_bridge.updateWithCanvas(self._experiment_figure_obj_name, data)
        self.experiments = [{"label": "D1A@ILL", "color": "steelblue"}]
        self.experimentDataChanged.emit()
        self.updateCalculatedData()

    def createFakeExperiment(self):
        self.experiments = [{"label": "D2B_300K", "color": "steelblue"}]
        data = self.data.experiments
        data = data[0]
        #  Of course this needs to change........
        self._currentModel = Sample.from_dict(self.sample.as_dict(skip=['interface']))
        pbg = PointBackground(linked_experiment='NEED_TO_CHANGE')
        from random import random
        ran_p = lambda r: min(data.x) + r*(max(data.x) - min(data.x))
        pbg.append(BackgroundPoint.from_pars(ran_p(random()), 10000 * random()))
        pbg.append(BackgroundPoint.from_pars(ran_p(random()), 10000 * random()))
        pbg.append(BackgroundPoint.from_pars(ran_p(random()), 10000 * random()))
        self._currentModel._pattern.backgrounds[0] = pbg
        interface_f = InterfaceFactory()
        self._currentModel.interface = interface_f
        self._currentModel._updateInterface()
        data.y = interface_f.fit_func(data.x)
        self.bridge.updateWithCanvas('figureEXP', data)
        self.experimentDataChanged.emit()

    @Property(bool, notify=experimentLoadedChanged)
    def experimentLoaded(self):
        return self._experiment_loaded

    @experimentLoaded.setter
    def setExperimentLoaded(self, experiment_loaded: bool):
        if self._experiment_loaded == experiment_loaded:
            return
        self._experiment_loaded = experiment_loaded
        self.experimentLoadedChanged.emit()

    def onExperimentLoaded(self):
        print("-onExperimentLoaded-")
        #if not self._experiment_loaded:
        #    return
        #exp = self.data.experiments[0]
        #sim = self.data.simulations[0]
        #sim.x = exp.x
        #sim.y = self.interface.fit_func(sim.x)
        #self.matplotlib_bridge.updateWithCanvas(self._analysis_figure_obj_name, [exp, sim])
        #else:
        #    self.matplotlib_bridge.updateWithCanvas(self._analysis_figure_obj_name, data)

    # Pattern parameters

    @Property('QVariant', notify=simulationParametersChanged)
    def simulationParameters(self):
        return self._simulation_parameters

    @simulationParameters.setter
    def setSimulationParameters(self, json_str):
        self._simulation_parameters = json.loads(json_str)
        self.simulationParametersChanged.emit()

    def onSimulationParametersChanged(self):
        #print("------------ self._simulation_parameters", self._simulation_parameters)
        x_min = float(self._simulation_parameters['x_min'])
        x_max = float(self._simulation_parameters['x_max'])
        x_step = float(self._simulation_parameters['x_step'])
        num_points = int((x_max - x_min) / x_step + 1)
        sim = self.data.simulations[0]
        sim.x = np.linspace(x_min, x_max, num_points)
        sim.y = self.interface.fit_func(sim.x)
        self.updateCalculatedData()

    # Pattern parameters

    @Property('QVariant', notify=experimentDataChanged)
    def patternParameters(self):
        parameters = self.sample.pattern.as_dict()
        return parameters

    # Instrument parameters

    @Property('QVariant', notify=experimentDataChanged)
    def instrumentParameters(self):
        parameters = self.sample.parameters.as_dict()
        return parameters

    @Property(str, notify=experimentDataChanged)
    def instrumentParametersAsXml(self):
        parameters = [self.sample.parameters.as_dict()]
        xml = dicttoxml(parameters, attr_type=False)
        xml = xml.decode()
        return xml

    # Calculated data

    @Slot()
    def updateCalculatedData(self):
        if self._analysis_figure_obj_name is None:
            return
        self.sample.output_index = self.currentPhaseIndex
        #  THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        sim = self.data.simulations[0]
        if self.experimentLoaded:
            exp = self.data.experiments[0]
            sim.x = exp.x
            sim.y = self.interface.fit_func(sim.x)
            data = [exp, sim]
        else:
            zeros = DataSet1D(name='',
                              x_label='2theta (deg)', y_label='Intensity (arb. units)',
                              x=[sim.x[0]], y=[sim.y[0]])  # Temp solution to have proper color for sim curve
            x_min = float(self._simulation_parameters['x_min'])
            x_max = float(self._simulation_parameters['x_max'])
            x_step = float(self._simulation_parameters['x_step'])
            num_points = int((x_max - x_min) / x_step + 1)
            sim.x = np.linspace(x_min, x_max, num_points)
            sim.y = self.interface.fit_func(sim.x)
            data = [zeros, sim]
        self.matplotlib_bridge.updateWithCanvas(self._analysis_figure_obj_name, data)
        self.modelChanged.emit()

    # Minimizer

    @Property('QVariant', notify=minimizerChanged)
    def minimizerList(self):
        return self.fitter.available_engines

    @Property(int, notify=minimizerChanged)
    def minimizerIndex(self):
        return self.minimizerList.index(self.fitter.current_engine.name)

    @minimizerIndex.setter
    def setMinimizer(self, index: int):
        self.fitter.switch_engine(self.minimizerList[index])
        self.minimizerChanged.emit()

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
        data = self.data.simulations
        #  THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        data = data[0]
        data.name = '{:s} engine'.format(self.interface.current_interface_name)
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

    @Slot(str)
    def setExperimentFigureObjName(self, name):
        if self._experiment_figure_obj_name == name:
            return
        self._experiment_figure_obj_name = name

    @Slot(str)
    def setAnalysisFigureObjName(self, name):
        if self._analysis_figure_obj_name == name:
            return
        self._analysis_figure_obj_name = name

    # Status

    @Property(str, notify=statusChanged)
    def statusModelAsXml(self):
        items = [{"label": "Engine", "value": self.interface.current_interface_name},
                 {"label": "Minimizer", "value": self.fitter.current_engine.name}]
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

    def _onSampleAdded(self):
        if self.interface.current_interface_name != 'CrysPy':
            self.interface.generate_sample_binding("filename", self.sample)
        # self.vtkHandler.plot_system2(self.sample.phases[0])
        self.sample.set_background(self.background)
        self.updateStructureView()
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.currentPhaseChanged.emit()
        self.currentPhaseSitesChanged.emit()
        self.spaceGroupChanged.emit()

    @Slot(str)
    def addSampleFromCif(self, cif_path):
        cif_path = generalizePath(cif_path)
        crystals = Phases.from_cif_file(cif_path)
        crystals.name = 'Phases'
        self.sample.phases = crystals
        self.sample.set_background(self.background)
        self._onSampleAdded()

    @Slot()
    def addSampleManual(self):
        cell = Lattice.from_pars(8.56, 8.56, 6.12, 90, 90, 90)
        spacegroup = SpaceGroup.from_pars('P 42/n c m')
        atom = Site.from_pars(label='Cl1', specie='Cl', fract_x=0.125, fract_y=0.167, fract_z=0.107)
        atom.add_adp('Uiso', Uiso=0.0)
        crystal = Phase('Dichlorine', spacegroup=spacegroup, cell=cell)
        crystal.add_atom(atom)
        self.sample.phases = crystal
        self.sample.phases.name = 'Phases'
        self._onSampleAdded()

    @Slot(str)
    def removePhase(self, phase_name: str):
        del self.sample.phases[phase_name]
        # self.vtkHandler.clearScene()
        self.updateStructureView()
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
        self.phases = Phases.from_cif_str(cif_str)
        self.sample.phases = self.phases
        self.updateStructureView()
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
        all_sites = {k: all_sites[k].tolist() for k in all_sites.keys()}
        return all_sites

    @Property(int, notify=currentPhaseChanged)
    def currentPhaseIndex(self):
        return self._current_phase_index

    @currentPhaseIndex.setter
    def setCurrentPhaseIndex(self, index: int):
        if index == -1:
            return
        self._current_phase_index = index
        self.updateStructureView()
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.currentPhaseChanged.emit()

    # Peak profile

    @Property(str, notify=instrumentResolutionChanged)
    def instrumentResolutionAsXml(self):
        instrument_resolution = [{"U": 11.3, "V": -2.9, "W": 1.1, "X": 0.0, "Y": 0.0}]
        xml = dicttoxml(instrument_resolution, attr_type=False)
        xml = xml.decode()
        return xml

    # Background

    @Property(str, notify=backgroundChanged)
    def backgroundAsXml(self):
        background = np.array([item.as_dict() for item in self.background])
        idx = np.array([item.x.raw_value for item in self.background]).argsort()
        xml = dicttoxml(background[idx], attr_type=False)
        xml = xml.decode()
        return xml

    @Slot(str)
    def removeBackgroundPoint(self, background_point_x_name: str):
        print(f"removeBackgroundPoint for background_point_x_name: {background_point_x_name}")
        self.sample.remove_background(self.background)
        names = self.background.names
        del self.background[names.index(background_point_x_name)]
        self.sample.set_background(self.background)
        self.backgroundChanged.emit()
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.modelChanged.emit()

    @Slot()
    def addBackgroundPoint(self):
        print(f"addBackgroundPoint")
        self.sample.remove_background(self.background)
        point = BackgroundPoint.from_pars(x=180.0, y=0.0)
        self.background.append(point)
        self.sample.set_background(self.background)
        self.backgroundChanged.emit()
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.modelChanged.emit()

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
        out_list = [
            "<font color='#999'>{}</font> {:s}".format(this_int, SpacegroupInfo.get_symbol_from_int_number(this_int))
            for this_int in ints]
        out = {'display': out_list, 'index': ints}
        return out
        # ints = SpacegroupInfo.get_ints_from_system(self.spaceGroupSystem)
        # out_list = ["<font color='#999'>{}</font> {:s}".format(this_int, SpacegroupInfo.get_symbol_from_int_number(
        # this_int)) for this_int in ints]
        # display_list =  ["<font color='#999'>{}</font> {:s}".format(i, value) for i, value in enumerate(
        # self._currentSpaceGroupSettingList())]
        # return out

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
        display_list = ["<font color='#999'>{}</font> {:s}".format(i + 1, value) for i, value in
                        enumerate(self._currentSpaceGroupSettingList())]
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
        self.updateStructureView()
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.currentPhaseChanged.emit()
        self.currentPhaseSitesChanged.emit()
        self.spaceGroupChanged.emit()

    # Atoms

    @Slot(str)
    def removeAtom(self, atom_label: str):
        del self.sample.phases[self.currentPhaseIndex].atoms[atom_label]
        self.updateStructureView()
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
        self.updateStructureView()
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.currentPhaseChanged.emit()
        self.currentPhaseSitesChanged.emit()

    # Fitables

    def _setFitablesList(self):
        self._fitables_list = []
        pars_id, pars_path = generatePath(self.sample, True)
        for index, par_path in enumerate(pars_path):
            id = pars_id[index]
            par = borg.map.get_item_by_key(id)
            if not par.enabled:
                continue
            if self._filter_criteria.lower() not in par_path.lower():
                continue
            self._fitables_list.append(
                {"id":     str(id),
                 "number": index + 1,
                 "label":  par_path,
                 "value":  par.raw_value,
                 "unit":   '{:~P}'.format(par.unit),
                 "error":  par.error,
                 "fit":    int(not par.fixed)}
            )

    @Property(str, notify=modelChanged)
    def fitablesListAsXml(self):
        self._setFitablesList()
        xml = dicttoxml(self._fitables_list, attr_type=False)
        xml = xml.decode()
        return xml

    @Slot(str)
    def setFilterCriteria(self, filter_criteria):
        if self._filter_criteria == filter_criteria:
            return
        self._filter_criteria = filter_criteria
        self.modelChanged.emit()

    # Edit parameter or descriptor

    def _editValue(self, obj_id, new_value):
        if not obj_id:
            return
        obj_id = int(obj_id)
        obj = borg.map.get_item_by_key(obj_id)
        obj.value = new_value
        self.updateStructureView()
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.backgroundChanged.emit()

    @Slot(str, float)
    def editParameterValue(self, obj_id: str, new_value: float):
        self._editValue(obj_id, new_value)
        self.parameterChanged.emit()

    @Slot(str, bool)
    def editParameterFit(self, obj_id: str, new_value: bool):
        if not obj_id:
            return
        obj_id = int(obj_id)
        obj = borg.map.get_item_by_key(obj_id)
        obj.fixed = not new_value
        # self.updateStructureView()
        # self.updateCalculatedData()
        # self.phasesChanged.emit()
        # self.backgroundChanged.emit()
        self.parameterChanged.emit()

    @Slot(str, str)
    def editDescriptorValue(self, obj_id: str, new_value: str):
        self._editValue(obj_id, new_value)

    #

    @Slot(str)
    def fit(self, method: str):
        if not method:
            method = 'leastsq'
        exp_data = self.data.experiments[0]
        # result = f.fit(exp_data.x, exp_data.y, method='brute')
        # print(result)
        result = self.fitter.fit(exp_data.x, exp_data.y, weights=1/exp_data.e, method=method)
        self._fit_results = {"success": result.success,
                             "nvarys": len(result.p),
                             "gof": float(result.goodness_of_fit),
                             "redchi2": float(result.goodness_of_fit / (len(result.y_calc) - len(result.p)))}
        #print(f"self._fit_results 1: {self._fit_results}")
        self.fitResultsChanged.emit()
        self.updateStructureView()
        self.updateCalculatedData()
        self.phasesChanged.emit()
        self.backgroundChanged.emit()

    @Property('QVariant', notify=fitResultsChanged)
    def fitResults(self):
        #print(f"self._fit_results 2: {self._fit_results}")
        return self._fit_results