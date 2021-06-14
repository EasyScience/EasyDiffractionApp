# noqa: E501
import timeit

from typing import Union

from PySide2.QtCore import QObject, Slot, Signal, Property

from easyCore.Utils.UndoRedo import property_stack_deco

from easyDiffractionApp.Logic.LogicController import LogicController
from easyDiffractionApp.Logic.Proxies.Background import BackgroundProxy
from easyDiffractionApp.Logic.Proxies.Experiment import ExperimentProxy
from easyDiffractionApp.Logic.Proxies.Fitting import FittingProxy
from easyDiffractionApp.Logic.Proxies.Phase import PhaseProxy
from easyDiffractionApp.Logic.Proxies.Plotting1d import Plotting1dProxy
from easyDiffractionApp.Logic.Proxies.Plotting3d import Plotting3dProxy
from easyDiffractionApp.Logic.Proxies.Project import ProjectProxy
from easyDiffractionApp.Logic.Proxies.Stack import StackProxy


class PyQmlProxy(QObject):
    # SIGNALS

    # Fitables
    parametersAsObjChanged = Signal()
    parametersAsXmlChanged = Signal()

    # Experiment
    patternParametersAsObjChanged = Signal()

    instrumentParametersAsObjChanged = Signal()
    instrumentParametersAsXmlChanged = Signal()

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
        self._phase_proxy = PhaseProxy(self, logic=self.lc)

        ####################################################################################################################
        ####################################################################################################################
        # SIGNALS
        ####################################################################################################################
        ####################################################################################################################

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

    # phase
    @Property('QVariant', notify=dummySignal)
    def phase(self):
        return self._phase_proxy

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
