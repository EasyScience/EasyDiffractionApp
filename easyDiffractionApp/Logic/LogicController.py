from easyDiffractionApp.Logic.Proxies.Project import ProjectProxy
from easyDiffractionApp.Logic.Background import BackgroundLogic
import json

from PySide2.QtCore import QObject, Signal

from easyDiffractionApp.Logic.Stack import StackLogic
from easyDiffractionApp.Logic.Plotting3d import Plotting3dLogic


class LogicController(QObject):
    parametersChanged = Signal()
    phaseAdded = Signal()

    def __init__(self, parent, state=None, interface=None):
        super().__init__(parent)
        self.proxy = parent
        self._fit_results = ""

        # temporary kludge
        self.state = state
        self._interface = interface

        self.initialize()
        self.mapSignals()

    def initialize(self):
        # initialize various logic components

        # stack logic
        # no_history = [self.parametersChanged]
        # with_history = [self.phaseAdded, self.parametersChanged]
        # self.stackLogic = StackLogic(self, self.proxy,
        #                              callbacks_no_history=no_history,
        #                              callbacks_with_history=with_history)

        self._background_proxy = self.proxy._background_proxy
        self._fitting_proxy = self.proxy._fitting_proxy
        # parameters slots
        self.parametersChanged.connect(self.proxy._onParametersChanged)
        self.parametersChanged.connect(self.state._updateCalculatedData)
        # self.parametersChanged.connect(self.chartsLogic._onStructureViewChanged)
        self.parametersChanged.connect(self.proxy._onStructureParametersChanged)
        self.parametersChanged.connect(self.proxy._onPatternParametersChanged)
        self.parametersChanged.connect(self.proxy._onInstrumentParametersChanged)
        self.parametersChanged.connect(self._background_proxy.logic.onAsObjChanged)
        self.parametersChanged.connect(self.proxy.undoRedoChanged)

        # Screen recorder
        self._screen_recorder = self.recorder()

    def mapSignals(self):
        """
        Map signals from logics to proxy
        Needed so logics don't call emit directly on proxy signals
        """
        # self.state.projectCreatedChanged.connect(self.proxy.project.projectCreatedChanged)
        self.state.parametersChanged.connect(self.proxy._onParametersChanged)
        self.state.experimentLoadedChanged.connect(self.proxy.experimentLoadedChanged)
        self.state.experimentSkippedChanged.connect(self.proxy.experimentSkippedChanged)
        self.state.phasesEnabled.connect(self.proxy.phasesEnabled)
        self.state.phasesAsObjChanged.connect(self.proxy.phasesAsObjChanged)
        # self.state.structureParametersChanged.connect(self.proxy.structureParametersChanged)
        # self.state.projectInfoChanged.connect(self.proxy.project.projectInfoChanged)
        self.state.experimentDataAdded.connect(self._onExperimentDataAdded)
        self.state.removePhaseSignal.connect(self.removePhase)

###############################################################################
#  MULTI-STATE UTILITY METHODS
###############################################################################

    def recorder(self):
        rec = None
        try:
            from easyDiffractionApp.Logic.ScreenRecorder import ScreenRecorder
            rec = ScreenRecorder()
        except (ImportError, ModuleNotFoundError):
            print('Screen recording disabled')
        return rec

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        self.proxy._plotting_1d_proxy.logic.setMeasuredData(
                                            self.state._experiment_data.x,
                                            self.state._experiment_data.y,
                                            self.state._experiment_data.e)
        self.state._experiment_parameters = \
            self.state._experimentDataParameters(self.state._experiment_data)

        self.proxy.simulationParametersAsObj = \
            json.dumps(self.state._experiment_parameters)

        # self.state.simulationParametersAsObj(json.dumps(self.state._experiment_parameters))

        if len(self.state._sample.pattern.backgrounds) == 0:
            self._background_proxy.logic.initializeContainer()

        self.proxy.experimentDataChanged.emit()
        self.proxy.projectInfoAsJson['experiments'] = \
            self.state._data.experiments[0].name

        self.proxy.projectInfoChanged.emit()

    def _onPhaseAdded(self):
        self.state._onPhaseAdded(self._background_proxy.asObj)

    def removePhase(self, phase_name: str):
        if self.state.removePhase(phase_name):
            self.proxy.structureParametersChanged.emit()
            self.proxy.phasesEnabled.emit()

    # def samplesPresent(self):
    #     return len(self.state._sample.phases) > 0

    # def statusModelAsObj(self):
    #     engine_name = self._fitting_proxy.logic.fitter.current_engine.name
    #     minimizer_name = self._fitting_proxy.logic._current_minimizer_method_name
    #     return self.state.statusModelAsObj(engine_name, minimizer_name)

    # def statusModelAsXml(self):
    #     engine_name = self._fitting_proxy.logic.fitter.current_engine.name
    #     minimizer_name = self._fitting_proxy.logic._current_minimizer_method_name
    #     return self.state.statusModelAsXml(engine_name, minimizer_name)


##########################################################################################
##########################################################################################

from easyDiffractionApp.Logic.Background import BackgroundLogic
from easyDiffractionApp.Logic.State import StateLogic
from easyDiffractionApp.Logic.Fitting import FittingLogic as FittingLogic
from easyDiffractionApp.Logic.Plotting1d import Plotting1dLogic
from easyDiffractionApp.Logic.Project import ProjectLogic
from easyDiffractionLib.interface import InterfaceFactory

class LogicController2(QObject):
    parametersChanged = Signal()
    phaseAdded = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.proxy = parent
        self.interface = InterfaceFactory()
        # instantiate logics
        self.initializeLogics()

        # define signal forwarders
        self.setupSignals()


    def initializeLogics(self):
        self.l_state = StateLogic(self, interface=self.interface)
        self.l_fitting = FittingLogic(self, state=self.l_state, interface=self.interface)
        self.l_plotting1d = Plotting1dLogic(self)
        self.l_plotting3d = Plotting3dLogic(self)
        self.l_background = BackgroundLogic(self, state=self.l_state)
        self.l_project = ProjectLogic(self, interface=self.interface)
        # stack logic
        no_history = [self.parametersChanged]
        with_history = [self.phaseAdded, self.parametersChanged]
        # TODO fix after phase logic implemented
        self.l_stack = StackLogic(self, self.proxy,
                                  callbacks_no_history=no_history,
                                  callbacks_with_history=with_history)

    def setupSignals(self):
       # background logic
        self.l_background.asObjChanged.connect(self.proxy._onParametersChanged)
        self.l_background.asObjChanged.connect(self.l_state._sample.set_background)
        self.l_background.asObjChanged.connect(self.l_state._updateCalculatedData)
        self.l_state.plotCalculatedDataSignal.connect(self.plotCalculatedData)
        self.l_state.plotBraggDataSignal.connect(self.plotBraggData)
        self.l_fitting.fitFinished.connect(self.onFitFinished)
        self.l_state.currentMinimizerIndex.connect(self.l_fitting.setCurrentMinimizerIndex)
        self.l_state.currentMinimizerMethodIndex.connect(self.l_fitting.currentMinimizerMethodIndex)
        self.l_state.undoRedoChanged.connect(self.l_stack.undoRedoChanged)
        self.l_state.parametersChanged.connect(self.parametersChanged)
        self.l_project.reset.connect(self.resetState)
        self.l_state.updateProjectInfo.connect(self.l_project.updateProjectInfo)
        self.l_state.experimentLoadedChanged.connect(self.proxy.experimentLoadedChanged)
        self.l_state.experimentSkippedChanged.connect(self.proxy.experimentSkippedChanged)
        self.l_state.phasesEnabled.connect(self.proxy.phasesEnabled)
        self.l_state.phasesAsObjChanged.connect(self.proxy.phasesAsObjChanged)
        self.l_state.experimentDataAdded.connect(self._onExperimentDataAdded)
        self.l_state.removePhaseSignal.connect(self.removePhase)

        self.l_project.phasesEnabled.connect(self.proxy.phasesEnabled)
        self.l_project.phasesAsObjChanged.connect(self.proxy.phasesAsObjChanged)
        self.l_project.structureParametersChanged.connect(self.proxy.structureParametersChanged)
        self.l_project.removePhaseSignal.connect(self.removePhase)
        self.l_project.experimentDataAdded.connect(self._onExperimentDataAdded)
        self.l_project.parametersChanged.connect(self.parametersChanged)
        self.l_project.experimentLoadedChanged.connect(self.proxy.experimentLoadedChanged)

        self.parametersChanged.connect(self.proxy._onParametersChanged)
        self.parametersChanged.connect(self.l_state._updateCalculatedData)
        self.parametersChanged.connect(self.proxy._onStructureParametersChanged)
        self.parametersChanged.connect(self.proxy._onPatternParametersChanged)
        self.parametersChanged.connect(self.proxy._onInstrumentParametersChanged)
        self.parametersChanged.connect(self.l_background.onAsObjChanged)
        self.parametersChanged.connect(self.proxy.undoRedoChanged)
 

    def resetFactory(self):
        self.interface = InterfaceFactory()

    def plotCalculatedData(self, data):
        self.l_plotting1d.setCalculatedData(data[0], data[1])

    def plotBraggData(self, data):
        self.l_plotting1d.setBraggData(data[0], data[1], data[2], data[3])  # noqa: E501

    def onFitFinished(self):
        self.parametersChanged.emit()

    def initializeBorg(self):
        self.l_stack.initializeBorg()

    def resetState(self):
        self.l_plotting1d.clearBackendState()
        self.l_plotting1d.clearFrontendState()
        self.l_stack.resetUndoRedoStack()

    def _onPhaseAdded(self):
        self.l_state._onPhaseAdded(self.l_background._background_as_obj)

    def removePhase(self, phase_name: str):
        if self.l_state.removePhase(phase_name):
            self.proxy.structureParametersChanged.emit()
            self.proxy.phasesEnabled.emit()

    def samplesPresent(self):
        return len(self.l_state._sample.phases) > 0

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        self.l_plotting1d.setMeasuredData(
                                          self.l_state._experiment_data.x,
                                          self.l_state._experiment_data.y,
                                          self.l_state._experiment_data.e)
        self.l_state._experiment_parameters = \
            self.l_state._experimentDataParameters(self.l_state._experiment_data)

        self.proxy.simulationParametersAsObj = \
            json.dumps(self.l_state._experiment_parameters)

        if len(self.l_state._sample.pattern.backgrounds) == 0:
            self.l_background.initializeContainer()

        self.proxy.experimentDataChanged.emit()
        self.l_project._project_info['experiments'] = \
            self.l_state._data.experiments[0].name
        
        self.l_project.projectInfoChanged.emit()

    def statusModelAsObj(self):
        engine_name = self.l_fitting.fitter.current_engine.name
        minimizer_name = self.l_fitting._current_minimizer_method_name
        return self.l_state.statusModelAsObj(engine_name, minimizer_name)

    def statusModelAsXml(self):
        engine_name = self.l_fitting.fitter.current_engine.name
        minimizer_name = self.l_fitting._current_minimizer_method_name
        return self.l_state.statusModelAsXml(engine_name, minimizer_name)

    def recorder(self):
        rec = None
        try:
            from easyDiffractionApp.Logic.ScreenRecorder import ScreenRecorder
            rec = ScreenRecorder()
        except (ImportError, ModuleNotFoundError):
            print('Screen recording disabled')
        return rec
