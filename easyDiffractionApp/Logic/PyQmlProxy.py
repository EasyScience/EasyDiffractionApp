# noqa: E501
import os
import timeit

from typing import Union

from PySide2.QtCore import QObject, Slot, Signal, Property

from easyCore.Utils.UndoRedo import property_stack_deco
from easyDiffractionApp.Logic.LogicController import LogicController
from easyDiffractionApp.Logic.Proxies.Plotting1d import Plotting1dProxy
from easyDiffractionApp.Logic.Proxies.Plotting3d import Plotting3dProxy
from easyDiffractionApp.Logic.Proxies.Background import BackgroundProxy
from easyDiffractionApp.Logic.Proxies.Fitting import FittingProxy
from easyDiffractionApp.Logic.Proxies.Stack import StackProxy
from easyDiffractionApp.Logic.Proxies.Project import ProjectProxy


class PyQmlProxy(QObject):
    # SIGNALS

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

    currentCalculatorChanged = Signal()

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
        from easyDiffractionApp.Logic.LogicController import LogicController2
        self.lc2 = LogicController2(self)

        self.state = self.lc2.l_state  # temp hack

        ################## proxies #################
        self._fitting_proxy = FittingProxy(self, self.lc2)
        self._plotting_1d_proxy = Plotting1dProxy(logic=self.lc2)
        self._plotting_3d_proxy = Plotting3dProxy(logic=self.lc2)
        self._background_proxy = BackgroundProxy(self, logic=self.lc2)
        self._stack_proxy = StackProxy(self, logic=self.lc2)
        self._project_proxy = ProjectProxy(self, logic=self.lc2)


        # initialize the logic controller - soon to be redundant!
        interface = self.lc2.interface
        self.lc = LogicController(self, state=self.state, interface=interface)

        ####################################################################################################################
        ####################################################################################################################
        # SIGNALS
        ####################################################################################################################
        ####################################################################################################################

         # Structure
        self.structureParametersChanged.connect(self._onStructureParametersChanged)
        self.structureParametersChanged.connect(self.lc2.l_state._updateCalculatedData())

        self.lc2.phaseAdded.connect(self._onPhaseAdded)
        self.lc2.phaseAdded.connect(self.phasesEnabled)

        self.currentPhaseChanged.connect(self._onCurrentPhaseChanged)

        # Experiment
        self.experimentDataChanged.connect(self._onExperimentDataChanged)

        self.experimentLoadedChanged.connect(self._onExperimentLoadedChanged)
        self.experimentSkippedChanged.connect(self._onExperimentSkippedChanged)

        # Analysis
        self.simulationParametersChanged.connect(self._onSimulationParametersChanged)
        self.simulationParametersChanged.connect(self._stack_proxy.undoRedoChanged)

        # self.currentMinimizerChanged.connect(self._onCurrentMinimizerChanged)
        # self.currentMinimizerMethodChanged.connect(self._onCurrentMinimizerMethodChanged)

        # Status info
        self.statusInfoChanged.connect(self._onStatusInfoChanged)
        self.currentCalculatorChanged.connect(self.statusInfoChanged)
        self._fitting_proxy.currentMinimizerChanged.connect(self.statusInfoChanged)
        self._fitting_proxy.currentMinimizerMethodChanged.connect(self.statusInfoChanged)

        # start the undo/redo stack
        self.lc2.initializeBorg()

    ####################################################################################################################
    ####################################################################################################################
    # Proxies
    ####################################################################################################################
    ####################################################################################################################

    # 1d plotting
    @Property('QVariant', notify=dummySignal)
    def plotting1d(self):
        return self._plotting_1d_proxy

    # 3d plotting
    @Property('QVariant', notify=dummySignal)
    def plotting3d(self):
        return self._plotting_3d_proxy

    # background
    @Property('QVariant', notify=dummySignal)
    def background(self):
        return self._background_proxy

    # fitting
    @Property('QVariant', notify=dummySignal)
    def fitting(self):
        return self._fitting_proxy

    # stack
    @Property('QVariant', notify=dummySignal)
    def stack(self):
        return self._stack_proxy

    # project
    @Property('QVariant', notify=dummySignal)
    def project(self):
        return self._project_proxy

    ####################################################################################################################
    # Phase models (list, xml, cif)
    ####################################################################################################################

    @Property('QVariant', notify=phasesAsObjChanged)
    def phasesAsObj(self):
        return self.lc2.l_state._phases_as_obj

    @Property(str, notify=phasesAsXmlChanged)
    def phasesAsXml(self):
        return self.lc2.l_state._phases_as_xml

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsCif(self):
        return self.lc2.l_state._phases_as_cif

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsExtendedCif(self):
        return self.lc2.l_state.phasesAsExtendedCif()

    @phasesAsCif.setter
    @property_stack_deco
    def phasesAsCif(self, phases_as_cif):
        self.lc2.l_state.phasesAsCif(phases_as_cif)
        self.lc2.parametersChanged.emit()

    def _setPhasesAsObj(self):
        start_time = timeit.default_timer()
        self.lc2.l_state._setPhasesAsObj()
        print("+ _setPhasesAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsObjChanged.emit()

    def _setPhasesAsXml(self):
        start_time = timeit.default_timer()
        self.lc2.l_state._setPhasesAsXml()
        print("+ _setPhasesAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsXmlChanged.emit()

    def _setPhasesAsCif(self):
        start_time = timeit.default_timer()
        self.lc2.l_state._setPhasesAsCif()
        print("+ _setPhasesAsCif: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsCifChanged.emit()

    def _onStructureParametersChanged(self):
        print("***** _onStructureParametersChanged")
        self._setPhasesAsObj()  # 0.025 s
        self._setPhasesAsXml()  # 0.065 s
        self._setPhasesAsCif()  # 0.010 s
        self._project_proxy.stateChanged.emit(True)

    ####################################################################################################################
    # Phase: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addSampleFromCif(self, cif_url):
        self.lc2.l_state.addSampleFromCif(cif_url)
        self.lc2.phaseAdded.emit()

    @Slot()
    def addDefaultPhase(self):
        print("+ addDefaultPhase")
        self.lc2.l_state.addDefaultPhase()
        self.lc2.phaseAdded.emit()

    @Slot(str)
    def removePhase(self, phase_name: str):
        self.lc2.removePhase(phase_name)

    def _onPhaseAdded(self):
        print("***** _onPhaseAdded")
        self.lc2._onPhaseAdded()
        self.phasesEnabled.emit()
        self.structureParametersChanged.emit()
        self._project_proxy.projectInfoChanged.emit()

    @Property(bool, notify=phasesEnabled)
    def samplesPresent(self) -> bool:
        return self.lc2.samplesPresent()

    ####################################################################################################################
    # Phase: Symmetry
    ####################################################################################################################

    # Crystal system

    @Property('QVariant', notify=structureParametersChanged)
    def crystalSystemList(self):
        return self.lc2.l_state.crystalSystemList()

    @Property(str, notify=structureParametersChanged)
    def currentCrystalSystem(self):
        return self.lc2.l_state.currentCrystalSystem()

    @currentCrystalSystem.setter
    def currentCrystalSystem(self, new_system: str):
        self.lc2.l_state.setCurrentCrystalSystem(new_system)
        self.structureParametersChanged.emit()

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupList(self):
        return self.lc2.l_state.formattedSpaceGroupList()

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroup(self):
        return self.lc2.l_state.getCurrentSpaceGroup()

    @currentSpaceGroup.setter
    def currentSpaceGroup(self, new_idx: int):
        self.lc2.l_state.currentSpaceGroup(new_idx)
        self.structureParametersChanged.emit()

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupSettingList(self):
        return self.lc2.l_state.formattedSpaceGroupSettingList()

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroupSetting(self):
        return self.lc2.l_state.currentSpaceGroupSetting()

    @currentSpaceGroupSetting.setter
    def currentSpaceGroupSetting(self, new_number: int):
        self.lc2.l_state.setCurrentSpaceGroupSetting(new_number)
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Phase: Atoms
    ####################################################################################################################

    @Slot()
    def addDefaultAtom(self):
        try:
            self.lc2.l_state.addDefaultAtom()
            self.structureParametersChanged.emit()
        except AttributeError:
            print("Error: failed to add atom")

    @Slot(str)
    def removeAtom(self, atom_label: str):
        self.lc2.l_state.removeAtom(atom_label)
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Current phase
    ####################################################################################################################

    @Property(int, notify=currentPhaseChanged)
    def currentPhaseIndex(self):
        return self.lc2.l_state._current_phase_index

    @currentPhaseIndex.setter
    def currentPhaseIndex(self, new_index: int):
        if self.lc2.l_state.currentPhaseIndex(new_index):
            self.currentPhaseChanged.emit()

    def _onCurrentPhaseChanged(self):
        print("***** _onCurrentPhaseChanged")
        self.structureViewChanged.emit()

    @Slot(str)
    def setCurrentPhaseName(self, name):
        self.lc2.l_state.setCurrentPhaseName(name)
        self.lc2.parametersChanged.emit()
        self._project_proxy.projectInfoChanged.emit()

    @Property('QVariant', notify=experimentDataChanged)
    def experimentDataAsObj(self):
        return self.lc2.l_state.experimentDataAsObj()

    @Slot(str)
    def setCurrentExperimentDatasetName(self, name):
        self.lc2.l_state.setCurrentExperimentDatasetName(name)
        self.experimentDataChanged.emit()
        self._project_proxy.projectInfoChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # EXPERIMENT
    ####################################################################################################################
    ####################################################################################################################

    @Property(str, notify=experimentDataAsXmlChanged)
    def experimentDataAsXml(self):
        return self.lc2.l_state._experiment_data_as_xml

    def _setExperimentDataAsXml(self):
        print("+ _setExperimentDataAsXml")
        self.lc2.l_state._setExperimentDataAsXml()
        self.experimentDataAsXmlChanged.emit()

    def _onExperimentDataChanged(self):
        print("***** _onExperimentDataChanged")
        self._setExperimentDataAsXml()
        self._project_proxy.stateChanged.emit(True)

    ####################################################################################################################
    # Experiment data: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addExperimentDataFromXye(self, file_url):
        self.lc2.l_state.addExperimentDataFromXye(file_url)
        self._onExperimentDataAdded()
        self.experimentLoadedChanged.emit()

    @Slot()
    def removeExperiment(self):
        print("+ removeExperiment")
        self.lc2.l_state.removeExperiment()
        self._onExperimentDataRemoved()
        self.experimentLoadedChanged.emit()

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        return self.lc2.l_state._loadExperimentData(file_url)

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        self.lc2._onExperimentDataAdded()

    def _onExperimentDataRemoved(self):
        print("***** _onExperimentDataRemoved")
        self.lc2.chartsLogic._plotting_1d_proxy.clearFrontendState()
        self.experimentDataChanged.emit()

    ####################################################################################################################
    # Experiment loaded and skipped flags
    ####################################################################################################################

    @Property(bool, notify=experimentLoadedChanged)
    def experimentLoaded(self):
        return self.lc2.l_state._experiment_loaded

    @experimentLoaded.setter
    def experimentLoaded(self, loaded: bool):
        self.lc2.l_state.experimentLoaded(loaded)
        self.experimentLoadedChanged.emit()

    @Property(bool, notify=experimentSkippedChanged)
    def experimentSkipped(self):
        return self.lc2.l_state._experiment_skipped

    @experimentSkipped.setter
    def experimentSkipped(self, skipped: bool):
        self.lc2.l_state.experimentSkipped(skipped)
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
            self.lc2.l_state._updateCalculatedData()

    ####################################################################################################################
    # Simulation parameters
    ####################################################################################################################

    @Property('QVariant', notify=simulationParametersChanged)
    def simulationParametersAsObj(self):
        return self.lc2.l_state._simulation_parameters_as_obj

    @simulationParametersAsObj.setter
    def simulationParametersAsObj(self, json_str):
        self.lc2.l_state.simulationParametersAsObj(json_str)
        self.simulationParametersChanged.emit()

    def _onSimulationParametersChanged(self):
        print("***** _onSimulationParametersChanged")
        self.lc2.l_state._updateCalculatedData()

    ####################################################################################################################
    # Pattern parameters (scale, zero_shift, backgrounds)
    ####################################################################################################################

    @Property('QVariant', notify=patternParametersAsObjChanged)
    def patternParametersAsObj(self):
        return self.lc2.l_state._pattern_parameters_as_obj

    def _setPatternParametersAsObj(self):
        start_time = timeit.default_timer()
        self.lc2.l_state._setPatternParametersAsObj()
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
        return self.lc2.l_state._instrument_parameters_as_obj

    @Property(str, notify=instrumentParametersAsXmlChanged)
    def instrumentParametersAsXml(self):
        return self.lc2.l_state._instrument_parameters_as_xml

    def _setInstrumentParametersAsObj(self):
        start_time = timeit.default_timer()
        self.lc2.l_state._setInstrumentParametersAsObj()
        print("+ _setInstrumentParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsObjChanged.emit()

    def _setInstrumentParametersAsXml(self):
        start_time = timeit.default_timer()
        self.lc2.l_state._setInstrumentParametersAsXml()
        print("+ _setInstrumentParametersAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsXmlChanged.emit()

    def _onInstrumentParametersChanged(self):
        print("***** _onInstrumentParametersChanged")
        self._setInstrumentParametersAsObj()
        self._setInstrumentParametersAsXml()

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
        return self.lc2.l_state._parameters_as_obj

    @Property(str, notify=parametersAsXmlChanged)
    def parametersAsXml(self):
        return self.lc2.l_state._parameters_as_xml

    def _setParametersAsObj(self):
        start_time = timeit.default_timer()

        self.lc2.l_state._setParametersAsObj()
        print("+ _setParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsObjChanged.emit()

    def _setParametersAsXml(self):
        start_time = timeit.default_timer()
        self.lc2.l_state._setParametersAsXml()
        print("+ _setParametersAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsXmlChanged.emit()

    def _onParametersChanged(self):
        print("***** _onParametersChanged")
        self._setParametersAsObj()
        self._setParametersAsXml()
        self._project_proxy.stateChanged.emit(True)

    # Filtering
    @Slot(str)
    def setParametersFilterCriteria(self, new_criteria):
        self.lc2.l_state.setParametersFilterCriteria(new_criteria)
        self._onParametersChanged()

    ####################################################################################################################
    # Any parameter
    ####################################################################################################################

    @Slot(str, 'QVariant')
    def editParameter(self, obj_id: str, new_value: Union[bool, float, str]):
        self.lc2.l_state.editParameter(obj_id, new_value)

    ####################################################################################################################
    ####################################################################################################################
    # STATUS
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=statusInfoChanged)
    def statusModelAsObj(self):
        return self.lc2.statusModelAsObj()

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        return self.lc2.statusModelAsXml()

    def _onStatusInfoChanged(self):
        pass

    ####################################################################################################################
    ####################################################################################################################
    # Project examples
    ####################################################################################################################
    ####################################################################################################################

    @Property(str, notify=dummySignal)
    def projectExamplesAsXml(self):
        return self.lc2.l_project.projectExamplesAsXml()

    ####################################################################################################################
    ####################################################################################################################
    # Screen recorder
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def screenRecorder(self):
        return self.lc2._screen_recorder
