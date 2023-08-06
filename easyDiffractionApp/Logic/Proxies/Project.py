# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from PySide6.QtCore import QObject, Signal, Slot, Property


class ProjectProxy(QObject):
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal()
    dummySignal = Signal()
    stateChanged = Signal(bool)
    htmlExportingFinished = Signal(bool, str)
    statusInfoChanged = Signal()
    reportRequested = Signal()

    def __init__(self, parent=None, logic=None):  # , interface=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_project
        self.stateChanged.connect(self._onStateChanged)
        self.logic.projectCreatedChanged.connect(self.projectCreatedChanged)
        self.logic.projectInfoChanged.connect(self.projectInfoChanged)

    @Property('QVariant', notify=projectInfoChanged)
    def projectInfoAsJson(self):
        return self.logic._project_info

    @projectInfoAsJson.setter
    def projectInfoAsJson(self, json_str):
        self.logic.projectInfoAsJson(json_str)
        self.projectInfoChanged.emit()

    @Property(str, notify=projectInfoChanged)
    def projectInfoAsCif(self):
        return self.logic.projectInfoAsCif()

    @Slot(str, str)
    def editProjectInfo(self, key, value):
        self.logic.editProjectInfo(key, value)
        self.projectInfoChanged.emit()

    @Property(str, notify=projectInfoChanged)
    def currentProjectPath(self):
        return self.logic._currentProjectPath

    @currentProjectPath.setter
    def currentProjectPath(self, new_path):
        self.logic.currentProjectPath(new_path)
        self.projectInfoChanged.emit()

    @Slot()
    def createProject(self):
        self.logic.createProject()

    @Property(str, notify=dummySignal)
    def projectExamplesAsXml(self):
        return self.logic.projectExamplesAsXml()

    ####################################################################################################################
    ####################################################################################################################
    # State save/load
    ####################################################################################################################
    ####################################################################################################################

    @Slot()
    def saveProject(self):
        self.logic.saveProject()
        self.stateChanged.emit(False)

    @Slot(str)
    def loadProjectAs(self, filepath):
        self.logic._loadProjectAs(filepath)
        self.stateChanged.emit(False)
        self.parent.fitting.calculatorListChanged.emit()

    @Slot()
    def loadProject(self):
        self.logic._loadProject()
        self.stateChanged.emit(False)
        self.parent.fitting.calculatorListChanged.emit()

    @Slot(str)
    def loadExampleProject(self, filepath):
        self.logic._loadProjectAs(filepath)
        self.stateChanged.emit(False)
        self.parent.fitting.calculatorListChanged.emit()

    @Property(str, notify=dummySignal)
    def projectFilePath(self):
        return self.logic.project_save_filepath

    @Property(bool, notify=projectCreatedChanged)
    def projectCreated(self):
        return self.logic._project_created

    @projectCreated.setter
    def projectCreated(self, created: bool):
        self.logic.setProjectCreated(created)

    @Slot()
    def resetState(self):
        self.logic.resetState()
        self.parent.experiment.removeExperiment()
        self.logic.stateHasChanged(False)
        self.stateChanged.emit(False)

    @Property(bool, notify=projectCreatedChanged)
    def readOnly(self):
        return self.logic._read_only

    @Property(bool, notify=stateChanged)
    def stateHasChanged(self):
        return self.logic._state_changed

    def _onStateChanged(self, changed=True):
        self.logic.stateHasChanged(changed)

    @Slot(str)
    def setReport(self, report):
        """
        Keep the QML generated HTML report for saving
        """
        self.logic.setReport(report)

    @Slot(str)
    def saveReport(self, filepath):
        """
        Save the generated report to the specified file
        Currently only html
        """
        success = self.logic.saveReport(filepath)
        self.htmlExportingFinished.emit(success, filepath)

    @Slot()
    def requestReport(self):
        """
        Request a report generation
        """
        self.reportRequested.emit()

    # status
    @Property('QVariant', notify=statusInfoChanged)
    def statusModelAsObj(self):
        return self.logic.statusModelAsObj()

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        return self.logic.statusModelAsXml()
