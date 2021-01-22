import json
from typing import Union

from dicttoxml import dicttoxml

import timeit

from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCore import QPointF
from PySide2.QtCharts import QtCharts

from easyCore import np
from easyCore import borg
# borg.debug = True

from easyCore.Symmetry.tools import SpacegroupInfo
from easyCore.Fitting.Fitting import Fitter
from easyCore.Fitting.Constraints import ObjConstraint, NumericConstraint
from easyCore.Utils.classTools import generatePath

from easyDiffractionLib.sample import Sample
from easyDiffractionLib import Phases, Phase, Lattice, Site, Atoms, SpaceGroup
from easyDiffractionLib.interface import InterfaceFactory
from easyDiffractionLib.Elements.Experiments.Experiment import Pars1D
from easyDiffractionLib.Elements.Experiments.Pattern import Pattern1D

from easyAppLogic.Utils.Utils import generalizePath

from easyDiffractionApp.Logic.DataStore import DataSet1D, DataStore

from easyDiffractionApp.Logic.Proxies.MatplotlibBackend import DisplayBridge
from easyDiffractionApp.Logic.Proxies.BackgroundProxy import BackgroundProxy
from easyDiffractionApp.Logic.Proxies.QtChartsBackend import QtChartsBridge


class PyQmlProxy(QObject):
    # SIGNALS

    # Project
    projectInfoChanged = Signal()

    # Fitables
    parametersChanged = Signal()
    parametersAsObjChanged = Signal()
    parametersAsXmlChanged = Signal()
    parametersFilterCriteriaChanged = Signal()

    # Structure
    structureParametersChanged = Signal()
    structureViewChanged = Signal()

    phaseAdded = Signal()
    phaseRemoved = Signal()
    phasesAsObjChanged = Signal()
    phasesAsXmlChanged = Signal()
    phasesAsCifChanged = Signal()
    currentPhaseChanged = Signal()

    # Experiment
    patternParametersChanged = Signal()
    patternParametersAsObjChanged = Signal()

    instrumentParametersChanged = Signal()
    instrumentParametersAsObjChanged = Signal()
    instrumentParametersAsXmlChanged = Signal()

    experimentDataAdded = Signal()
    experimentDataRemoved = Signal()
    experimentDataChanged = Signal()
    experimentDataAsXmlChanged = Signal()

    experimentLoadedChanged = Signal()
    experimentSkippedChanged = Signal()

    # Analysis
    calculatedDataChanged = Signal()

    simulationParametersChanged = Signal()

    fitFinished = Signal()
    fitResultsChanged = Signal()

    currentMinimizerChanged = Signal()
    currentMinimizerMethodChanged = Signal()

    currentCalculatorChanged = Signal()

    # Plotting
    showMeasuredSeriesChanged = Signal()
    showDifferenceChartChanged = Signal()
    current1dPlottingLibChanged = Signal()
    current3dPlottingLibChanged = Signal()

    # Status info
    statusInfoChanged = Signal()

    # METHODS

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main
        self._interface = InterfaceFactory()
        self._sample = self._defaultSample()

        # Charts
        self._vtk_handler = None

        self._qtcharts_bridge = QtChartsBridge()
        self._matplotlib_bridge = DisplayBridge()
        self._experiment_figure_canvas = None
        self._analysis_figure_canvas = None
        self._difference_figure_canvas = None

        self._calculated_series_ref = None

        self._show_measured_series = True
        self._show_difference_chart = True

        self.current1dPlottingLibChanged.connect(self.onCurrent1dPlottingLibChanged)
        self.current3dPlottingLibChanged.connect(self.onCurrent3dPlottingLibChanged)

        # Project
        self._project_info = self._defaultProjectInfo()

        # Structure
        self.structureParametersChanged.connect(self._onStructureParametersChanged)
        self.structureParametersChanged.connect(self._onStructureViewChanged)
        self.structureParametersChanged.connect(self._onCalculatedDataChanged)
        self.structureViewChanged.connect(self._onStructureViewChanged)

        self._phases_as_obj = []
        self._phases_as_xml = ""
        self._phases_as_cif = ""
        self.phaseAdded.connect(self._onPhaseAdded)
        self.phaseRemoved.connect(self._onPhaseRemoved)

        self._current_phase_index = 0
        self.currentPhaseChanged.connect(self._onCurrentPhaseChanged)

        # Experiment and calculated data
        self._data = self._defaultData()

        # Experiment
        self._pattern_parameters_as_obj = self._defaultPatternParameters()
        self.patternParametersChanged.connect(self._onPatternParametersChanged)

        self._instrument_parameters_as_obj = self._defaultInstrumentParameters()
        self._instrument_parameters_as_xml = ""
        self.instrumentParametersChanged.connect(self._onInstrumentParametersChanged)

        self._experiment_parameters = None
        self._experiment_data = None
        self._experiment_data_as_xml = ""
        self.experiments = self._defaultExperiments()
        self.experimentDataChanged.connect(self._onExperimentDataChanged)
        self.experimentDataAdded.connect(self._onExperimentDataAdded)
        self.experimentDataRemoved.connect(self._onExperimentDataRemoved)

        self._experiment_loaded = False
        self._experiment_skipped = False
        self.experimentLoadedChanged.connect(self._onExperimentLoadedChanged)
        self.experimentSkippedChanged.connect(self._onExperimentSkippedChanged)

        self._background_proxy = BackgroundProxy()
        self._background_proxy.asObjChanged.connect(self._onParametersChanged)
        self._background_proxy.asObjChanged.connect(self.calculatedDataChanged)
        self._background_proxy.asObjChanged.connect(self._sample.set_background)

        # Analysis
        self.calculatedDataChanged.connect(self._onCalculatedDataChanged)

        self._simulation_parameters_as_obj = self._defaultSimulationParameters()
        self.simulationParametersChanged.connect(self._onSimulationParametersChanged)

        self._fit_results = self._defaultFitResults()
        self.fitter = Fitter(self._sample, self._interface.fit_func)
        self.fitFinished.connect(self._onFitFinished)

        self._current_minimizer_method_index = 0
        self._current_minimizer_method_name = self.fitter.available_methods()[0]
        self.currentMinimizerChanged.connect(self._onCurrentMinimizerChanged)
        self.currentMinimizerMethodChanged.connect(self._onCurrentMinimizerMethodChanged)

        self.currentCalculatorChanged.connect(self._onCurrentCalculatorChanged)

        # Parameters
        self._parameters_as_obj = []
        self._parameters_as_xml = []
        self.parametersChanged.connect(self._onParametersChanged)
        self.parametersChanged.connect(self._onCalculatedDataChanged)
        self.parametersChanged.connect(self._onStructureViewChanged)
        self.parametersChanged.connect(self._onStructureParametersChanged)
        self.parametersChanged.connect(self._onPatternParametersChanged)
        self.parametersChanged.connect(self._onInstrumentParametersChanged)
        self.parametersChanged.connect(self._background_proxy.onAsObjChanged)

        self._parameters_filter_criteria = ""
        self.parametersFilterCriteriaChanged.connect(self._onParametersFilterCriteriaChanged)

        # Plotting
        self._1d_plotting_libs = ['matplotlib', 'qtcharts']
        self._current_1d_plotting_lib = self._1d_plotting_libs[0]

        self._3d_plotting_libs = ['vtk', 'qtdatavisualization']
        self._current_3d_plotting_lib = self._3d_plotting_libs[0]

        # Status info
        self.statusInfoChanged.connect(self._onStatusInfoChanged)
        self.currentCalculatorChanged.connect(self.statusInfoChanged)
        self.currentMinimizerChanged.connect(self.statusInfoChanged)
        self.currentMinimizerMethodChanged.connect(self.statusInfoChanged)

    ####################################################################################################################
    ####################################################################################################################
    # Charts
    ####################################################################################################################
    ####################################################################################################################

    # Vtk

    def setVtkHandler(self, vtk_handler):
        self._vtk_handler = vtk_handler

    @Property(bool, notify=False)
    def showBonds(self):
        if self._vtk_handler is None:
            return True
        return self._vtk_handler.show_bonds

    @showBonds.setter
    def showBondsSetter(self, show_bonds: bool):
        if self._vtk_handler is None or self._vtk_handler.show_bonds == show_bonds:
            return
        self._vtk_handler.show_bonds = show_bonds
        self.structureViewChanged.emit()

    @Property(float, notify=False)
    def bondsMaxDistance(self):
        if self._vtk_handler is None:
            return 2.0
        return self._vtk_handler.max_distance

    @bondsMaxDistance.setter
    def bondsMaxDistanceSetter(self, max_distance: float):
        if self._vtk_handler is None or self._vtk_handler.max_distance == max_distance:
            return
        self._vtk_handler.max_distance = max_distance
        self.structureViewChanged.emit()

    def _updateStructureView(self):
        start_time = timeit.default_timer()
        if self._vtk_handler is None or not self._sample.phases:
            return
        self._vtk_handler.clearScene()
        self._vtk_handler.plot_system2(self._sample.phases[0])
        print("+ _updateStructureView: {0:.3f} s".format(timeit.default_timer() - start_time))

    def _onStructureViewChanged(self):
        print("***** _onStructureViewChanged")
        self._updateStructureView()

    # Matplotlib

    @Property('QVariant', constant=True)
    def matplotlibBridge(self):
        return self._matplotlib_bridge

    @Slot('QVariant')
    def setExperimentFigureCanvas(self, canvas):
        if self._experiment_figure_canvas == canvas:
            return
        self._experiment_figure_canvas = canvas

    @Slot('QVariant')
    def setAnalysisFigureCanvas(self, canvas):
        if self._analysis_figure_canvas == canvas:
            return
        self._analysis_figure_canvas = canvas

    @Slot('QVariant')
    def setDifferenceFigureCanvas(self, canvas):
        if self._difference_figure_canvas == canvas:
            return
        self._difference_figure_canvas = canvas

    # QtCharts

    @Slot(QtCharts.QXYSeries)
    def setCalculatedSeriesRef(self, series_ref):
        self._calculated_series_ref = series_ref

    @Property('QVariant', constant=True)
    #@Property('QVariant', notify=phasesAsXmlChanged)
    def qtCharts(self):
        return self._qtcharts_bridge

    # Plotting libs

    @Property('QVariant', constant=True)
    def plotting1dLibs(self):
        return self._1d_plotting_libs

    @Property('QVariant', notify=current1dPlottingLibChanged)
    def current1dPlottingLib(self):
        return self._current_1d_plotting_lib

    @current1dPlottingLib.setter
    def current1dPlottingLibSetter(self, plotting_lib):
        self._current_1d_plotting_lib = plotting_lib
        self.current1dPlottingLibChanged.emit()

    def onCurrent1dPlottingLibChanged(self):
        if self.current1dPlottingLib == 'matplotlib':
            self._updateCalculatedData()
        elif self.current1dPlottingLib == 'qtcharts':
            self._qtcharts_bridge.updateAllCharts()

    @Property('QVariant', constant=True)
    def plotting3dLibs(self):
        return self._3d_plotting_libs

    @Property('QVariant', notify=current3dPlottingLibChanged)
    def current3dPlottingLib(self):
        return self._current_3d_plotting_lib

    @current3dPlottingLib.setter
    def current3dPlottingLibSetter(self, plotting_lib):
        self._current_3d_plotting_lib = plotting_lib
        self.current3dPlottingLibChanged.emit()

    def onCurrent3dPlottingLibChanged(self):
        if self.current3dPlottingLib == 'vtk':
            print("Warning: Select Vtk. Not implemented yet.")
        elif self.current3dPlottingLib == 'qtdatavisualization':
            print("Warning: Select Qt Data Visualization. Not implemented yet.")

    #

    @Property(bool, notify=showDifferenceChartChanged)
    def showDifferenceChart(self):
        return self._show_difference_chart

    @showDifferenceChart.setter
    def showDifferenceChartSetter(self, show):
        if self._show_difference_chart == show:
            return
        self._show_difference_chart = show
        self.showDifferenceChartChanged.emit()

    @Property(bool, notify=showMeasuredSeriesChanged)
    def showMeasuredSeries(self):
        return self._show_measured_series

    @showMeasuredSeries.setter
    def showMeasuredSeriesSetter(self, show):
        if self._show_measured_series == show:
            return
        self._show_measured_series = show
        self.showMeasuredSeriesChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # PROJECT
    ####################################################################################################################
    ####################################################################################################################

    ####################################################################################################################
    # Project
    ####################################################################################################################

    @Property('QVariant', notify=projectInfoChanged)
    def projectInfoAsJson(self):
        return self._project_info

    @projectInfoAsJson.setter
    def projectInfoAsJsonSetter(self, json_str):
        self._project_info = json.loads(json_str)
        self.projectInfoChanged.emit()

    @Slot(str, str)
    def editProjectInfo(self, key, value):
        if self._project_info[key] == value:
            return

        self._project_info[key] = value
        self.projectInfoChanged.emit()

    def _defaultProjectInfo(self):
        return dict(
            name="Example Project",
            keywords="diffraction, powder, 1D",
            samples="samples.cif",
            experiments="experiments.cif",
            calculations="calculation.cif",
            modified="18.09.2020, 09:24"
        )

    ####################################################################################################################
    ####################################################################################################################
    # SAMPLE
    ####################################################################################################################
    ####################################################################################################################

    def _defaultSample(self):
        sample = Sample(parameters=Pars1D.default(), pattern=Pattern1D.default(), interface=self._interface)
        sample.pattern.zero_shift = 0.0
        sample.pattern.scale = 1.0
        sample.parameters.wavelength = 1.912
        sample.parameters.resolution_u = 0.14
        sample.parameters.resolution_v = -0.42
        sample.parameters.resolution_w = 0.38
        sample.parameters.resolution_x = 0.0
        sample.parameters.resolution_y = 0.0
        return sample

    ####################################################################################################################
    # Phase models (list, xml, cif)
    ####################################################################################################################

    @Property('QVariant', notify=phasesAsObjChanged)
    def phasesAsObj(self):
        #print("+ phasesAsObj")
        return self._phases_as_obj

    @Property(str, notify=phasesAsXmlChanged)
    def phasesAsXml(self):
        #print("+ phasesAsXml")
        return self._phases_as_xml

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsCif(self):
        #print("+ phasesAsCif")
        return self._phases_as_cif

    @phasesAsCif.setter
    def phasesAsCifSetter(self, phases_as_cif):
        print("+ phasesAsCifSetter")
        if self._phases_as_cif == phases_as_cif:
            return

        self._sample.phases = Phases.from_cif_str(phases_as_cif)
        self.structureParametersChanged.emit()

    def _setPhasesAsObj(self):
        start_time = timeit.default_timer()
        self._phases_as_obj = self._sample.phases.as_dict()['data']
        print("+ _setPhasesAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsObjChanged.emit()

    def _setPhasesAsXml(self):
        start_time = timeit.default_timer()
        self._phases_as_xml = dicttoxml(self._phases_as_obj, attr_type=True).decode()
        print("+ _setPhasesAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsXmlChanged.emit()

    def _setPhasesAsCif(self):
        start_time = timeit.default_timer()
        self._phases_as_cif = str(self._sample.phases.cif)
        print("+ _setPhasesAsCif: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsCifChanged.emit()

    def _onStructureParametersChanged(self):
        print("***** _onStructureParametersChanged")
        self._setPhasesAsObj()  # 0.025 s
        self._setPhasesAsXml()  # 0.065 s
        self._setPhasesAsCif()  # 0.010 s

    ####################################################################################################################
    # Phase: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addSampleFromCif(self, cif_path):
        cif_path = generalizePath(cif_path)
        self._sample.phases = Phases.from_cif_file(cif_path)
        self.phaseAdded.emit()

    @Slot()
    def addDefaultPhase(self):
        print("+ addDefaultPhase")
        self._sample.phases = self._defaultPhase()
        self.phaseAdded.emit()

    @Slot(str)
    def removePhase(self, phase_name: str):
        if phase_name in self._sample.phases.phase_names:
            del self._sample.phases[phase_name]
            self.phaseRemoved.emit()

    def _defaultPhase(self):
        space_group = SpaceGroup.from_pars('P 42/n c m')
        cell = Lattice.from_pars(8.56, 8.56, 6.12, 90, 90, 90)
        atom = Site.from_pars(label='Cl1', specie='Cl', fract_x=0.125, fract_y=0.167, fract_z=0.107)
        atom.add_adp('Uiso', Uiso=0.0)
        phase = Phase('Dichlorine', spacegroup=space_group, cell=cell)
        phase.add_atom(atom)
        return phase

    def _onPhaseAdded(self):
        print("***** _onPhaseAdded")
        if self._interface.current_interface_name != 'CrysPy':
            self._interface.generate_sample_binding("filename", self._sample)
        self._sample.phases.name = 'Phases'
        self._sample.set_background(self._background_proxy.asObj)
        self.structureParametersChanged.emit()

    def _onPhaseRemoved(self):
        print("***** _onPhaseRemoved")
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Phase: Symmetry
    ####################################################################################################################

    # Crystal system

    @Property('QVariant', notify=structureParametersChanged)
    def crystalSystemList(self):
        systems = [system.capitalize() for system in SpacegroupInfo.get_all_systems()]
        return systems

    @Property(str, notify=structureParametersChanged)
    def currentCrystalSystem(self):
        phases = self._sample.phases
        if not phases:
            return ''

        current_system = phases[self.currentPhaseIndex].spacegroup.crystal_system
        current_system = current_system.capitalize()
        return current_system

    @currentCrystalSystem.setter
    def currentCrystalSystemSetter(self, new_system: str):
        new_system = new_system.lower()
        space_group_numbers = SpacegroupInfo.get_ints_from_system(new_system)
        top_space_group_number = space_group_numbers[0]
        top_space_group_name = SpacegroupInfo.get_symbol_from_int_number(top_space_group_number)
        self._setCurrentSpaceGroup(top_space_group_name)

    # Space group number and name

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupList(self):
        def format_display(num):
            name = SpacegroupInfo.get_symbol_from_int_number(num)
            return f"<font color='#999'>{num}</font> {name}"

        space_group_numbers = self._spaceGroupNumbers()
        display_list = [format_display(num) for num in space_group_numbers]
        return display_list

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroup(self):
        def space_group_index(number, numbers):
            if number in numbers:
                return numbers.index(number)
            return 0

        phases = self._sample.phases
        if not phases:
            return -1

        space_group_numbers = self._spaceGroupNumbers()
        current_number = self._currentSpaceGroupNumber()
        current_idx = space_group_index(current_number, space_group_numbers)
        return current_idx

    @currentSpaceGroup.setter
    def currentSpaceGroupSetter(self, new_idx: int):
        space_group_numbers = self._spaceGroupNumbers()
        space_group_number = space_group_numbers[new_idx]
        space_group_name = SpacegroupInfo.get_symbol_from_int_number(space_group_number)
        self._setCurrentSpaceGroup(space_group_name)

    def _spaceGroupNumbers(self):
        current_system = self.currentCrystalSystem.lower()
        numbers = SpacegroupInfo.get_ints_from_system(current_system)
        return numbers

    def _currentSpaceGroupNumber(self):
        phases = self._sample.phases
        current_number = phases[self.currentPhaseIndex].spacegroup.int_number
        return current_number

    # Space group setting

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupSettingList(self):
        def format_display(num, name):
            return f"<font color='#999'>{num}</font> {name}"

        raw_list = self._spaceGroupSettingList()
        formatted_list = [format_display(i+1, name) for i, name in enumerate(raw_list)]
        return formatted_list

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroupSetting(self):
        phases = self._sample.phases
        if not phases:
            return 0

        settings = self._spaceGroupSettingList()
        current_setting = phases[self.currentPhaseIndex].spacegroup.space_group_HM_name.raw_value
        current_number = settings.index(current_setting)
        return current_number

    @currentSpaceGroupSetting.setter
    def currentSpaceGroupSettingSetter(self, new_number: int):
        settings = self._spaceGroupSettingList()
        name = settings[new_number]
        self._setCurrentSpaceGroup(name)

    def _spaceGroupSettingList(self):
        phases = self._sample.phases
        if not phases:
            return []

        current_number = self._currentSpaceGroupNumber()
        settings = SpacegroupInfo.get_compatible_HM_from_int(current_number)
        return settings

    # Common

    def _setCurrentSpaceGroup(self, new_name: str):
        phases = self._sample.phases
        if phases[self.currentPhaseIndex].spacegroup.space_group_HM_name == new_name:
            return

        phases[self.currentPhaseIndex].spacegroup.space_group_HM_name = new_name
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Phase: Atoms
    ####################################################################################################################

    @Slot()
    def addDefaultAtom(self):
        try:
            atom = Site.default('Label2', 'H')
            atom.add_adp('Uiso', Uiso=0.0)
            self._sample.phases[self.currentPhaseIndex].add_atom(atom)
            self.structureParametersChanged.emit()
        except AttributeError:
            print("Error: failed to add atom")

    @Slot(str)
    def removeAtom(self, atom_label: str):
        del self._sample.phases[self.currentPhaseIndex].atoms[atom_label]
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Current phase
    ####################################################################################################################

    @Property(int, notify=currentPhaseChanged)
    def currentPhaseIndex(self):
        return self._current_phase_index

    @currentPhaseIndex.setter
    def currentPhaseIndexSetter(self, new_index: int):
        if self._current_phase_index == new_index or new_index == -1:
            return

        self._current_phase_index = new_index
        self.currentPhaseChanged.emit()

    def _onCurrentPhaseChanged(self):
        print("***** _onCurrentPhaseChanged")
        self.structureViewChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # EXPERIMENT
    ####################################################################################################################
    ####################################################################################################################

    def _defaultExperiments(self):
        return []

    def _defaultData(self):
        x_min = self._defaultSimulationParameters()['x_min']
        x_max = self._defaultSimulationParameters()['x_max']
        x_step = self._defaultSimulationParameters()['x_step']
        num_points = int((x_max - x_min) / x_step + 1)
        x_data = np.linspace(x_min, x_max, num_points)

        data = DataStore()

        data.append(
            DataSet1D(
                name='D1A@ILL data',
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Intensity',
                data_type='experiment'
            )
        )
        data.append(
            DataSet1D(
                name='{:s} engine'.format(self._interface.current_interface_name),
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Intensity',
                data_type='simulation'
            )
        )
        data.append(
            DataSet1D(
                name='Difference',
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Difference',
                data_type='simulation'
            )
        )
        return data

    ####################################################################################################################
    # Experiment models (list, xml, cif)
    ####################################################################################################################

    @Property(str, notify=experimentDataAsXmlChanged)
    def experimentDataAsXml(self):
        return self._experiment_data_as_xml

    def _setExperimentDataAsXml(self):
        print("+ _setExperimentDataAsXml")
        self._experiment_data_as_xml = dicttoxml(self.experiments, attr_type=True).decode()
        self.experimentDataAsXmlChanged.emit()

    def _onExperimentDataChanged(self):
        print("***** _onExperimentDataChanged")
        self._setExperimentDataAsXml()  # ? s

    ####################################################################################################################
    # Experiment data: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addExperimentDataFromXye(self, file_url):
        print(f"+ addExperimentDataFromXye: {file_url}")
        self._experiment_data = self._loadExperimentData(file_url)
        self.experimentDataAdded.emit()

    @Slot()
    def removeExperiment(self):
        print("+ removeExperiment")
        self.experiments.clear()
        self.experimentDataRemoved.emit()

    def _defaultExperiment(self):
        return {
            "label": "D1A@ILL",
            "color": "#00a3e3"
        }

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        file_path = generalizePath(file_url)
        data = self._data.experiments[0]
        data.x, data.y, data.e = np.loadtxt(file_path, unpack=True)
        return data

    def _experimentDataParameters(self, data):
        x_min = data.x[0]
        x_max = data.x[-1]
        x_step = (x_max - x_min) / (len(data.x) - 1)
        parameters = {
            "x_min": x_min,
            "x_max": x_max,
            "x_step": x_step
        }
        return parameters

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        if self.current1dPlottingLib == 'matplotlib':
            self._matplotlib_bridge.updateData(self._experiment_figure_canvas, [self._experiment_data])
        elif self.current1dPlottingLib == 'qtcharts':
            self._qtcharts_bridge.setMeasuredData(self._experiment_data.x, self._experiment_data.y, self._experiment_data.e)
        self._experiment_parameters = self._experimentDataParameters(self._experiment_data)
        self.simulationParametersAsObj = json.dumps(self._experiment_parameters)
        self.experiments = [self._defaultExperiment()]
        self._background_proxy.setDefaultPoints()
        self.experimentDataChanged.emit()

    def _onExperimentDataRemoved(self):
        print("***** _onExperimentDataRemoved")
        self._matplotlib_bridge.clearDispalyAdapters()
        self.experimentDataChanged.emit()

    ####################################################################################################################
    # Experiment loaded and skipped flags
    ####################################################################################################################

    @Property(bool, notify=experimentLoadedChanged)
    def experimentLoaded(self):
        return self._experiment_loaded

    @experimentLoaded.setter
    def experimentLoadedSetter(self, loaded: bool):
        if self._experiment_loaded == loaded:
            return

        self._experiment_loaded = loaded
        self.experimentLoadedChanged.emit()

    @Property(bool, notify=experimentSkippedChanged)
    def experimentSkipped(self):
        return self._experiment_skipped

    @experimentSkipped.setter
    def experimentSkippedSetter(self, skipped: bool):
        if self._experiment_skipped == skipped:
            return

        self._experiment_skipped = skipped
        self.experimentSkippedChanged.emit()

    def _onExperimentLoadedChanged(self):
        print("***** _onExperimentLoadedChanged")
        if self.experimentLoaded:
            self._onParametersChanged()
            self.instrumentParametersChanged.emit()
            self.patternParametersChanged.emit()

    def _onExperimentSkippedChanged(self):
        print("***** _onExperimentSkippedChanged")
        if self.experimentSkipped:
            self._onParametersChanged()
            self.instrumentParametersChanged.emit()
            self.patternParametersChanged.emit()
            self.calculatedDataChanged.emit()

    ####################################################################################################################
    # Simulation parameters
    ####################################################################################################################

    @Property('QVariant', notify=simulationParametersChanged)
    def simulationParametersAsObj(self):
        return self._simulation_parameters_as_obj

    @simulationParametersAsObj.setter
    def simulationParametersAsObjSetter(self, json_str):
        if self._simulation_parameters_as_obj == json.loads(json_str):
            return

        self._simulation_parameters_as_obj = json.loads(json_str)
        self.simulationParametersChanged.emit()

    def _defaultSimulationParameters(self):
        return {
            "x_min": 10.0,
            "x_max": 150.0,
            "x_step": 0.1
        }

    def _onSimulationParametersChanged(self):
        print("***** _onSimulationParametersChanged")
        self.calculatedDataChanged.emit()

    ####################################################################################################################
    # Pattern parameters (scale, zero_shift, backgrounds)
    ####################################################################################################################

    @Property('QVariant', notify=patternParametersAsObjChanged)
    def patternParametersAsObj(self):
        return self._pattern_parameters_as_obj

    def _defaultPatternParameters(self):
        return {
            "scale": 1.0,
            "zero_shift": 0.0
        }

    def _setPatternParametersAsObj(self):
        start_time = timeit.default_timer()
        parameters = self._sample.pattern.as_dict()
        self._pattern_parameters_as_obj = parameters
        print("+ _setPatternParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.patternParametersAsObjChanged.emit()

    def _onPatternParametersChanged(self):
        print("***** _onPatternParametersChanged")
        self._setPatternParametersAsObj()

    ####################################################################################################################
    # Instrument parameters (wavelength, resolution_u, ..., resolution_y)
    ####################################################################################################################

    @Property('QVariant', notify=instrumentParametersAsObjChanged)
    def instrumentParametersAsObj(self):
        return self._instrument_parameters_as_obj

    @Property(str, notify=instrumentParametersAsXmlChanged)
    def instrumentParametersAsXml(self):
        return self._instrument_parameters_as_xml

    def _defaultInstrumentParameters(self):
        return {
            "wavelength": 1.0,
            "resolution_u": 0.01,
            "resolution_v": -0.01,
            "resolution_w": 0.01,
            "resolution_x": 0.0,
            "resolution_y": 0.0
        }

    def _setInstrumentParametersAsObj(self):
        start_time = timeit.default_timer()
        parameters = self._sample.parameters.as_dict()
        self._instrument_parameters_as_obj = parameters
        print("+ _setInstrumentParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsObjChanged.emit()

    def _setInstrumentParametersAsXml(self):
        start_time = timeit.default_timer()
        parameters = [self._instrument_parameters_as_obj]
        self._instrument_parameters_as_xml = dicttoxml(parameters, attr_type=True).decode()
        print("+ _setInstrumentParametersAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsXmlChanged.emit()

    def _onInstrumentParametersChanged(self):
        print("***** _onInstrumentParametersChanged")
        self._setInstrumentParametersAsObj()
        self._setInstrumentParametersAsXml()

    ####################################################################################################################
    # Background
    ####################################################################################################################

    @Property('QVariant', constant=True)
    def backgroundProxy(self):
        return self._background_proxy

    ####################################################################################################################
    ####################################################################################################################
    # ANALYSIS
    ####################################################################################################################
    ####################################################################################################################

    ####################################################################################################################
    # Calculated data
    ####################################################################################################################

    def _updateCalculatedData(self):
        start_time = timeit.default_timer()

        if not self.experimentLoaded and not self.experimentSkipped:
            return

        if self.current1dPlottingLib == 'matplotlib' and self._analysis_figure_canvas is None:
            return

        if self.current1dPlottingLib == 'qtchart' and self._calculated_series_ref is None:
            return

        self._sample.output_index = self.currentPhaseIndex

        #  THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        sim = self._data.simulations[0]

        zeros_sim = DataSet1D(name='', x=[sim.x[0]], y=[sim.y[0]])  # Temp solution to have proper color for sim curve
        zeros_diff = DataSet1D(name='', x=[sim.x[0]])  # Temp solution to have proper color for sim curve

        if self.experimentLoaded:
            exp = self._data.experiments[0]

            sim.x = exp.x
            sim.y = self._interface.fit_func(sim.x)

            diff = self._data.simulations[1]
            diff.x = exp.x
            diff.y = exp.y - sim.y

            zeros_diff.y = [exp.y[0] - sim.y[0]]

            difference_dataset = [zeros_diff, zeros_diff, diff]
            analysis_dataset = [exp, sim]

            if self.current1dPlottingLib == 'matplotlib':
                self._matplotlib_bridge.updateData(self._difference_figure_canvas, difference_dataset)
######            elif self.current1dPlottingLib == 'qtcharts':
######                self._qtcharts_bridge.replacePoints('analysis.measured.lower', exp.x, exp.y - 100)
######                self._qtcharts_bridge.replacePoints('analysis.measured.upper', exp.x, exp.y + 100)
            #    self._qtcharts_bridge.replacePoints('analysis.difference.lower', diff.x, diff.y)
            #    self._qtcharts_bridge.replacePoints('analysis.difference.upper', diff.x, diff.y)

        elif self.experimentSkipped:
            x_min = float(self._simulation_parameters_as_obj['x_min'])
            x_max = float(self._simulation_parameters_as_obj['x_max'])
            x_step = float(self._simulation_parameters_as_obj['x_step'])
            num_points = int((x_max - x_min) / x_step + 1)

            sim.x = np.linspace(x_min, x_max, num_points)
            sim.y = self._interface.fit_func(sim.x)  # CrysPy: 0.5 s, CrysFML: 0.005 s, GSAS-II: 0.25 s

            analysis_dataset = [zeros_sim, sim]

        if self.current1dPlottingLib == 'matplotlib':
            self._matplotlib_bridge.updateData(self._analysis_figure_canvas, analysis_dataset)
        elif self.current1dPlottingLib == 'qtcharts':
            self._qtcharts_bridge.setCalculatedData(sim.x, sim.y)

        print("+ _updateCalculatedData: {0:.3f} s".format(timeit.default_timer() - start_time))

    def _onCalculatedDataChanged(self):
        print("***** _onCalculatedDataChanged")
        self._updateCalculatedData()

    ####################################################################################################################
    # Fitables (parameters table from analysis tab & ...)
    ####################################################################################################################

    @Property('QVariant', notify=parametersAsObjChanged)
    def parametersAsObj(self):
        #print("+ parametersAsObj")
        return self._parameters_as_obj

    @Property(str, notify=parametersAsXmlChanged)
    def parametersAsXml(self):
        #print("+ parametersAsXml")
        return self._parameters_as_xml

    def _setParametersAsObj(self):
        start_time = timeit.default_timer()
        self._parameters_as_obj.clear()

        par_ids, par_paths = generatePath(self._sample, True)
        for par_index, par_path in enumerate(par_paths):
            par_id = par_ids[par_index]
            par = borg.map.get_item_by_key(par_id)

            if not par.enabled:
                continue

            if self._parameters_filter_criteria.lower() not in par_path.lower():
                continue

            self._parameters_as_obj.append({
                "id": str(par_id),
                "number": par_index + 1,
                "label": par_path,
                "value": par.raw_value,
                "unit": '{:~P}'.format(par.unit),
                "error": par.error,
                "fit": int(not par.fixed)
            })

        print("+ _setParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsObjChanged.emit()

    def _setParametersAsXml(self):
        start_time = timeit.default_timer()
        # print(f" _setParametersAsObj self._parameters_as_obj id C {id(self._parameters_as_obj)}")
        self._parameters_as_xml = dicttoxml(self._parameters_as_obj, attr_type=False).decode()
        print("+ _setParametersAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsXmlChanged.emit()

    def _onParametersChanged(self):
        print("***** _onParametersChanged")
        self._setParametersAsObj()
        self._setParametersAsXml()

    # Filtering

    @Slot(str)
    def setParametersFilterCriteria(self, new_criteria):
        if self._parameters_filter_criteria == new_criteria:
            return
        self._parameters_filter_criteria = new_criteria
        self.parametersFilterCriteriaChanged.emit()

    def _onParametersFilterCriteriaChanged(self):
        print("***** _onParametersFilterCriteriaChanged")
        self._onParametersChanged()

    ####################################################################################################################
    # Any parameter
    ####################################################################################################################

    @Slot(str, 'QVariant')
    def editParameter(self, obj_id: str, new_value: Union[bool, float, str]):  # covers both parameter and descriptor
        obj = self._parameterObj(obj_id)
        print(f"\n\n+ editParameter {obj_id} of {type(new_value)} from {obj.raw_value} to {new_value}")

        if isinstance(new_value, bool):
            if obj.fixed == (not new_value):
                return

            obj.fixed = not new_value
            self._onParametersChanged()

        else:
            if obj.raw_value == new_value:
                return

            obj.value = new_value
            self.parametersChanged.emit()

    def _parameterObj(self, obj_id: str):
        if not obj_id:
            return
        obj_id = int(obj_id)
        obj = borg.map.get_item_by_key(obj_id)
        return obj

    ####################################################################################################################
    # Minimizer
    ####################################################################################################################

    # Minimizer

    @Property('QVariant', constant=True)
    def minimizerNames(self):
        return self.fitter.available_engines

    @Property(int, notify=currentMinimizerChanged)
    def currentMinimizerIndex(self):
        current_name = self.fitter.current_engine.name
        return self.minimizerNames.index(current_name)

    @Slot(int)
    def changeCurrentMinimizer(self, new_index: int):
        if self.currentMinimizerIndex == new_index:
            return

        new_name = self.minimizerNames[new_index]
        self.fitter.switch_engine(new_name)
        self.currentMinimizerChanged.emit()

    def _onCurrentMinimizerChanged(self):
        print("***** _onCurrentMinimizerChanged")

    # Minimizer method

    @Property('QVariant', notify=currentMinimizerChanged)
    def minimizerMethodNames(self):
        return self.fitter.available_methods()

    @Property(int, notify=currentMinimizerMethodChanged)
    def currentMinimizerMethodIndex(self):
        return self._current_minimizer_method_index

    @Slot(int)
    def changeCurrentMinimizerMethod(self, new_index: int):
        if self._current_minimizer_method_index == new_index:
            return

        self._current_minimizer_method_index = new_index
        self._current_minimizer_method_name = self.minimizerMethodNames[new_index]
        self.currentMinimizerMethodChanged.emit()

    def _onCurrentMinimizerMethodChanged(self):
        print("***** _onCurrentMinimizerMethodChanged")

    ####################################################################################################################
    # Calculator
    ####################################################################################################################

    @Property('QVariant', constant=True)
    def calculatorNames(self):
        return self._interface.available_interfaces

    @Property(int, notify=currentCalculatorChanged)
    def currentCalculatorIndex(self):
        return self.calculatorNames.index(self._interface.current_interface_name)

    @Slot(int)
    def changeCurrentCalculator(self, new_index: int):
        if self.currentCalculatorIndex == new_index:
            return

        new_name = self.calculatorNames[new_index]
        self._interface.switch(new_name)
        self.currentCalculatorChanged.emit()

    def _onCurrentCalculatorChanged(self):
        print("***** _onCurrentCalculatorChanged")
        data = self._data.simulations
        data = data[0]  # THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        data.name = f'{self._interface.current_interface_name} engine'
        self._sample._updateInterface()
        self.calculatedDataChanged.emit()

    ####################################################################################################################
    # Fitting
    ####################################################################################################################

    @Slot()
    def fit(self):
        exp_data = self._data.experiments[0]

        x = exp_data.x
        y = exp_data.y
        weights = 1 / exp_data.e
        method = self._current_minimizer_method_name

        res = self.fitter.fit(x, y, weights=weights, method=method)

        self._setFitResults(res)
        self.fitFinished.emit()

    @Property('QVariant', notify=fitResultsChanged)
    def fitResults(self):
        return self._fit_results

    def _defaultFitResults(self):
        return {
            "success": None,
            "nvarys": None,
            "GOF": None,
            "redchi2": None
        }

    def _setFitResults(self, res):
        self._fit_results = {
            "success": res.success,
            "nvarys": res.n_pars,
            "GOF": float(res.goodness_of_fit),
            "redchi2": float(res.reduced_chi)
        }
        self.fitResultsChanged.emit()

    def _onFitFinished(self):
        print("***** _onFitFinished")
        self.parametersChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # STATUS
    ####################################################################################################################
    ####################################################################################################################

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        model = [
            {"label": "Engine", "value": self._interface.current_interface_name},
            {"label": "Minimizer", "value": self.fitter.current_engine.name},
            {"label": "Method", "value": self._current_minimizer_method_name}
        ]
        xml = dicttoxml(model, attr_type=False)
        xml = xml.decode()
        return xml

    def _onStatusInfoChanged(self):
        print("***** _onStatusInfoChanged")
