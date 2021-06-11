from PySide2.QtCore import QObject, Signal, Slot, Property

from easyDiffractionApp.Logic.Project import ProjectLogic


class ProjectProxy(QObject):
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal()
    dummySignal = Signal()
    stateChanged = Signal(bool)

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

    @Slot()
    def loadProject(self):
        self.logic._loadProject()
        self._background_proxy.onAsObjChanged()
        self.stateChanged.emit(False)

    @Slot(str)
    def loadExampleProject(self, filepath):
        self.logic._loadProjectAs(filepath)
        self.currentProjectPath = '--- EXAMPLE ---'
        self.stateChanged.emit(False)

    @Property(str, notify=dummySignal)
    def projectFilePath(self):
        return self.logic.project_save_filepath

    @Property(bool, notify=projectCreatedChanged)
    def projectCreated(self):
        return self.logic._project_created

    @projectCreated.setter
    def projectCreated(self, created: bool):
        self.logic.setProjectCreated(created)
        #if self.logic.setProjectCreated(created):
        #    self.projectCreatedChanged.emit()

    @Slot()
    def resetState(self):
        self.logic.resetState()
        self.stateChanged.emit(False)

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
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self._report)
            success = True
        except IOError:
            success = False
        finally:
            self.htmlExportingFinished.emit(success, filepath)

