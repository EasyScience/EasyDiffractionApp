# noqa: E501
import os
import timeit

from typing import Union

from PySide2.QtCore import QObject, Slot, Signal, Property

from easyCore.Utils.UndoRedo import property_stack_deco
from easyDiffractionApp.Logic.LogicController import LogicController


class PyQmlProxy(QObject):
    # SIGNALS

    # Project
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal()
    stateChanged = Signal(bool)

    # Fitables
    parametersAsObjChanged = Signal()
    parametersAsXmlChanged = Signal()

    # Structure
    structureParametersChanged = Signal()
    structureViewChanged = Signal()

    phasesAsObjChanged = Signal()
    phasesAsXmlChanged = Signal()
    phasesAsCifChanged = Signal()
    currentPhaseChanged = Signal()
    phasesEnabled = Signal()

    # Experiment
    patternParametersAsObjChanged = Signal()

    instrumentParametersAsObjChanged = Signal()
    instrumentParametersAsXmlChanged = Signal()

    experimentDataChanged = Signal()
    experimentDataAsXmlChanged = Signal()

    experimentLoadedChanged = Signal()
    experimentSkippedChanged = Signal()

    # Analysis
    simulationParametersChanged = Signal()

    fitResultsChanged = Signal()
    fitFinishedNotify = Signal()
    stopFit = Signal()

    currentMinimizerChanged = Signal()
    currentMinimizerMethodChanged = Signal()
    currentCalculatorChanged = Signal()

    # Plotting
    current3dPlottingLibChanged = Signal()

    htmlExportingFinished = Signal(bool, str)

    # Status info
    statusInfoChanged = Signal()

    # Undo Redo
    undoRedoChanged = Signal()

    # Misc
    dummySignal = Signal()

    # METHODS

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize logics
        self.stateChanged.connect(self._onStateChanged)

        # initialize the logic controller
        self.lc = LogicController(self)

        # Structure
        self.structureParametersChanged.connect(self._onStructureParametersChanged)
        self.structureParametersChanged.connect(self.lc.chartsLogic._onStructureViewChanged)
        self.structureParametersChanged.connect(self.lc.state._updateCalculatedData())

        self.structureViewChanged.connect(self.lc.chartsLogic._onStructureViewChanged)

        self.lc.phaseAdded.connect(self._onPhaseAdded)
        self.lc.phaseAdded.connect(self.phasesEnabled)

        self.currentPhaseChanged.connect(self._onCurrentPhaseChanged)
        self.current3dPlottingLibChanged.connect(self.onCurrent3dPlottingLibChanged)

        # Experiment
        self.experimentDataChanged.connect(self._onExperimentDataChanged)

        self.experimentLoadedChanged.connect(self._onExperimentLoadedChanged)
        self.experimentSkippedChanged.connect(self._onExperimentSkippedChanged)

        # Analysis
        self.simulationParametersChanged.connect(self._onSimulationParametersChanged)
        self.simulationParametersChanged.connect(self.undoRedoChanged)

        self.currentMinimizerChanged.connect(self._onCurrentMinimizerChanged)
        self.currentMinimizerMethodChanged.connect(self._onCurrentMinimizerMethodChanged)

        # Status info
        self.statusInfoChanged.connect(self._onStatusInfoChanged)
        self.currentCalculatorChanged.connect(self.statusInfoChanged)
        #self.currentCalculatorChanged.connect(self.undoRedoChanged)
        self.currentMinimizerChanged.connect(self.statusInfoChanged)
        #self.currentMinimizerChanged.connect(self.undoRedoChanged)
        self.currentMinimizerMethodChanged.connect(self.statusInfoChanged)
        #self.currentMinimizerMethodChanged.connect(self.undoRedoChanged)

        # Multithreading
        # self.stopFit.connect(self.lc.fitLogic.onStopFit)

        # start the undo/redo stack
        self.lc.initializeBorg()

    ####################################################################################################################
    ####################################################################################################################
    # Charts
    ####################################################################################################################
    ####################################################################################################################

    # 1d plotting

    @Property('QVariant', notify=dummySignal)
    def plotting1d(self):
        return self.lc.chartsLogic.plotting1d()

    # 3d plotting
    @Property('QVariant', notify=dummySignal)
    def plotting3dLibs(self):
        return self.lc.chartsLogic.plotting3dLibs()

    @Property('QVariant', notify=current3dPlottingLibChanged)
    def current3dPlottingLib(self):
        return self.lc.chartsLogic.current3dPlottingLib()

    @current3dPlottingLib.setter
    @property_stack_deco('Changing 3D library from {old_value} to {new_value}')
    def current3dPlottingLib(self, plotting_lib):
        self.lc.chartsLogic._current_3d_plotting_lib = plotting_lib
        self.current3dPlottingLibChanged.emit()

    def onCurrent3dPlottingLibChanged(self):
        self.lc.chartsLogic.onCurrent3dPlottingLibChanged()

    # Structure view

    @Property(bool, notify=structureViewChanged)
    def showBonds(self):
        return self.lc.chartsLogic.showBonds()

    @showBonds.setter
    def showBonds(self, show_bonds: bool):
        self.lc.chartsLogic.setShowBons(show_bonds)
        self.structureViewChanged.emit()

    @Property(float, notify=structureViewChanged)
    def bondsMaxDistance(self):
        return self.chartsLogic.bondsMaxDistance()

    @bondsMaxDistance.setter
    def bondsMaxDistance(self, max_distance: float):
        self.lc.chartsLogic.setBondsMaxDistance(max_distance)
        self.structureViewChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # PROJECT
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=projectInfoChanged)
    def projectInfoAsJson(self):
        return self.lc.state._project_info

    @projectInfoAsJson.setter
    def projectInfoAsJson(self, json_str):
        self.lc.state.projectInfoAsJson(json_str)
        self.projectInfoChanged.emit()

    @Property(str, notify=projectInfoChanged)
    def projectInfoAsCif(self):
        return self.lc.state.projectInfoAsCif()

    @Slot(str, str)
    def editProjectInfo(self, key, value):
        self.lc.state.editProjectInfo(key, value)
        self.projectInfoChanged.emit()

    @Property(str, notify=projectInfoChanged)
    def currentProjectPath(self):
        return self.lc.state._currentProjectPath

    @currentProjectPath.setter
    def currentProjectPath(self, new_path):
        self.lc.state.currentProjectPath(new_path)
        self.projectInfoChanged.emit()

    @Slot()
    def createProject(self):
        self.lc.state.createProject()

    @Property(bool, notify=stateChanged)
    def stateHasChanged(self):
        return self.lc.state._state_changed

    @stateHasChanged.setter
    def stateHasChanged(self, changed: bool):
        self.lc.state.stateHasChanged(changed)

    def _onStateChanged(self, changed=True):
        self.stateHasChanged = changed

    ####################################################################################################################
    # Phase models (list, xml, cif)
    ####################################################################################################################

    @Property('QVariant', notify=phasesAsObjChanged)
    def phasesAsObj(self):
        return self.lc.state._phases_as_obj

    @Property(str, notify=phasesAsXmlChanged)
    def phasesAsXml(self):
        return self.lc.state._phases_as_xml

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsCif(self):
        return self.lc.state._phases_as_cif

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsExtendedCif(self):
        return self.lc.state.phasesAsExtendedCif()

    @phasesAsCif.setter
    @property_stack_deco
    def phasesAsCif(self, phases_as_cif):
        self.lc.state.phasesAsCif(phases_as_cif)
        self.lc.parametersChanged.emit()

    def _setPhasesAsObj(self):
        start_time = timeit.default_timer()
        self.lc.state._setPhasesAsObj()
        print("+ _setPhasesAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsObjChanged.emit()

    def _setPhasesAsXml(self):
        start_time = timeit.default_timer()
        self.lc.state._setPhasesAsXml()
        print("+ _setPhasesAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsXmlChanged.emit()

    def _setPhasesAsCif(self):
        start_time = timeit.default_timer()
        self.lc.state._setPhasesAsCif()
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
        self.lc.state.addSampleFromCif(cif_url)
        self.lc.phaseAdded.emit()

    @Slot()
    def addDefaultPhase(self):
        print("+ addDefaultPhase")
        self.lc.state.addDefaultPhase()
        self.lc.phaseAdded.emit()

    @Slot(str)
    def removePhase(self, phase_name: str):
        self.lc.removePhase(phase_name)

    def _onPhaseAdded(self):
        print("***** _onPhaseAdded")
        self.lc._onPhaseAdded()
        self.phasesEnabled.emit()
        self.structureParametersChanged.emit()
        self.projectInfoChanged.emit()

    @Property(bool, notify=phasesEnabled)
    def samplesPresent(self) -> bool:
        return self.lc.samplesPresent()

    ####################################################################################################################
    # Phase: Symmetry
    ####################################################################################################################

    # Crystal system

    @Property('QVariant', notify=structureParametersChanged)
    def crystalSystemList(self):
        return self.lc.state.crystalSystemList()

    @Property(str, notify=structureParametersChanged)
    def currentCrystalSystem(self):
        return self.lc.state.currentCrystalSystem()

    @currentCrystalSystem.setter
    def currentCrystalSystem(self, new_system: str):
        self.lc.state.setCurrentCrystalSystem(new_system)
        self.structureParametersChanged.emit()

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupList(self):
        return self.lc.state.formattedSpaceGroupList()

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroup(self):
        return self.lc.state.getCurrentSpaceGroup()

    @currentSpaceGroup.setter
    def currentSpaceGroup(self, new_idx: int):
        self.lc.state.currentSpaceGroup(new_idx)
        self.structureParametersChanged.emit()

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupSettingList(self):
        return self.lc.state.formattedSpaceGroupSettingList()

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroupSetting(self):
        return self.lc.state.currentSpaceGroupSetting()

    @currentSpaceGroupSetting.setter
    def currentSpaceGroupSetting(self, new_number: int):
        self.lc.state.setCurrentSpaceGroupSetting(new_number)
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Phase: Atoms
    ####################################################################################################################

    @Slot()
    def addDefaultAtom(self):
        try:
            self.lc.state.addDefaultAtom()
            self.structureParametersChanged.emit()
        except AttributeError:
            print("Error: failed to add atom")

    @Slot(str)
    def removeAtom(self, atom_label: str):
        self.lc.state.removeAtom(atom_label)
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Current phase
    ####################################################################################################################

    @Property(int, notify=currentPhaseChanged)
    def currentPhaseIndex(self):
        return self.lc.state._current_phase_index

    @currentPhaseIndex.setter
    def currentPhaseIndex(self, new_index: int):
        if self.lc.state.currentPhaseIndex(new_index):
            self.currentPhaseChanged.emit()

    def _onCurrentPhaseChanged(self):
        print("***** _onCurrentPhaseChanged")
        self.structureViewChanged.emit()

    @Slot(str)
    def setCurrentPhaseName(self, name):
        self.lc.state.setCurrentPhaseName(name)
        self.lc.parametersChanged.emit()
        self.projectInfoChanged.emit()

    @Property('QVariant', notify=experimentDataChanged)
    def experimentDataAsObj(self):
        return self.lc.state.experimentDataAsObj()

    @Slot(str)
    def setCurrentExperimentDatasetName(self, name):
        self.lc.state.setCurrentExperimentDatasetName(name)
        self.experimentDataChanged.emit()
        self.projectInfoChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # EXPERIMENT
    ####################################################################################################################
    ####################################################################################################################

    @Property(str, notify=experimentDataAsXmlChanged)
    def experimentDataAsXml(self):
        return self.lc.state._experiment_data_as_xml

    def _setExperimentDataAsXml(self):
        print("+ _setExperimentDataAsXml")
        self.lc.state._setExperimentDataAsXml()
        self.experimentDataAsXmlChanged.emit()

    def _onExperimentDataChanged(self):
        print("***** _onExperimentDataChanged")
        self._setExperimentDataAsXml()
        self.stateChanged.emit(True)

    ####################################################################################################################
    # Experiment data: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addExperimentDataFromXye(self, file_url):
        self.lc.state.addExperimentDataFromXye(file_url)
        self._onExperimentDataAdded()
        self.experimentLoadedChanged.emit()

    @Slot()
    def removeExperiment(self):
        print("+ removeExperiment")
        self.lc.state.removeExperiment()
        self._onExperimentDataRemoved()
        self.experimentLoadedChanged.emit()

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        return self.lc.state._loadExperimentData(file_url)

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        self.lc._onExperimentDataAdded()

    def _onExperimentDataRemoved(self):
        print("***** _onExperimentDataRemoved")
        self.lc.chartsLogic._plotting_1d_proxy.clearFrontendState()
        self.experimentDataChanged.emit()

    ####################################################################################################################
    # Experiment loaded and skipped flags
    ####################################################################################################################

    @Property(bool, notify=experimentLoadedChanged)
    def experimentLoaded(self):
        return self.lc.state._experiment_loaded

    @experimentLoaded.setter
    def experimentLoaded(self, loaded: bool):
        self.lc.state.experimentLoaded(loaded)
        self.experimentLoadedChanged.emit()

    @Property(bool, notify=experimentSkippedChanged)
    def experimentSkipped(self):
        return self.lc.state._experiment_skipped

    @experimentSkipped.setter
    def experimentSkipped(self, skipped: bool):
        self.lc.state.experimentSkipped(skipped)
        self.experimentSkippedChanged.emit()

    def _onExperimentLoadedChanged(self):
        print("***** _onExperimentLoadedChanged")
        if self.experimentLoaded:
            self._onParametersChanged()
            self._onInstrumentParametersChanged()
            self._onPatternParametersChanged()

    def _onExperimentSkippedChanged(self):
        print("***** _onExperimentSkippedChanged")
        if self.experimentSkipped:
            self._onParametersChanged()
            self._onInstrumentParametersChanged()
            self._onPatternParametersChanged()
            self.lc.state._updateCalculatedData()

    ####################################################################################################################
    # Simulation parameters
    ####################################################################################################################

    @Property('QVariant', notify=simulationParametersChanged)
    def simulationParametersAsObj(self):
        return self.lc.state._simulation_parameters_as_obj

    @simulationParametersAsObj.setter
    def simulationParametersAsObj(self, json_str):
        self.lc.state.simulationParametersAsObj(json_str)
        self.simulationParametersChanged.emit()

    def _onSimulationParametersChanged(self):
        print("***** _onSimulationParametersChanged")
        self.lc.state._updateCalculatedData()

    ####################################################################################################################
    # Pattern parameters (scale, zero_shift, backgrounds)
    ####################################################################################################################

    @Property('QVariant', notify=patternParametersAsObjChanged)
    def patternParametersAsObj(self):
        return self.lc.state._pattern_parameters_as_obj

    def _setPatternParametersAsObj(self):
        start_time = timeit.default_timer()
        self.lc.state._setPatternParametersAsObj()
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
        return self.lc.state._instrument_parameters_as_obj

    @Property(str, notify=instrumentParametersAsXmlChanged)
    def instrumentParametersAsXml(self):
        return self.lc.state._instrument_parameters_as_xml

    def _setInstrumentParametersAsObj(self):
        start_time = timeit.default_timer()
        self.lc.state._setInstrumentParametersAsObj()
        print("+ _setInstrumentParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsObjChanged.emit()

    def _setInstrumentParametersAsXml(self):
        start_time = timeit.default_timer()
        self.lc.state._setInstrumentParametersAsXml()
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
        return self.lc._background_proxy

    ####################################################################################################################
    ####################################################################################################################
    # ANALYSIS
    ####################################################################################################################
    ####################################################################################################################


    ####################################################################################################################
    # Fitables (parameters table from analysis tab & ...)
    ####################################################################################################################

    @Property('QVariant', notify=parametersAsObjChanged)
    def parametersAsObj(self):
        return self.lc.state._parameters_as_obj

    @Property(str, notify=parametersAsXmlChanged)
    def parametersAsXml(self):
        return self.lc.state._parameters_as_xml

    def _setParametersAsObj(self):
        start_time = timeit.default_timer()

        self.lc.state._setParametersAsObj()
        print("+ _setParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsObjChanged.emit()

    def _setParametersAsXml(self):
        start_time = timeit.default_timer()
        self.lc.state._setParametersAsXml()
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
        self.lc.state.setParametersFilterCriteria(new_criteria)
        self._onParametersChanged()

    ####################################################################################################################
    # Any parameter
    ####################################################################################################################

    @Slot(str, 'QVariant')
    def editParameter(self, obj_id: str, new_value: Union[bool, float, str]):
        self.lc.state.editParameter(obj_id, new_value)

    ####################################################################################################################
    # Minimizer
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def minimizerNames(self):
        return self.lc.fitLogic.fitter.available_engines

    @Property(int, notify=currentMinimizerChanged)
    def currentMinimizerIndex(self):
        return self.lc.fitLogic.currentMinimizerIndex()

    @currentMinimizerIndex.setter
    @property_stack_deco('Minimizer change')
    def currentMinimizerIndex(self, new_index: int):
        self.lc.fitLogic.setCurrentMinimizerIndex(new_index)

    def _onCurrentMinimizerChanged(self):
        print("***** _onCurrentMinimizerChanged")
        self.lc.fitLogic.onCurrentMinimizerChanged()

    # Minimizer method
    @Property('QVariant', notify=currentMinimizerChanged)
    def minimizerMethodNames(self):
        return self.lc.fitLogic.minimizerMethodNames()

    @Property(int, notify=currentMinimizerMethodChanged)
    def currentMinimizerMethodIndex(self):
        return self.lc.fitLogic._current_minimizer_method_index

    @currentMinimizerMethodIndex.setter
    @property_stack_deco('Minimizer method change')
    def currentMinimizerMethodIndex(self, new_index: int):
        self.lc.currentMinimizerMethodIndex(new_index)

    def _onCurrentMinimizerMethodChanged(self):
        print("***** _onCurrentMinimizerMethodChanged")

    ####################################################################################################################
    # Calculator
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def calculatorNames(self):
        names = [f'{name} (experimental)' if name in ['CrysFML', 'GSASII'] else name for name in self.lc._interface.available_interfaces]
        return names

    @Property(int, notify=currentCalculatorChanged)
    def currentCalculatorIndex(self):
        return self.lc.currentCalculatorIndex()

    @currentCalculatorIndex.setter
    @property_stack_deco('Calculation engine change')
    def currentCalculatorIndex(self, new_index: int):
        if self.lc.setCurrentCalculatorIndex(new_index):
            print("***** _onCurrentCalculatorChanged")
            self.lc.state._onCurrentCalculatorChanged()
            self.lc.state._updateCalculatedData()
            self.currentCalculatorChanged.emit()

    ####################################################################################################################
    # Fitting
    ####################################################################################################################

    @Slot()
    def fit(self):
        # Currently using python threads from the `threading` module,
        # since QThreads don't seem to properly work under macos
        self.lc.fitLogic.fit(self.lc.state._data)

    @Property('QVariant', notify=fitResultsChanged)
    def fitResults(self):
        return self.lc.fitLogic._fit_results

    @Property(bool, notify=fitFinishedNotify)
    def isFitFinished(self):
        return self.lc.fitLogic._fit_finished

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
        self.lc.state.setReport(report)

    @Slot(str)
    def saveReport(self, filepath):
        """
        Save the generated report to the specified file
        Currently only html
        """
        success = self.lc.state.saveReport(filepath)
        self.htmlExportingFinished.emit(success, filepath)

    ####################################################################################################################
    ####################################################################################################################
    # STATUS
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=statusInfoChanged)
    def statusModelAsObj(self):
        return self.lc.statusModelAsObj()

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        return self.lc.statusModelAsXml()

    def _onStatusInfoChanged(self):
        pass

    ####################################################################################################################
    ####################################################################################################################
    # Project examples
    ####################################################################################################################
    ####################################################################################################################

    @Property(str, notify=dummySignal)
    def projectExamplesAsXml(self):
        return self.lc.state.projectExamplesAsXml()

    ####################################################################################################################
    ####################################################################################################################
    # Screen recorder
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def screenRecorder(self):
        return self.lc._screen_recorder

    ####################################################################################################################
    ####################################################################################################################
    # State save/load
    ####################################################################################################################
    ####################################################################################################################

    @Slot()
    def saveProject(self):
        self.lc.state.saveProject()
        self.stateChanged.emit(False)

    @Slot(str)
    def loadProjectAs(self, filepath):
        self.lc.state._loadProjectAs(filepath)
        self.stateChanged.emit(False)

    @Slot()
    def loadProject(self):
        self.lc.state._loadProject()
        self.lc._background_proxy.onAsObjChanged()
        self.stateChanged.emit(False)

    @Slot(str)
    def loadExampleProject(self, filepath):
        self.lc.state._loadProjectAs(filepath)
        self.currentProjectPath = '--- EXAMPLE ---'
        self.stateChanged.emit(False)

    @Property(str, notify=dummySignal)
    def projectFilePath(self):
        return self.lc.state.project_save_filepath

    @Property(bool, notify=projectCreatedChanged)
    def projectCreated(self):
        return self.lc.state._project_created

    @projectCreated.setter
    def projectCreated(self, created: bool):
        if self.lc.state.setProjectCreated(created):
            self.projectCreatedChanged.emit()

    @Slot()
    def resetState(self):
        self.lc.state.resetState()
        self.lc.chartsLogic._plotting_1d_proxy.clearBackendState()
        self.lc.chartsLogic._plotting_1d_proxy.clearFrontendState()
        self.resetUndoRedoStack()
        self.stateChanged.emit(False)

    ####################################################################################################################
    # Undo/Redo stack operations
    ####################################################################################################################

    @Property(bool, notify=undoRedoChanged)
    def canUndo(self) -> bool:
        return self.lc.stackLogic.canUndo()

    @Property(bool, notify=undoRedoChanged)
    def canRedo(self) -> bool:
        return self.lc.stackLogic.canRedo()

    @Slot()
    def undo(self):
        self.lc.stackLogic.undo()

    @Slot()
    def redo(self):
        self.lc.stackLogic.redo()

    @Property(str, notify=undoRedoChanged)
    def undoText(self):
        return self.lc.stackLogic.undoText()

    @Property(str, notify=undoRedoChanged)
    def redoText(self):
        return self.lc.stackLogic.redoText()

    @Slot()
    def resetUndoRedoStack(self):

        self.lc.stackLogic.resetUndoRedoStack()
        self.undoRedoChanged.emit()
