import os
import datetime
import time
import pathlib

import json
from typing import Union

from dicttoxml import dicttoxml

import timeit

from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCore import QByteArray, QBuffer, QIODevice
from PySide2.QtCore import QPointF
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QPdfWriter, QTextDocument

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

from easyDiffractionApp.Logic.Proxies.BackgroundProxy import BackgroundProxy
from easyDiffractionApp.Logic.Proxies.PlottingQtCharts import QtChartsProxy
from easyDiffractionApp.Logic.Proxies.PlottingBokeh import BokehProxy

from easyDiffractionApp.Logic.ScreenRecorder import ScreenRecorder


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
    structureViewUpdated = Signal()

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
    calculatedDataUpdated = Signal()

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

    htmlExportingFinished = Signal(bool, str)

    # Status info
    statusInfoChanged = Signal()

    # Misc
    dummySignal = Signal()

    # METHODS

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main
        self._interface = InterfaceFactory()
        self._sample = self._defaultSample()

        # Charts 1D
        self._qtcharts_proxy = QtChartsProxy()
        self._bokeh_proxy = BokehProxy()

        self._1d_plotting_libs = ['qtcharts', 'bokeh']
        self._current_1d_plotting_lib = 'bokeh'
        #self._current_1d_plotting_lib_proxy = self.initCurrent1dPlottingProxy()

        self._show_measured_series = True
        self._show_difference_chart = False

        self.current1dPlottingLibChanged.connect(self.onCurrent1dPlottingLibChanged)

        # Charts 3D
        self._vtk_handler = None

        self._3d_plotting_libs = ['vtk', 'qtdatavisualization', 'chemdoodle']
        self._current_3d_plotting_lib = self._3d_plotting_libs[0]

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
        self._background_proxy.asObjChanged.connect(self._sample.set_background)
        self._background_proxy.asObjChanged.connect(self.calculatedDataChanged)

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

        # Report
        self._report = ""

        # Status info
        self.statusInfoChanged.connect(self._onStatusInfoChanged)
        self.currentCalculatorChanged.connect(self.statusInfoChanged)
        self.currentMinimizerChanged.connect(self.statusInfoChanged)
        self.currentMinimizerMethodChanged.connect(self.statusInfoChanged)

        # Screen recorder
        self._screen_recorder = ScreenRecorder()

    ####################################################################################################################
    ####################################################################################################################
    # Charts
    ####################################################################################################################
    ####################################################################################################################

    # Vtk

    def setVtkHandler(self, vtk_handler):
        self._vtk_handler = vtk_handler

    @Property(bool, notify=dummySignal)
    def showBonds(self):
        if self._vtk_handler is None:
            return True
        return self._vtk_handler.show_bonds

    @showBonds.setter
    def showBonds(self, show_bonds: bool):
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
    def bondsMaxDistance(self, max_distance: float):
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
        self.structureViewUpdated.emit()

    # QtCharts

    @Property('QVariant', notify=dummySignal)
    def qtCharts(self):
        return self._qtcharts_proxy

    # Bokeh

    @Property('QVariant', notify=dummySignal)
    def bokeh(self):
        return self._bokeh_proxy

    # Plotting libs

    def initCurrent1dPlottingProxy(self):
        pass
        #if self._current_1d_plotting_lib == 'bokeh':
        #    return self._bokeh_proxy
        #elif self._current_1d_plotting_lib == 'qtcharts':
        #    return self._qtcharts_proxy
        #else:
        #    raise NotImplementedError(f'Supported plotting libraries are: qtcharts and bokeh.')

    @Property('QVariant', notify=dummySignal)
    def plotting1dLibs(self):
        return self._1d_plotting_libs

    @Property(str, notify=current1dPlottingLibChanged)
    def current1dPlottingLib(self):
        return self._current_1d_plotting_lib

    @current1dPlottingLib.setter
    def current1dPlottingLib(self, plotting_lib):
        self._current_1d_plotting_lib = plotting_lib
        self.current1dPlottingLibChanged.emit()

    def onCurrent1dPlottingLibChanged(self):
        pass
        #measured_xarray = self._current_1d_plotting_lib_proxy._measured_xarray
        #measured_yarray = self._current_1d_plotting_lib_proxy._measured_yarray
        #measured_syarray = self._current_1d_plotting_lib_proxy._measured_syarray
        #calculated_xarray = self._current_1d_plotting_lib_proxy._calculated_xarray
        #calculated_yarray = self._current_1d_plotting_lib_proxy._calculated_yarray
        #bragg_xarray = self._current_1d_plotting_lib_proxy._bragg_xarray
        #if self._current_1d_plotting_lib == 'qtcharts':
        #    self._current_1d_plotting_lib_proxy = self._qtcharts_proxy
        #elif self._current_1d_plotting_lib == 'bokeh':
        #    self._current_1d_plotting_lib_proxy = self._bokeh_proxy
        #else:
        #    raise NotImplementedError(f'Only the following plotting libs are available: {self._1d_plotting_libs}.')
        #self._current_1d_plotting_lib_proxy.setMeasuredData(measured_xarray, measured_yarray, measured_syarray)
        #self._current_1d_plotting_lib_proxy.setCalculatedData(calculated_xarray, calculated_yarray)
        #self._current_1d_plotting_lib_proxy.setBraggData(bragg_xarray)

    @Property('QVariant', notify=dummySignal)
    def plotting3dLibs(self):
        return self._3d_plotting_libs

    @Property('QVariant', notify=current3dPlottingLibChanged)
    def current3dPlottingLib(self):
        return self._current_3d_plotting_lib

    @current3dPlottingLib.setter
    def current3dPlottingLib(self, plotting_lib):
        self._current_3d_plotting_lib = plotting_lib
        self.current3dPlottingLibChanged.emit()

    def onCurrent3dPlottingLibChanged(self):
        if self.current3dPlottingLib == 'vtk':
            self._onStructureViewChanged()

    @Property(bool, notify=showDifferenceChartChanged)
    def showDifferenceChart(self):
        return self._show_difference_chart

    @showDifferenceChart.setter
    def showDifferenceChart(self, show):
        if self._show_difference_chart == show:
            return
        self._show_difference_chart = show
        self.showDifferenceChartChanged.emit()

    @Property(bool, notify=showMeasuredSeriesChanged)
    def showMeasuredSeries(self):
        return self._show_measured_series

    @showMeasuredSeries.setter
    def showMeasuredSeries(self, show):
        if self._show_measured_series == show:
            return
        self._show_measured_series = show
        self.showMeasuredSeriesChanged.emit()

    # Charts for report

    @Slot('QVariant', result=str)
    def imageToSource(self, image):
        ba = QByteArray()
        buffer = QBuffer(ba)
        buffer.open(QIODevice.WriteOnly)
        image.save(buffer, 'png')
        data = ba.toBase64().data().decode('utf-8')
        source = f'data:image/png;base64,{data}'
        return source

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
    def projectInfoAsJson(self, json_str):
        self._project_info = json.loads(json_str)
        self.projectInfoChanged.emit()

    @Property(str, notify=projectInfoChanged)
    def projectInfoAsCif(self):
        cif_list = []
        for key, value in self.projectInfoAsJson.items():
            if ' ' in value:
                value = f"'{value}'"
            cif_list.append(f'_{key} {value}')
        cif_str = '\n'.join(cif_list)
        return cif_str

    @Slot(str, str)
    def editProjectInfo(self, key, value):
        if self._project_info[key] == value:
            return

        self._project_info[key] = value
        self.projectInfoChanged.emit()

    @Slot()
    def createProject(self):
        projectPath = self.projectInfoAsJson['location']
        mainCif = os.path.join(projectPath, 'project.cif')
        samplesPath = os.path.join(projectPath, 'samples')
        experimentsPath = os.path.join(projectPath, 'experiments')
        calculationsPath = os.path.join(projectPath, 'calculations')
        if not os.path.exists(projectPath):
            os.makedirs(projectPath)
            os.makedirs(samplesPath)
            os.makedirs(experimentsPath)
            os.makedirs(calculationsPath)
            with open(mainCif, 'w') as file:
                file.write(self.projectInfoAsCif)
        else:
            print(f"ERROR: Directory {projectPath} already exists")

    def _defaultProjectInfo(self):
        return dict(
            name="Example Project",
            location=os.path.join(os.path.expanduser("~"), "Example Project"),
            short_description="diffraction, powder, 1D",
            samples="Not loaded",
            experiments="Not loaded",
            calculations="Not created",
            modified=datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
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

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsExtendedCif(self):
        if len(self._sample.phases) == 0:
            return

        symm_ops = self._sample.phases[0].spacegroup.symmetry_opts
        symm_ops_cif_loop = "loop_\n _symmetry_equiv_pos_as_xyz\n"
        for symm_op in symm_ops:
            symm_ops_cif_loop += f' {symm_op.as_xyz_string()}\n'
        return self._phases_as_cif + symm_ops_cif_loop

    @phasesAsCif.setter
    def phasesAsCif(self, phases_as_cif):
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
    def addSampleFromCif(self, cif_url):
        cif_path = generalizePath(cif_url)
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
    def currentCrystalSystem(self, new_system: str):
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
    def currentSpaceGroup(self, new_idx: int):
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
    def currentSpaceGroupSetting(self, new_number: int):
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
    def currentPhaseIndex(self, new_index: int):
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
        #self._current_1d_plotting_lib_proxy.setMeasuredData(self._experiment_data.x, self._experiment_data.y, self._experiment_data.e)
        self._bokeh_proxy.setMeasuredData(self._experiment_data.x, self._experiment_data.y, self._experiment_data.e)
        self._qtcharts_proxy.setMeasuredData(self._experiment_data.x, self._experiment_data.y, self._experiment_data.e)
        self._experiment_parameters = self._experimentDataParameters(self._experiment_data)
        self.simulationParametersAsObj = json.dumps(self._experiment_parameters)
        self.experiments = [self._defaultExperiment()]
        self._background_proxy.setDefaultPoints()
        self.experimentDataChanged.emit()

    def _onExperimentDataRemoved(self):
        print("***** _onExperimentDataRemoved")
        self.experimentDataChanged.emit()

    ####################################################################################################################
    # Experiment loaded and skipped flags
    ####################################################################################################################

    @Property(bool, notify=experimentLoadedChanged)
    def experimentLoaded(self):
        return self._experiment_loaded

    @experimentLoaded.setter
    def experimentLoaded(self, loaded: bool):
        if self._experiment_loaded == loaded:
            return

        self._experiment_loaded = loaded
        self.experimentLoadedChanged.emit()

    @Property(bool, notify=experimentSkippedChanged)
    def experimentSkipped(self):
        return self._experiment_skipped

    @experimentSkipped.setter
    def experimentSkipped(self, skipped: bool):
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
    def simulationParametersAsObj(self, json_str):
        if self._simulation_parameters_as_obj == json.loads(json_str):
            return

        self._simulation_parameters_as_obj = json.loads(json_str)
        self.simulationParametersChanged.emit()

    def _defaultSimulationParameters(self):
        return {
            "x_min": 10.0,
            "x_max": 120.0,
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

    @Property('QVariant', notify=dummySignal)
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

        self._sample.output_index = self.currentPhaseIndex

        #  THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        sim = self._data.simulations[0]

        if self.experimentLoaded:
            exp = self._data.experiments[0]
            sim.x = exp.x

        elif self.experimentSkipped:
            x_min = float(self._simulation_parameters_as_obj['x_min'])
            x_max = float(self._simulation_parameters_as_obj['x_max'])
            x_step = float(self._simulation_parameters_as_obj['x_step'])
            num_points = int((x_max - x_min) / x_step + 1)
            sim.x = np.linspace(x_min, x_max, num_points)

        sim.y = self._interface.fit_func(sim.x)  # CrysPy: 0.5 s, CrysFML: 0.005 s, GSAS-II: 0.25 s

        #self._current_1d_plotting_lib_proxy.setCalculatedData(sim.x, sim.y)
        #self._current_1d_plotting_lib_proxy.setBraggData(np.array([12.950,15.796,20.409,20.479,24.246,25.913,26.069,29.070,30.627,31.903,33.333,34.563,37.087,38.171,39.547,40.471,41.505,41.651,42.834,43.659,44.673,44.902,46.710,46.809,47.890,48.691,49.672,50.604,51.681,52.454,53.285,53.321,53.626,55.082,55.117,56.056,56.134,56.269,57.975,58.668,60.258,60.291,60.494,61.169,63.769,64.214,64.456,65.822,65.858,66.594,66.687,67.445,67.715,68.173,68.265,68.351,68.381,68.645,70.004,70.533,70.550,70.950,72.089,72.105,72.291,72.460,72.812,72.901,73.504,74.716,75.018,75.335,76.630,77.696,78.106,78.995,79.024,79.502,79.625,80.309,80.395,81.355,81.683,83.153,83.509,84.026,84.542,85.160,85.683,86.004,86.798,86.845,87.328,87.541,88.256,88.392,88.610,88.762,89.882,90.254,90.379,90.396,90.556,90.641,90.926,91.712,91.854,92.179,92.207,92.419,92.629,93.824,93.878,94.242,94.834,96.095,96.238,97.065,97.439,97.689,98.276,98.946,99.598,99.744,99.965,100.424,101.226,101.259,101.586,101.800,102.749,103.112,103.494,103.640,103.805,103.892,104.257,104.804,104.906,105.207,105.723,105.730,106.501,107.277,107.630,108.002,108.170,108.530,108.560,110.141,110.292,110.554,110.604,111.073,111.701,112.607,112.643,113.411,113.463,114.292,114.448,114.982,115.097,116.491,116.601,116.689,117.394,117.471,118.726,119.420,119.827]))
        self._bokeh_proxy.setCalculatedData(sim.x, sim.y)
        self._bokeh_proxy.setBraggData(np.array([12.950,15.796,20.409,20.479,24.246,25.913,26.069,29.070,30.627,31.903,33.333,34.563,37.087,38.171,39.547,40.471,41.505,41.651,42.834,43.659,44.673,44.902,46.710,46.809,47.890,48.691,49.672,50.604,51.681,52.454,53.285,53.321,53.626,55.082,55.117,56.056,56.134,56.269,57.975,58.668,60.258,60.291,60.494,61.169,63.769,64.214,64.456,65.822,65.858,66.594,66.687,67.445,67.715,68.173,68.265,68.351,68.381,68.645,70.004,70.533,70.550,70.950,72.089,72.105,72.291,72.460,72.812,72.901,73.504,74.716,75.018,75.335,76.630,77.696,78.106,78.995,79.024,79.502,79.625,80.309,80.395,81.355,81.683,83.153,83.509,84.026,84.542,85.160,85.683,86.004,86.798,86.845,87.328,87.541,88.256,88.392,88.610,88.762,89.882,90.254,90.379,90.396,90.556,90.641,90.926,91.712,91.854,92.179,92.207,92.419,92.629,93.824,93.878,94.242,94.834,96.095,96.238,97.065,97.439,97.689,98.276,98.946,99.598,99.744,99.965,100.424,101.226,101.259,101.586,101.800,102.749,103.112,103.494,103.640,103.805,103.892,104.257,104.804,104.906,105.207,105.723,105.730,106.501,107.277,107.630,108.002,108.170,108.530,108.560,110.141,110.292,110.554,110.604,111.073,111.701,112.607,112.643,113.411,113.463,114.292,114.448,114.982,115.097,116.491,116.601,116.689,117.394,117.471,118.726,119.420,119.827]))
        self._qtcharts_proxy.setCalculatedData(sim.x, sim.y)
        self._qtcharts_proxy.setBraggData(np.array([12.950,15.796,20.409,20.479,24.246,25.913,26.069,29.070,30.627,31.903,33.333,34.563,37.087,38.171,39.547,40.471,41.505,41.651,42.834,43.659,44.673,44.902,46.710,46.809,47.890,48.691,49.672,50.604,51.681,52.454,53.285,53.321,53.626,55.082,55.117,56.056,56.134,56.269,57.975,58.668,60.258,60.291,60.494,61.169,63.769,64.214,64.456,65.822,65.858,66.594,66.687,67.445,67.715,68.173,68.265,68.351,68.381,68.645,70.004,70.533,70.550,70.950,72.089,72.105,72.291,72.460,72.812,72.901,73.504,74.716,75.018,75.335,76.630,77.696,78.106,78.995,79.024,79.502,79.625,80.309,80.395,81.355,81.683,83.153,83.509,84.026,84.542,85.160,85.683,86.004,86.798,86.845,87.328,87.541,88.256,88.392,88.610,88.762,89.882,90.254,90.379,90.396,90.556,90.641,90.926,91.712,91.854,92.179,92.207,92.419,92.629,93.824,93.878,94.242,94.834,96.095,96.238,97.065,97.439,97.689,98.276,98.946,99.598,99.744,99.965,100.424,101.226,101.259,101.586,101.800,102.749,103.112,103.494,103.640,103.805,103.892,104.257,104.804,104.906,105.207,105.723,105.730,106.501,107.277,107.630,108.002,108.170,108.530,108.560,110.141,110.292,110.554,110.604,111.073,111.701,112.607,112.643,113.411,113.463,114.292,114.448,114.982,115.097,116.491,116.601,116.689,117.394,117.471,118.726,119.420,119.827]))

        print("+ _updateCalculatedData: {0:.3f} s".format(timeit.default_timer() - start_time))

    def _onCalculatedDataChanged(self):
        print("***** _onCalculatedDataChanged")
        self._updateCalculatedData()
        self.calculatedDataUpdated.emit()

    @Property(str, notify=calculatedDataUpdated)
    def calculatedDataXStr(self):
        return self._calculated_data_x_str

    @Property(str, notify=calculatedDataUpdated)
    def calculatedDataYStr(self):
        return self._calculated_data_y_str

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
                "error": float(par.error),
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

    @Property('QVariant', notify=dummySignal)
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

    @Property('QVariant', notify=dummySignal)
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

    @Slot(str)
    def setReport(self, report):
        """
        Keep the QML generated HTML report for saving
        """
        self._report = report

    @Slot(str)
    def saveReport(self, filepath):
        """
        Save the generated report to the specified file
        Currently only html
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self._report)
            success = True
        except IOError:
            success = False
        finally:
            self.htmlExportingFinished.emit(success, filepath)

    ####################################################################################################################
    ####################################################################################################################
    # STATUS
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=statusInfoChanged)
    def statusModelAsObj(self):
        obj = {
            "calculation": self._interface.current_interface_name,
            "minimization": f'{self.fitter.current_engine.name} ({self._current_minimizer_method_name})'
        }
        return obj

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        model = [
            {"label": "Calculation", "value": self._interface.current_interface_name},
            {"label": "Minimization", "value": f'{self.fitter.current_engine.name} ({self._current_minimizer_method_name})'}
        ]
        xml = dicttoxml(model, attr_type=False)
        xml = xml.decode()
        return xml

    def _onStatusInfoChanged(self):
        print("***** _onStatusInfoChanged")

    ####################################################################################################################
    ####################################################################################################################
    # Screen recorder
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def screenRecorder(self):
        return self._screen_recorder
