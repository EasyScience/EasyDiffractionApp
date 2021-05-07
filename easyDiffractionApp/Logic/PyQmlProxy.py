# noqa: E501
import os
import sys
import pathlib
import datetime
import re
import timeit
from typing import Union

from PySide2.QtCore import QObject, Slot, Signal, Property

from easyCore import borg
from easyCore.Utils.UndoRedo import property_stack_deco
from easyDiffractionLib.interface import InterfaceFactory
from easyDiffractionApp.Logic.State import State

from easyDiffractionApp.Logic.Proxies.Background import BackgroundProxy
from easyDiffractionApp.Logic.Proxies.Plotting1d import Plotting1dProxy
from easyDiffractionApp.Logic.Fitter import FitterLogic as FitterLogic
from easyDiffractionApp.Logic.Stack import StackLogic

class PyQmlProxy(QObject):
    # SIGNALS

    # Project
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal()
    stateChanged = Signal(bool)

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
    phasesEnabled = Signal()

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

    fitResultsChanged = Signal()
    stopFit = Signal()

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

    # Undo Redo
    undoRedoChanged = Signal()

    # Misc
    dummySignal = Signal()

    fitFinished = Signal()
    fitFinishedNotify = Signal()
    fitResultsChanged = Signal()
    stopFit = Signal()

    # METHODS

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main
        self._interface = InterfaceFactory()

        # Plotting 1D
        self._plotting_1d_proxy = Plotting1dProxy()

        # Plotting 3D
        self._3d_plotting_libs = ['chemdoodle', 'qtdatavisualization']
        self._current_3d_plotting_lib = self._3d_plotting_libs[0]

        self._show_bonds = True
        self._bonds_max_distance = 2.0

        self.current3dPlottingLibChanged.connect(self.onCurrent3dPlottingLibChanged)

        # Initialize logics
        self.state = State(self, interface=self._interface)
        self.stateChanged.connect(self._onStateChanged)

        no_history = [self.parametersChanged]
        with_history = [self.phaseAdded, self.parametersChanged]
        self.stackLogic = StackLogic(self, callbacks_no_history=no_history, callbacks_with_history=with_history)

        self.fitLogic = FitterLogic(self, self.state._sample, self._interface.fit_func)
        self._fit_results = self.fitLogic._defaultFitResults()
        self.fitFinished.connect(self.fitLogic._onFitFinished)

        # Structure
        self.structureParametersChanged.connect(self._onStructureParametersChanged)
        self.structureParametersChanged.connect(self._onStructureViewChanged)
        self.structureParametersChanged.connect(self._onCalculatedDataChanged)
        self.structureViewChanged.connect(self._onStructureViewChanged)

        self.phaseAdded.connect(self._onPhaseAdded)
        self.phaseAdded.connect(self.phasesEnabled)
        #self.phaseAdded.connect(self.undoRedoChanged)
        self.phaseRemoved.connect(self._onPhaseRemoved)
        self.phaseRemoved.connect(self.phasesEnabled)
        #self.phaseRemoved.connect(self.undoRedoChanged)

        self.currentPhaseChanged.connect(self._onCurrentPhaseChanged)

        # Experiment
        self.patternParametersChanged.connect(self._onPatternParametersChanged)

        self.instrumentParametersChanged.connect(self._onInstrumentParametersChanged)

        self.experimentDataChanged.connect(self._onExperimentDataChanged)
        self.experimentDataAdded.connect(self._onExperimentDataAdded)
        self.experimentDataRemoved.connect(self._onExperimentDataRemoved)

        self.experimentLoadedChanged.connect(self._onExperimentLoadedChanged)
        self.experimentSkippedChanged.connect(self._onExperimentSkippedChanged)

        self._background_proxy = BackgroundProxy(self)
        self._background_proxy.asObjChanged.connect(self._onParametersChanged)
        self._background_proxy.asObjChanged.connect(self.state._sample.set_background)
        self._background_proxy.asObjChanged.connect(self.calculatedDataChanged)
        self._background_proxy.asXmlChanged.connect(self.updateChartBackground)

        # Analysis
        self.calculatedDataChanged.connect(self._onCalculatedDataChanged)
        self.simulationParametersChanged.connect(self._onSimulationParametersChanged)
        self.simulationParametersChanged.connect(self.undoRedoChanged)

        self._current_minimizer_method_index = 0
        self._current_minimizer_method_name = self.fitLogic.fitter.available_methods()[0]
        self.currentMinimizerChanged.connect(self._onCurrentMinimizerChanged)
        self.currentMinimizerMethodChanged.connect(self._onCurrentMinimizerMethodChanged)

        self.currentCalculatorChanged.connect(self._onCurrentCalculatorChanged)

        # Parameters
        self.parametersChanged.connect(self._onParametersChanged)
        self.parametersChanged.connect(self._onCalculatedDataChanged)
        self.parametersChanged.connect(self._onStructureViewChanged)
        self.parametersChanged.connect(self._onStructureParametersChanged)
        self.parametersChanged.connect(self._onPatternParametersChanged)
        self.parametersChanged.connect(self._onInstrumentParametersChanged)
        self.parametersChanged.connect(self._background_proxy.onAsObjChanged)
        self.parametersChanged.connect(self.undoRedoChanged)

        self.parametersFilterCriteriaChanged.connect(self._onParametersFilterCriteriaChanged)

        # Report
        self._report = ""

        # Status info
        self.statusInfoChanged.connect(self._onStatusInfoChanged)
        self.currentCalculatorChanged.connect(self.statusInfoChanged)
        #self.currentCalculatorChanged.connect(self.undoRedoChanged)
        self.currentMinimizerChanged.connect(self.statusInfoChanged)
        #self.currentMinimizerChanged.connect(self.undoRedoChanged)
        self.currentMinimizerMethodChanged.connect(self.statusInfoChanged)
        #self.currentMinimizerMethodChanged.connect(self.undoRedoChanged)

        # Multithreading
        self._fitter_thread = None
        self.stopFit.connect(self.fitLogic.onStopFit)

        # Screen recorder
        recorder = None
        try:
            from easyDiffractionApp.Logic.ScreenRecorder import ScreenRecorder
            recorder = ScreenRecorder()
        except (ImportError, ModuleNotFoundError):
            print('Screen recording disabled')
        self._screen_recorder = recorder

        # !! THIS SHOULD ALWAYS GO AT THE END !!
        # Start the undo/redo stack
        borg.stack.enabled = True
        borg.stack.clear()
        # borg.debug = True

        self._currentProjectPath = os.path.expanduser("~")

    ####################################################################################################################
    ####################################################################################################################
    # Charts
    ####################################################################################################################
    ####################################################################################################################

    # 1d plotting

    @Property('QVariant', notify=dummySignal)
    def plotting1d(self):
        return self._plotting_1d_proxy

    # 3d plotting

    @Property('QVariant', notify=dummySignal)
    def plotting3dLibs(self):
        return self._3d_plotting_libs

    @Property('QVariant', notify=current3dPlottingLibChanged)
    def current3dPlottingLib(self):
        return self._current_3d_plotting_lib

    @current3dPlottingLib.setter
    @property_stack_deco('Changing 3D library from {old_value} to {new_value}')
    def current3dPlottingLib(self, plotting_lib):
        self._current_3d_plotting_lib = plotting_lib
        self.current3dPlottingLibChanged.emit()

    def onCurrent3dPlottingLibChanged(self):
        pass

    # Structure view

    def _onStructureViewChanged(self):
        print("***** _onStructureViewChanged")

    @Property(bool, notify=structureViewChanged)
    def showBonds(self):
        return self._show_bonds

    @showBonds.setter
    def showBonds(self, show_bonds: bool):
        if self._show_bonds == show_bonds:
            return
        self._show_bonds = show_bonds
        self.structureViewChanged.emit()

    @Property(float, notify=structureViewChanged)
    def bondsMaxDistance(self):
        return self._bonds_max_distance

    @bondsMaxDistance.setter
    def bondsMaxDistance(self, max_distance: float):
        if self._bonds_max_distance == max_distance:
            return
        self._bonds_max_distance = max_distance
        self.structureViewChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # PROJECT
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=projectInfoChanged)
    def projectInfoAsJson(self):
        return self.state._project_info

    @projectInfoAsJson.setter
    def projectInfoAsJson(self, json_str):
        self.state.projectInfoAsJson(json_str)
        self.projectInfoChanged.emit()

    @Property(str, notify=projectInfoChanged)
    def projectInfoAsCif(self):
        return self.state.projectInfoAsCif()

    # **** TODO *****
    @Slot(str, str)
    def editProjectInfo(self, key, value):
        if key == 'location':
            self.currentProjectPath = value
            return
        else:
            if self.state._project_info[key] == value:
                return
            self.state._project_info[key] = value
        self.projectInfoChanged.emit()

    @Property(str, notify=projectInfoChanged)
    def currentProjectPath(self):
        return self._currentProjectPath

    @currentProjectPath.setter
    def currentProjectPath(self, new_path):
        if self._currentProjectPath == new_path:
            return
        self._currentProjectPath = new_path
        self.projectInfoChanged.emit()

    @Slot()
    def createProject(self):
        self.state.createProject()

    @Property(bool, notify=stateChanged)
    def stateHasChanged(self):
        return self.state._state_changed

    @stateHasChanged.setter
    def stateHasChanged(self, changed: bool):
        self.state.stateHasChanged(changed)
        # self.stateChanged.emit(changed)

    def _onStateChanged(self, changed=True):
        self.stateHasChanged = changed

    ####################################################################################################################
    # Phase models (list, xml, cif)
    ####################################################################################################################

    @Property('QVariant', notify=phasesAsObjChanged)
    def phasesAsObj(self):
        return self.state._phases_as_obj

    @Property(str, notify=phasesAsXmlChanged)
    def phasesAsXml(self):
        return self.state._phases_as_xml

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsCif(self):
        return self.state._phases_as_cif

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsExtendedCif(self):
        return self.state.phasesAsExtendedCif()

    @phasesAsCif.setter
    @property_stack_deco
    def phasesAsCif(self, phases_as_cif):
        self.state.phasesAsCif(phases_as_cif)
        self.structureParametersChanged.emit()

    def _setPhasesAsObj(self):
        start_time = timeit.default_timer()
        self.state._setPhasesAsObj()
        print("+ _setPhasesAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsObjChanged.emit()

    def _setPhasesAsXml(self):
        start_time = timeit.default_timer()
        self.state._setPhasesAsXml()
        print("+ _setPhasesAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsXmlChanged.emit()

    def _setPhasesAsCif(self):
        start_time = timeit.default_timer()
        self.state._setPhasesAsCif()
        print("+ _setPhasesAsCif: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsCifChanged.emit()

    def _onStructureParametersChanged(self):
        print("***** _onStructureParametersChanged")
        self._setPhasesAsObj()  # 0.025 s
        self._setPhasesAsXml()  # 0.065 s
        self._setPhasesAsCif()  # 0.010 s
        self.stateChanged.emit(True)

    ####################################################################################################################
    # Phase: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addSampleFromCif(self, cif_url):
        self.state.addSampleFromCif(cif_url)
        self.phaseAdded.emit()

    @Slot()
    def addDefaultPhase(self):
        print("+ addDefaultPhase")
        self.state.addDefaultPhase()
        self.phaseAdded.emit()

    @Slot(str)
    def removePhase(self, phase_name: str):
        if self.state.removePhase(phase_name):
            self.phaseRemoved.emit()

    def _onPhaseAdded(self):
        print("***** _onPhaseAdded")
        self.state._onPhaseAdded(self._background_proxy.asObj)
        self.structureParametersChanged.emit()
        self.projectInfoAsJson['samples'] = self.state._sample.phases[self.currentPhaseIndex].name
        self.projectInfoChanged.emit()

    def _onPhaseRemoved(self):
        print("***** _onPhaseRemoved")
        self.structureParametersChanged.emit()

    @Property(bool, notify=phasesEnabled)
    def samplesPresent(self) -> bool:
        return len(self.state._sample.phases) > 0

    ####################################################################################################################
    # Phase: Symmetry
    ####################################################################################################################

    # Crystal system

    @Property('QVariant', notify=structureParametersChanged)
    def crystalSystemList(self):
        return self.state.crystalSystemList()

    @Property(str, notify=structureParametersChanged)
    def currentCrystalSystem(self):
        return self.state.currentCrystalSystem()

    @currentCrystalSystem.setter
    def currentCrystalSystem(self, new_system: str):
        self.state.setCurrentCrystalSystem(new_system)

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupList(self):
        return self.state.formattedSpaceGroupList()

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroup(self):
        return self.state.getCurrentSpaceGroup()

    @currentSpaceGroup.setter
    def currentSpaceGroup(self, new_idx: int):
        self.state.currentSpaceGroup(new_idx)

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupSettingList(self):
        return self.state.formattedSpaceGroupSettingList()

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroupSetting(self):
        return self.state.currentSpaceGroupSetting()

    @currentSpaceGroupSetting.setter
    def currentSpaceGroupSetting(self, new_number: int):
        self.state.setCurrentSpaceGroupSetting(new_number)

    def _setCurrentSpaceGroup(self, new_name: str):
        self.state._setCurrentSpaceGroup(new_name)
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Phase: Atoms
    ####################################################################################################################

    @Slot()
    def addDefaultAtom(self):
        try:
            self.state.addDefaultAtom()
            self.structureParametersChanged.emit()
        except AttributeError:
            print("Error: failed to add atom")

    @Slot(str)
    def removeAtom(self, atom_label: str):
        self.state.removeAtom(atom_label)
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Current phase
    ####################################################################################################################

    @Property(int, notify=currentPhaseChanged)
    def currentPhaseIndex(self):
        return self.state._current_phase_index

    @currentPhaseIndex.setter
    def currentPhaseIndex(self, new_index: int):
        self.state.currentPhaseIndex(new_index)
        self.currentPhaseChanged.emit()

    def _onCurrentPhaseChanged(self):
        print("***** _onCurrentPhaseChanged")
        self.structureViewChanged.emit()

    # **** TODO *****

    @Slot(str)
    def setCurrentPhaseName(self, name):
        if self.state._sample.phases[self.currentPhaseIndex].name == name:
            return

        self.state._sample.phases[self.currentPhaseIndex].name = name
        self.parametersChanged.emit()
        self.projectInfoAsJson['samples'] = name
        self.projectInfoChanged.emit()

    @Property('QVariant', notify=experimentDataChanged)
    def experimentDataAsObj(self):
        return [{'name': experiment.name} for experiment in self.state._data.experiments]

    @Slot(str)
    def setCurrentExperimentDatasetName(self, name):
        if self.state._data.experiments[0].name == name:
            return

        self.state._data.experiments[0].name = name
        self.experimentDataChanged.emit()
        self.projectInfoAsJson['experiments'] = name
        self.projectInfoChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # EXPERIMENT
    ####################################################################################################################
    ####################################################################################################################

    @Property(str, notify=experimentDataAsXmlChanged)
    def experimentDataAsXml(self):
        return self.state._experiment_data_as_xml

    def _setExperimentDataAsXml(self):
        print("+ _setExperimentDataAsXml")
        self.state._setExperimentDataAsXml()
        self.experimentDataAsXmlChanged.emit()

    def _onExperimentDataChanged(self):
        print("***** _onExperimentDataChanged")
        self._setExperimentDataAsXml()  # ? s
        self.stateChanged.emit(True)

    ####################################################################################################################
    # Experiment data: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addExperimentDataFromXye(self, file_url):
        self.state.addExperimentDataFromXye(file_url)

    @Slot()
    def removeExperiment(self):
        print("+ removeExperiment")
        self.state.removeExperiment()

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        return self.state._loadExperimentData(file_url)

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        self.state._onExperimentDataAdded()

        x, y, z = self.state.experimentDataXYZ()
        self._plotting_1d_proxy.setMeasuredData(x, y, z)
        # self._background_proxy.setDefaultPoints()
        if len(self.state._sample.pattern.backgrounds) == 0:
            self.backgroundProxy.initializeContainer()
        self.experimentDataChanged.emit()
        self.projectInfoAsJson['experiments'] = self.state._data.experiments[0].name
        self.projectInfoChanged.emit()

    def _onExperimentDataRemoved(self):
        print("***** _onExperimentDataRemoved")
        self._plotting_1d_proxy.clearFrontendState()
        self.experimentDataChanged.emit()

    ####################################################################################################################
    # Experiment loaded and skipped flags
    ####################################################################################################################

    @Property(bool, notify=experimentLoadedChanged)
    def experimentLoaded(self):
        return self.state._experiment_loaded

    @experimentLoaded.setter
    def experimentLoaded(self, loaded: bool):
        self.state.experimentLoaded(loaded)
        self.experimentLoadedChanged.emit()

    @Property(bool, notify=experimentSkippedChanged)
    def experimentSkipped(self):
        return self.state._experiment_skipped

    @experimentSkipped.setter
    def experimentSkipped(self, skipped: bool):
        self.state.experimentSkipped(skipped)
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
        return self.state._simulation_parameters_as_obj

    @simulationParametersAsObj.setter
    def simulationParametersAsObj(self, json_str):
        self.state.simulationParametersAsObj(json_str)
        self.simulationParametersChanged.emit()

    def _onSimulationParametersChanged(self):
        print("***** _onSimulationParametersChanged")
        self.calculatedDataChanged.emit()

    ####################################################################################################################
    # Pattern parameters (scale, zero_shift, backgrounds)
    ####################################################################################################################

    @Property('QVariant', notify=patternParametersAsObjChanged)
    def patternParametersAsObj(self):
        return self.state._pattern_parameters_as_obj

    def _setPatternParametersAsObj(self):
        start_time = timeit.default_timer()
        self.state._setPatternParametersAsObj()
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
        return self.state._instrument_parameters_as_obj

    @Property(str, notify=instrumentParametersAsXmlChanged)
    def instrumentParametersAsXml(self):
        return self.state._instrument_parameters_as_xml

    def _setInstrumentParametersAsObj(self):
        start_time = timeit.default_timer()
        self.state._setInstrumentParametersAsObj()
        print("+ _setInstrumentParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsObjChanged.emit()

    def _setInstrumentParametersAsXml(self):
        start_time = timeit.default_timer()
        self.state._setInstrumentParametersAsXml()
        print("+ _setInstrumentParametersAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsXmlChanged.emit()

    def _onInstrumentParametersChanged(self):
        print("***** _onInstrumentParametersChanged")
        self._setInstrumentParametersAsObj()
        self._setInstrumentParametersAsXml()

    ####################################################################################################################
    # Background
    ####################################################################################################################

    @property
    def _background_obj(self):
        bgs = self.state._sample.pattern.backgrounds
        itm = None
        if len(bgs) > 0:
            itm = bgs[0]
        return itm

    @Property('QVariant', notify=dummySignal)
    def backgroundProxy(self):
        return self._background_proxy

    def updateChartBackground(self):
        self._plotting_1d_proxy.setBackgroundData(self._background_proxy.asObj.x_sorted_points,
                                                  self._background_proxy.asObj.y_sorted_points)

    ####################################################################################################################
    ####################################################################################################################
    # ANALYSIS
    ####################################################################################################################
    ####################################################################################################################

    ####################################################################################################################
    # Calculated data
    ####################################################################################################################

    def _onCalculatedDataChanged(self):
        print("***** _onCalculatedDataChanged")
        try:
            self.state._updateCalculatedData()
        finally:
            self.calculatedDataUpdated.emit()

    ####################################################################################################################
    # Fitables (parameters table from analysis tab & ...)
    ####################################################################################################################

    @Property('QVariant', notify=parametersAsObjChanged)
    def parametersAsObj(self):
        return self.state._parameters_as_obj

    @Property(str, notify=parametersAsXmlChanged)
    def parametersAsXml(self):
        return self.state._parameters_as_xml

    def _setParametersAsObj(self):
        start_time = timeit.default_timer()
        self.state._setParametersAsObj()
        print("+ _setParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsObjChanged.emit()

    def _setParametersAsXml(self):
        start_time = timeit.default_timer()
        self.state._setParametersAsXml()
        print("+ _setParametersAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsXmlChanged.emit()

    def _onParametersChanged(self):
        print("***** _onParametersChanged")
        self._setParametersAsObj()
        self._setParametersAsXml()
        self.stateChanged.emit(True)

    # Filtering
    @Slot(str)
    def setParametersFilterCriteria(self, new_criteria):
        self.state.setParametersFilterCriteria()
        self.parametersFilterCriteriaChanged.emit()

    def _onParametersFilterCriteriaChanged(self):
        print("***** _onParametersFilterCriteriaChanged")
        self._onParametersChanged()

    ####################################################################################################################
    # Any parameter
    ####################################################################################################################

    @Slot(str, 'QVariant')
    def editParameter(self, obj_id: str, new_value: Union[bool, float, str]):  # covers both parameter and descriptor
        self.state.editParameter(obj_id, new_value)

    ####################################################################################################################
    # Minimizer
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def minimizerNames(self):
        return self.fitLogic.fitter.available_engines

    @Property(int, notify=currentMinimizerChanged)
    def currentMinimizerIndex(self):
        current_name = self.fitLogic.fitter.current_engine.name
        return self.minimizerNames.index(current_name)

    @currentMinimizerIndex.setter
    @property_stack_deco('Minimizer change')
    def currentMinimizerIndex(self, new_index: int):
        if self.currentMinimizerIndex == new_index:
            return
        new_name = self.minimizerNames[new_index]
        self.fitLogic.fitter.switch_engine(new_name)
        self.currentMinimizerChanged.emit()

    def _onCurrentMinimizerChanged(self):
        print("***** _onCurrentMinimizerChanged")
        idx = 0
        minimizer_name = self.fitLogic.fitter.current_engine.name
        if minimizer_name == 'lmfit':
            idx = self.minimizerMethodNames.index('leastsq')
        elif minimizer_name == 'bumps':
            idx = self.minimizerMethodNames.index('lm')
        if -1 < idx != self._current_minimizer_method_index:
            # Bypass the property as it would be added to the stack.
            self._current_minimizer_method_index = idx
            self._current_minimizer_method_name = self.minimizerMethodNames[idx]
            self.currentMinimizerMethodChanged.emit()

    # Minimizer method
    # **** TODO *****
    @Property('QVariant', notify=currentMinimizerChanged)
    def minimizerMethodNames(self):
        current_minimizer = self.minimizerNames[self.currentMinimizerIndex]
        tested_methods = {
            'lmfit': ['leastsq', 'powell', 'cobyla'],
            'bumps': ['newton', 'lm'],
            'DFO_LS': ['leastsq']
        }
        #return self.fitter.available_methods()
        return tested_methods[current_minimizer]

    @Property(int, notify=currentMinimizerMethodChanged)
    def currentMinimizerMethodIndex(self):
        return self._current_minimizer_method_index

    @currentMinimizerMethodIndex.setter
    @property_stack_deco('Minimizer method change')
    def currentMinimizerMethodIndex(self, new_index: int):
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

    @currentCalculatorIndex.setter
    @property_stack_deco('Calculation engine change')
    def currentCalculatorIndex(self, new_index: int):
        if self.currentCalculatorIndex == new_index:
            return

        new_name = self.calculatorNames[new_index]
        self._interface.switch(new_name)
        self.currentCalculatorChanged.emit()

    def _onCurrentCalculatorChanged(self):
        print("***** _onCurrentCalculatorChanged")
        self.state._onCurrentCalculatorChanged()
        self.calculatedDataChanged.emit()

    ####################################################################################################################
    # Fitting
    ####################################################################################################################

    @Slot()
    def fit(self):
        self.fitLogic.fit(self.state._data, self._current_minimizer_method_name)

    @Property('QVariant', notify=fitResultsChanged)
    def fitResults(self):
        return self.fitLogic._fit_results

    @Property(bool, notify=fitFinishedNotify)
    def isFitFinished(self):
        return self.fitLogic._fit_finished

    @isFitFinished.setter
    def isFitFinished(self, fit_finished: bool):
        self.fitLogic.setFitFinished(fit_finished)
        self.fitFinishedNotify.emit()

    ####################################################################################################################
    ####################################################################################################################
    # Report
    ####################################################################################################################
    ####################################################################################################################

    @Slot(str)
    def setReport(self, report):
        """
        Keep the QML generated HTML report for saving
        """
        self.state._report = report

    @Slot(str)
    def saveReport(self, filepath):
        """
        Save the generated report to the specified file
        Currently only html
        """
        success = self.state.saveReport(filepath)
        self.htmlExportingFinished.emit(success, filepath)

    ####################################################################################################################
    ####################################################################################################################
    # STATUS
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=statusInfoChanged)
    def statusModelAsObj(self):
        engine_name = self.fitLogic.fitter.current_engine.name
        minimizer_name = self._current_minimizer_method_name
        return self.state.statusModelAsObj(engine_name, minimizer_name)

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        engine_name = self.fitLogic.fitter.current_engine.name
        minimizer_name = self._current_minimizer_method_name
        return self.state.statusModelAsXml(engine_name, minimizer_name)

    def _onStatusInfoChanged(self):
        print("***** _onStatusInfoChanged")

    ####################################################################################################################
    ####################################################################################################################
    # Project examples
    ####################################################################################################################
    ####################################################################################################################

    @Property(str, notify=dummySignal)
    def projectExamplesAsXml(self):
        return self.state.projectExamplesAsXml()

    ####################################################################################################################
    ####################################################################################################################
    # Screen recorder
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def screenRecorder(self):
        return self._screen_recorder

    ####################################################################################################################
    ####################################################################################################################
    # State save/load
    ####################################################################################################################
    ####################################################################################################################

    @Slot()
    def saveProject(self):
        self._saveProject()
        self.stateChanged.emit(False)

    @Slot(str)
    def loadProjectAs(self, filepath):
        self._loadProjectAs(filepath)
        self.stateChanged.emit(False)

    @Slot()
    def loadProject(self):
        self._loadProject()
        self.stateChanged.emit(False)

    @Slot(str)
    def loadExampleProject(self, filepath):
        self._loadProjectAs(filepath)
        self.currentProjectPath = '--- EXAMPLE ---'
        self.stateChanged.emit(False)

    @Property(str, notify=dummySignal)
    def projectFilePath(self):
        return self.state.project_save_filepath

    def _saveProject(self):
        self.state._saveProject()

    def _loadProjectAs(self, filepath):
        self.state._loadProjectAs(filepath)

    def _loadProject(self):
        self.state._loadProject()

    ####################################################################################################################
    # Undo/Redo stack operations
    ####################################################################################################################

    @Property(bool, notify=undoRedoChanged)
    def canUndo(self) -> bool:
        return self.stackLogic.canUndo()

    @Property(bool, notify=undoRedoChanged)
    def canRedo(self) -> bool:
        return self.stackLogic.canRedo()

    @Slot()
    def undo(self):
        self.stackLogic.undo()

    @Slot()
    def redo(self):
        self.stackLogic.redo()

    @Property(str, notify=undoRedoChanged)
    def undoText(self):
        return self.stackLogic.undoText()

    @Property(str, notify=undoRedoChanged)
    def redoText(self):
        return self.stackLogic.redoText()

    @Slot()
    def resetUndoRedoStack(self):
        self.stackLogic.resetUndoRedoStack()
