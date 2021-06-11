# noqa: E501
import timeit

from typing import Union

from PySide2.QtCore import QObject, Slot, Signal, Property

from easyCore.Utils.UndoRedo import property_stack_deco

from easyDiffractionApp.Logic.LogicController import LogicController
from easyDiffractionApp.Logic.Proxies.Background import BackgroundProxy
from easyDiffractionApp.Logic.Proxies.Experiment import ExperimentProxy
from easyDiffractionApp.Logic.Proxies.Fitting import FittingProxy
from easyDiffractionApp.Logic.Proxies.Plotting1d import Plotting1dProxy
from easyDiffractionApp.Logic.Proxies.Plotting3d import Plotting3dProxy
from easyDiffractionApp.Logic.Proxies.Project import ProjectProxy
from easyDiffractionApp.Logic.Proxies.Stack import StackProxy


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

    # experimentDataChanged = Signal()
    # experimentDataAsXmlChanged = Signal()

    # experimentLoadedChanged = Signal()
    # experimentSkippedChanged = Signal()

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
        self.lc = LogicController(self)

        ################## proxies #################
        self._fitting_proxy = FittingProxy(self, self.lc)
        self._plotting_1d_proxy = Plotting1dProxy(logic=self.lc)
        self._plotting_3d_proxy = Plotting3dProxy(logic=self.lc)
        self._background_proxy = BackgroundProxy(self, logic=self.lc)
        self._stack_proxy = StackProxy(self, logic=self.lc)
        self._project_proxy = ProjectProxy(self, logic=self.lc)
        self._experiment_proxy = ExperimentProxy(self, logic=self.lc)


        ####################################################################################################################
        ####################################################################################################################
        # SIGNALS
        ####################################################################################################################
        ####################################################################################################################

        # Structure
        self.structureParametersChanged.connect(self._onStructureParametersChanged)
        self.structureParametersChanged.connect(self.lc.l_state._updateCalculatedData())

        self.lc.phaseAdded.connect(self._onPhaseAdded)
        self.lc.phaseAdded.connect(self.phasesEnabled)

        self.currentPhaseChanged.connect(self._onCurrentPhaseChanged)

        # Experiment
        # self.experimentDataChanged.connect(self._onExperimentDataChanged)

        # self.experimentLoadedChanged.connect(self._onExperimentLoadedChanged)
        # self.experimentSkippedChanged.connect(self._onExperimentSkippedChanged)

        # Analysis
        self.simulationParametersChanged.connect(self._onSimulationParametersChanged)
        self.simulationParametersChanged.connect(self._stack_proxy.undoRedoChanged)

        # Status info
        self.statusInfoChanged.connect(self._onStatusInfoChanged)
        self.currentCalculatorChanged.connect(self.statusInfoChanged)
        self._fitting_proxy.currentMinimizerChanged.connect(self.statusInfoChanged)
        self._fitting_proxy.currentMinimizerMethodChanged.connect(self.statusInfoChanged)

        # start the undo/redo stack
        self.lc.initializeBorg()

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

    # experiment
    @Property('QVariant', notify=dummySignal)
    def experiment(self):
        return self._experiment_proxy

    # fitting
    @Property('QVariant', notify=dummySignal)
    def fitting(self):
        return self._fitting_proxy

    # project
    @Property('QVariant', notify=dummySignal)
    def project(self):
        return self._project_proxy

    # stack
    @Property('QVariant', notify=dummySignal)
    def stack(self):
        return self._stack_proxy


    ####################################################################################################################
    # Phase models (list, xml, cif)
    ####################################################################################################################

    @Property('QVariant', notify=phasesAsObjChanged)
    def phasesAsObj(self):
        return self.lc.l_state._phases_as_obj

    @Property(str, notify=phasesAsXmlChanged)
    def phasesAsXml(self):
        return self.lc.l_state._phases_as_xml

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsCif(self):
        return self.lc.l_state._phases_as_cif

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsExtendedCif(self):
        return self.lc.l_state.phasesAsExtendedCif()

    @phasesAsCif.setter
    @property_stack_deco
    def phasesAsCif(self, phases_as_cif):
        self.lc.l_state.phasesAsCif(phases_as_cif)
        self.lc.parametersChanged.emit()

    def _setPhasesAsObj(self):
        start_time = timeit.default_timer()
        self.lc.l_state._setPhasesAsObj()
        print("+ _setPhasesAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsObjChanged.emit()

    def _setPhasesAsXml(self):
        start_time = timeit.default_timer()
        self.lc.l_state._setPhasesAsXml()
        print("+ _setPhasesAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsXmlChanged.emit()

    def _setPhasesAsCif(self):
        start_time = timeit.default_timer()
        self.lc.l_state._setPhasesAsCif()
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
        self.lc.l_state.addSampleFromCif(cif_url)
        self.lc.phaseAdded.emit()

    @Slot()
    def addDefaultPhase(self):
        print("+ addDefaultPhase")
        self.lc.l_state.addDefaultPhase()
        self.lc.phaseAdded.emit()

    @Slot(str)
    def removePhase(self, phase_name: str):
        self.lc.removePhase(phase_name)

    def _onPhaseAdded(self):
        print("***** _onPhaseAdded")
        self.lc._onPhaseAdded()
        self.phasesEnabled.emit()
        self.structureParametersChanged.emit()
        self._project_proxy.projectInfoChanged.emit()

    @Property(bool, notify=phasesEnabled)
    def samplesPresent(self) -> bool:
        return self.lc.samplesPresent()

    ####################################################################################################################
    # Phase: Symmetry
    ####################################################################################################################

    # Crystal system

    @Property('QVariant', notify=structureParametersChanged)
    def crystalSystemList(self):
        return self.lc.l_state.crystalSystemList()

    @Property(str, notify=structureParametersChanged)
    def currentCrystalSystem(self):
        return self.lc.l_state.currentCrystalSystem()

    @currentCrystalSystem.setter
    def currentCrystalSystem(self, new_system: str):
        self.lc.l_state.setCurrentCrystalSystem(new_system)
        self.structureParametersChanged.emit()

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupList(self):
        return self.lc.l_state.formattedSpaceGroupList()

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroup(self):
        return self.lc.l_state.getCurrentSpaceGroup()

    @currentSpaceGroup.setter
    def currentSpaceGroup(self, new_idx: int):
        self.lc.l_state.currentSpaceGroup(new_idx)
        self.structureParametersChanged.emit()

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupSettingList(self):
        return self.lc.l_state.formattedSpaceGroupSettingList()

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroupSetting(self):
        return self.lc.l_state.currentSpaceGroupSetting()

    @currentSpaceGroupSetting.setter
    def currentSpaceGroupSetting(self, new_number: int):
        self.lc.l_state.setCurrentSpaceGroupSetting(new_number)
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Phase: Atoms
    ####################################################################################################################

    @Slot()
    def addDefaultAtom(self):
        try:
            self.lc.l_state.addDefaultAtom()
            self.structureParametersChanged.emit()
        except AttributeError:
            print("Error: failed to add atom")

    @Slot(str)
    def removeAtom(self, atom_label: str):
        self.lc.l_state.removeAtom(atom_label)
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Current phase
    ####################################################################################################################

    @Property(int, notify=currentPhaseChanged)
    def currentPhaseIndex(self):
        return self.lc.l_state._current_phase_index

    @currentPhaseIndex.setter
    def currentPhaseIndex(self, new_index: int):
        if self.lc.l_state.currentPhaseIndex(new_index):
            self.currentPhaseChanged.emit()

    def _onCurrentPhaseChanged(self):
        print("***** _onCurrentPhaseChanged")
        self.structureViewChanged.emit()

    @Slot(str)
    def setCurrentPhaseName(self, name):
        self.lc.l_state.setCurrentPhaseName(name)
        self.lc.parametersChanged.emit()
        self._project_proxy.projectInfoChanged.emit()

    ####################################################################################################################
    # Simulation parameters
    ####################################################################################################################

    @Property('QVariant', notify=simulationParametersChanged)
    def simulationParametersAsObj(self):
        return self.lc.l_state._simulation_parameters_as_obj

    @simulationParametersAsObj.setter
    def simulationParametersAsObj(self, json_str):
        self.lc.l_state.simulationParametersAsObj(json_str)
        self.simulationParametersChanged.emit()

    def _onSimulationParametersChanged(self):
        print("***** _onSimulationParametersChanged")
        self.lc.l_state._updateCalculatedData()

    ####################################################################################################################
    # Pattern parameters (scale, zero_shift, backgrounds)
    ####################################################################################################################

    @Property('QVariant', notify=patternParametersAsObjChanged)
    def patternParametersAsObj(self):
        return self.lc.l_state._pattern_parameters_as_obj

    def _setPatternParametersAsObj(self):
        start_time = timeit.default_timer()
        self.lc.l_state._setPatternParametersAsObj()
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
        return self.lc.l_state._instrument_parameters_as_obj

    @Property(str, notify=instrumentParametersAsXmlChanged)
    def instrumentParametersAsXml(self):
        return self.lc.l_state._instrument_parameters_as_xml

    def _setInstrumentParametersAsObj(self):
        start_time = timeit.default_timer()
        self.lc.l_state._setInstrumentParametersAsObj()
        print("+ _setInstrumentParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsObjChanged.emit()

    def _setInstrumentParametersAsXml(self):
        start_time = timeit.default_timer()
        self.lc.l_state._setInstrumentParametersAsXml()
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
        return self.lc.l_state._parameters_as_obj

    @Property(str, notify=parametersAsXmlChanged)
    def parametersAsXml(self):
        return self.lc.l_state._parameters_as_xml

    def _setParametersAsObj(self):
        start_time = timeit.default_timer()

        self.lc.l_state._setParametersAsObj()
        print("+ _setParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsObjChanged.emit()

    def _setParametersAsXml(self):
        start_time = timeit.default_timer()
        self.lc.l_state._setParametersAsXml()
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
        self.lc.l_state.setParametersFilterCriteria(new_criteria)
        self._onParametersChanged()

    ####################################################################################################################
    # Any parameter
    ####################################################################################################################

    @Slot(str, 'QVariant')
    def editParameter(self, obj_id: str, new_value: Union[bool, float, str]):
        self.lc.l_state.editParameter(obj_id, new_value)

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
        return self.lc.l_project.projectExamplesAsXml()

    ####################################################################################################################
    ####################################################################################################################
    # Screen recorder
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def screenRecorder(self):
        return self.lc._screen_recorder
