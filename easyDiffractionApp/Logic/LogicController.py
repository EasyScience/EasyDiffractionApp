from PySide2.QtCore import QObject, Signal

# from easyDiffractionApp.Logic.State import State

from easyDiffractionApp.Logic.Proxies.Background import BackgroundProxy
from easyDiffractionApp.Logic.Fitter import FitterLogic as FitterLogic
from easyDiffractionApp.Logic.Stack import StackLogic
from easyDiffractionApp.Logic.Charts import ChartsLogic


class LogicController(QObject):
    parametersChanged = Signal()
    phaseAdded = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._fit_results = ""

        self.initialize()

    def initialize(self):
        # initialize various logic components

        # main logic
        # self.state = State(self, interface=self._interface)
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
        self.fitLogic = FitterLogic(self, self.parent.state._sample,
                                    self.parent._interface.fit_func)
        self._fit_results = self.fitLogic._defaultFitResults()
        # communication between logic and proxy notifiers
        self.fitLogic.fitFinished.connect(self.onFitFinished)
        self.fitLogic.fitStarted.connect(self.onFitStarted)

        # background logic
        self._background_proxy = BackgroundProxy(self.parent)
        self._background_proxy.asObjChanged.connect(self.parent._onParametersChanged)
        self._background_proxy.asObjChanged.connect(self.parent.state._sample.set_background)
        self._background_proxy.asObjChanged.connect(self.parent.calculatedDataChanged)
        self._background_proxy.asXmlChanged.connect(self.updateChartBackground)

        # parameters slots
        # Parameters
        self.parametersChanged.connect(self.parent._onParametersChanged)
        self.parametersChanged.connect(self.parent._onCalculatedDataChanged)
        self.parametersChanged.connect(self.parent._onStructureViewChanged)
        self.parametersChanged.connect(self.parent._onStructureParametersChanged)
        self.parametersChanged.connect(self.parent._onPatternParametersChanged)
        self.parametersChanged.connect(self.parent._onInstrumentParametersChanged)
        self.parametersChanged.connect(self._background_proxy.onAsObjChanged)
        self.parametersChanged.connect(self.parent.undoRedoChanged)

    @property
    def _background_obj(self):
        # this will change to self.state._sample... after refactoring State
        bgs = self.parent.state._sample.pattern.backgrounds
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
        self.parent.fitFinishedNotify.emit()

    def onFitFinished(self):
        self.parent.fitResultsChanged.emit()
        self.parent.fitFinishedNotify.emit()
        self.parametersChanged.emit()
