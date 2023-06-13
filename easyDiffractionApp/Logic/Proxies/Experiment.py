
# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import os
import timeit

from PySide2.QtCore import QObject, Signal, Slot, Property


class ExperimentProxy(QObject):

    dummySignal = Signal()
    experimentDataChanged = Signal()
    projectInfoChanged = Signal()
    stateChanged = Signal()
    experimentDataAsXmlChanged = Signal()
    experimentLoadedChanged = Signal()
    experimentSkippedChanged = Signal()

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_experiment
        self.logic.experimentLoadedChanged.connect(self.experimentLoadedChanged)
        self.logic.experimentSkippedChanged.connect(self.experimentSkippedChanged)
        self.logic.experimentDataAsXmlChanged.connect(self.experimentDataAsXmlChanged)
        self.experimentDataChanged.connect(self._onExperimentDataChanged)
        self.experimentSkippedChanged.connect(self._onExperimentSkippedChanged)
        self.experimentLoadedChanged.connect(self._onExperimentLoadedChanged)

        # notifiers for other proxies
        self.logic.patternParametersAsObjChanged.connect(self.parent.parameters.patternParametersAsObjChanged)
        self.logic.structureParametersChanged.connect(self.parent.phase.structureParametersChanged)

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

    @Property(bool, notify=experimentLoadedChanged)
    def isSpinPolarized(self):
        return self.logic.spin_polarized

    @Property(str, notify=experimentLoadedChanged)
    def spinComponent(self):
        return self.logic.spinComponent()

    @Slot('QVariant')
    def setSpinPolarization(self, spin_polarized):
        if self.logic.setPolarized(spin_polarized):
            self.experimentLoadedChanged.emit()

    @Slot('QVariant')
    def setSpinComponent(self, component):
        if self.logic.setSpinComponent(component):
            self.experimentLoadedChanged.emit()

    @Property(bool, notify=experimentLoadedChanged)
    def refineSum(self):
        return self.logic.refineSum()

    @refineSum.setter
    def refineSum(self, value):
        self.logic.setRefineSum(value)

    @Property(bool, notify=experimentLoadedChanged)
    def refineDiff(self):
        return self.logic.refineDiff()

    @refineDiff.setter
    def refineDiff(self, value):
        self.logic.setRefineDiff(value)

    @Property(bool, notify=experimentLoadedChanged)
    def refineUp(self):
        return self.logic.refineUp()

    @refineUp.setter
    def refineUp(self, value):
        self.logic.setRefineUp(value)

    @Property(bool, notify=experimentLoadedChanged)
    def refineDown(self):
        return self.logic.refineDown()

    @refineDown.setter
    def refineDown(self, value):
        self.logic.setRefineDown(value)

    @Property(str, notify=experimentDataAsXmlChanged)
    def experimentDataAsXml(self):
        return self.logic._experiment_data_as_xml

    @Property(str, notify=experimentDataAsXmlChanged)
    # @Property(str, notify=experimentLoadedChanged)
    def experimentAsCif(self):
        return self.logic._experiment_no_data_as_cif

    @experimentAsCif.setter
    def experimentAsCif(self, experiment_as_cif):
        self.logic.loadCifNoData(experiment_as_cif)
        self.experimentLoadedChanged.emit()
        self.experimentDataAsXmlChanged.emit()

    def _setExperimentDataAsXml(self):
        start_time = timeit.default_timer()
        self.logic._setExperimentDataAsXml()
        print("+ _setExperimentDataAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.experimentDataAsXmlChanged.emit()

    def _onExperimentDataChanged(self):
        print("***** _onExperimentDataChanged")
        self._setExperimentDataAsXml()
        self.parent.project.stateChanged.emit(True)

    ####################################################################################################################
    # Experiment data: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addExperimentData(self, file_url):
        _, file_extension = os.path.splitext(file_url)
        if file_extension == '.cif':
            print(f"Reading '{file_extension}' file")
            self._addExperimentDataFromCif(file_url)
        elif file_extension in ('.xye', '.xys'):
            print(f"Reading '{file_extension}' file")
            self._addExperimentDataFromXye(file_url)
        elif file_extension == '.xy':
            print(f"We are working on supporting '{file_extension}' files")
        else:
            print(f"This file extension is not supported: '{file_extension}'")

    def _addExperimentDataFromCif(self, file_url):
        self.logic.addExperimentDataFromCif(file_url)
        self.logic.initializeBackground()
        self.logic.updateBackgroundData() # bg is now read in the lib
        self.logic._onExperimentDataAdded()
        self.experimentLoadedChanged.emit()

    def _addExperimentDataFromXye(self, file_url):
        self.logic.addExperimentDataFromXye(file_url)
        self.logic._onExperimentDataAdded()
        self.experimentLoadedChanged.emit()

    @Slot()
    def removeExperiment(self):
        print("+ removeExperiment")
        self.logic.removeExperiment()
        self.experimentDataChanged.emit()
        self.experimentLoadedChanged.emit()

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        return self.logic._loadExperimentData(file_url)

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

    def _onExperimentLoadedChanged(self):
        print("***** _onExperimentLoadedChanged")
        if self.experimentLoaded:
            self.parent.parameters._onParametersChanged()
            self.parent.parameters._onInstrumentParametersChanged()
            self._setPatternParametersAsObj()
            self._onExperimentDataChanged()

    def _onExperimentSkippedChanged(self):
        print("***** _onExperimentSkippedChanged")
        if self.experimentSkipped:
            self.parent.parameters._onParametersChanged()
            self.parent.parameters._onInstrumentParametersChanged()
            self._setPatternParametersAsObj()
            self.logic._onExperimentSkippedChanged()

    def _setPatternParametersAsObj(self):
        self.logic._onPatternParametersChanged()
