
from PySide2.QtCore import QObject, Signal, Slot, Property


class ExperimentProxy(QObject):

    dummySignal = Signal()
    experimentDataChanged = Signal()
    projectInfoChanged = Signal()
    stateChanged = Signal()
    experimentDataAsXmlChanged = Signal()
    experimentLoadedChanged = Signal()
    experimentSkippedChanged = Signal()

    def __init__(self, parent=None, logic=None):  # , interface=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_experiment
        self.logic.experimentLoadedChanged.connect(self.experimentLoadedChanged)
        self.logic.experimentSkippedChanged.connect(self.experimentSkippedChanged)

    @Property('QVariant', notify=experimentDataChanged)
    def experimentDataAsObj(self):
        return self.logic.experimentDataAsObj()

    @Slot(str)
    def setCurrentExperimentDatasetName(self, name):
        self.logic.setCurrentExperimentDatasetName(name)
        self.experimentDataChanged.emit()
        self.parent.project.projectInfoChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # EXPERIMENT
    ####################################################################################################################
    ####################################################################################################################

    @Property(str, notify=experimentDataAsXmlChanged)
    def experimentDataAsXml(self):
        return self.logic._experiment_data_as_xml

    def _setExperimentDataAsXml(self):
        print("+ _setExperimentDataAsXml")
        self.logic._setExperimentDataAsXml()
        self.experimentDataAsXmlChanged.emit()

    def _onExperimentDataChanged(self):
        print("***** _onExperimentDataChanged")
        self._setExperimentDataAsXml()
        self.parent.project.stateChanged.emit(True)

    ####################################################################################################################
    # Experiment data: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addExperimentDataFromXye(self, file_url):
        self.logic.addExperimentDataFromXye(file_url)
        self.logic._onExperimentDataAdded()
        self.experimentLoadedChanged.emit()

    @Slot()
    def removeExperiment(self):
        print("+ removeExperiment")
        self.logic.removeExperiment()
        self._onExperimentDataRemoved()
        self.experimentLoadedChanged.emit()

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        return self.logic._loadExperimentData(file_url)

    def _onExperimentDataRemoved(self):
        print("***** _onExperimentDataRemoved")
        self.lc.chartsLogic._plotting_1d_proxy.clearFrontendState()
        self.experimentDataChanged.emit()

    @Property(bool, notify=experimentLoadedChanged)
    def experimentLoaded(self):
        return self.logic._experiment_loaded

    @experimentLoaded.setter
    def experimentLoaded(self, loaded: bool):
        self.logic.experimentLoaded(loaded)
        self.experimentLoadedChanged.emit()

    @Property(bool, notify=experimentSkippedChanged)
    def experimentSkipped(self):
        return self.logic._experiment_skipped

    @experimentSkipped.setter
    def experimentSkipped(self, skipped: bool):
        self.logic.experimentSkipped(skipped)
        self.experimentSkippedChanged.emit()

    def _onExperimentLoadedChanged(self):
        print("***** _onExperimentLoadedChanged")
        if self.experimentLoaded:
            self.parent._onParametersChanged()
            self.parent._onInstrumentParametersChanged()
            self.logic._onPatternParametersChanged()

    def _onExperimentSkippedChanged(self):
        print("***** _onExperimentSkippedChanged")
        if self.experimentSkipped:
            self.parent._onParametersChanged()
            self.parent._onInstrumentParametersChanged()
            self.parent_onPatternParametersChanged()
            self.logic._onExperimentSkippedChanged()
