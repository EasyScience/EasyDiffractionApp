import json

from PySide2.QtCore import QObject, Signal

from easyDiffractionLib.interface import InterfaceFactory

from easyDiffractionApp.Logic.Proxies.Background import BackgroundProxy
from easyDiffractionApp.Logic.State import State
from easyDiffractionApp.Logic.Fitter import FitterLogic as FitterLogic
from easyDiffractionApp.Logic.Stack import StackLogic
from easyDiffractionApp.Logic.Charts import ChartsLogic


class LogicController(QObject):
    parametersChanged = Signal()
    phaseAdded = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.proxy = parent
        self._fit_results = ""
        self._interface = InterfaceFactory()

        self.initialize()

    def initialize(self):
        # initialize various logic components

        # main logic
        self.state = State(self, interface=self._interface, proxy=self.proxy)
        # self.stateChanged.connect(self._onStateChanged)

        # chart logic
        self.chartsLogic = ChartsLogic(self)

        # stack logic
        no_history = [self.parametersChanged]
        with_history = [self.phaseAdded, self.parametersChanged]
        self.stackLogic = StackLogic(self,
                                     callbacks_no_history=no_history,
                                     callbacks_with_history=with_history)

        # fitter logic
        #####################################################
        self.fitLogic = FitterLogic(self, self.state._sample,
                                    self._interface.fit_func)
        self._fit_results = self.fitLogic._defaultFitResults()
        # communication between logic and proxy notifiers
        self.fitLogic.fitFinished.connect(self.onFitFinished)
        self.fitLogic.fitStarted.connect(self.onFitStarted)

        # background logic
        self._background_proxy = BackgroundProxy(self.proxy)
        self._background_proxy.asObjChanged.connect(self.proxy._onParametersChanged)
        self._background_proxy.asObjChanged.connect(self.state._sample.set_background)
        self._background_proxy.asObjChanged.connect(self.state._updateCalculatedData)
        self._background_proxy.asXmlChanged.connect(self.updateChartBackground)

        # parameters slots
        self.parametersChanged.connect(self.proxy._onParametersChanged)
        self.parametersChanged.connect(self.state._updateCalculatedData)
        self.parametersChanged.connect(self.chartsLogic._onStructureViewChanged)
        self.parametersChanged.connect(self.proxy._onStructureParametersChanged)
        self.parametersChanged.connect(self.proxy._onPatternParametersChanged)
        self.parametersChanged.connect(self.proxy._onInstrumentParametersChanged)
        self.parametersChanged.connect(self._background_proxy.onAsObjChanged)
        self.parametersChanged.connect(self.proxy.undoRedoChanged)

        # Screen recorder
        self._screen_recorder = self.recorder()

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

    @property
    def _background_obj(self):
        bgs = self.state._sample.pattern.backgrounds
        itm = None
        if len(bgs) > 0:
            itm = bgs[0]
        return itm

    def updateChartBackground(self):
        if self._background_proxy.asObj is None:
            return
        self.chartsLogic._plotting_1d_proxy.setBackgroundData(
                                self._background_proxy.asObj.x_sorted_points,
                                self._background_proxy.asObj.y_sorted_points)

    def onFitStarted(self):
        self.proxy.fitFinishedNotify.emit()

    def onFitFinished(self):
        self.proxy.fitResultsChanged.emit()
        self.proxy.fitFinishedNotify.emit()
        self.parametersChanged.emit()

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        self.chartsLogic._plotting_1d_proxy.setMeasuredData(
                                            self.state._experiment_data.x,
                                            self.state._experiment_data.y,
                                            self.state._experiment_data.e)
        self.state._experiment_parameters = \
            self.state._experimentDataParameters(self.state._experiment_data)

        self.proxy.simulationParametersAsObj = \
            json.dumps(self.state._experiment_parameters)
        if len(self.state._sample.pattern.backgrounds) == 0:
            self._background_proxy.initializeContainer()

        self.proxy.experimentDataChanged.emit()
        self.proxy.projectInfoAsJson['experiments'] = \
            self.state._data.experiments[0].name
        self.proxy.projectInfoChanged.emit()

    def _onPhaseAdded(self):
        self.state._onPhaseAdded(self._background_proxy.asObj)

    def samplesPresent(self):
        return len(self.state._sample.phases) > 0

