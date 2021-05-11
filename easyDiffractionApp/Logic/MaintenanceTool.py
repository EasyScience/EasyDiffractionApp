import os
import sys
import re

from PySide2.QtCore import QObject, QProcess, Property, Signal, Slot
from PySide2.QtWidgets import QApplication


class MaintenanceTool(QObject):

    # SIGNALS

    hasUpdateChanged = Signal(bool)
    webVersionChanged = Signal(str)

    # INIT

    def __init__(self, parent=None):
        super().__init__(parent)

        # private members
        self._has_update = False
        self._web_version = ""

        self._process = QProcess()
        self._process.setWorkingDirectory(QApplication.applicationDirPath())
        self._process.setWorkingDirectory("/Applications/easyDiffraction/MaintenanceTool.app/Contents/MacOS")
        self._process.setProgram(MaintenanceTool.exeRelativePath())

        # connections
        self._process.started.connect(self._onStarted)
        self._process.finished.connect(self._onFinished)
        self._process.errorOccurred.connect(self._onErrorOccurred)

    # PUBLIC SLOTS

    @Slot()
    def checkUpdate(self):
        print(f"* MaintenanceTool checkUpdate called")

        if self._process.state() == QProcess.Running:
            return

        self.webVersion = ""
        self.hasUpdate = False
        self._process.setArguments(["--checkupdates", "--verbose"])
        self._process.start()

    @Slot()
    def installUpdate(self):
        """
        Start the external maintenance tool as detached process
        """
        print(f"* MaintenanceTool installUpdate called")

        if self._process.state() == QProcess.Running:
            return

        program = os.path.join(self._process.workingDirectory(), self._process.program())
        args = ["--updater", "--verbose"]

        updater_started = QProcess.startDetached(program, args)

        if updater_started:
            QApplication.quit()

    # PUBLIC PROPERTIES

    # Get if there is an update
    @Property(bool, notify=hasUpdateChanged)
    def hasUpdate(self):
        return self._has_update

    @hasUpdate.setter
    def hasUpdate(self, has_update: bool):
        if self._has_update == has_update:
            return
        self._has_update = has_update
        self.hasUpdateChanged.emit(self._has_update)

    # Web version
    @Property(str, notify=webVersionChanged)
    def webVersion(self):
        return self._web_version

    @webVersion.setter
    def webVersion(self, update_details: str):
        if self._web_version == update_details:
            return
        self._web_version = update_details
        self.webVersionChanged.emit(self._web_version)

    # PRIVATE METHODS

    def _onStarted(self):
        print("* MaintenanceTool process started")

    def _onFinished(self, exit_code: int, exit_status: QProcess.ExitStatus):
        print(f"* MaintenanceTool process finished with exit code: '{exit_code}' and exit status: '{exit_status}'")

        std_out = self._process.readAllStandardOutput().data().decode('utf-8')
        std_err = self._process.readAllStandardError().data().decode('utf-8')

        if std_out:
            print(f"* MaintenanceTool standard output:\n{std_out}")
        if std_err:
            print(f"* MaintenanceTool standard error:\n{std_err}")

        if exit_code != 0 or exit_status != QProcess.ExitStatus.NormalExit:
            print(f"* MaintenanceTool process failed")
            return

        print(f"* MaintenanceTool process succeeded")

        pattern = r'<update.*version="([A-Za-z0-9.-]*)".*/>'
        matches = re.findall(pattern, std_out)

        if not matches:
            print("* MaintenanceTool did not find any updates")
            return

        self.hasUpdate = True
        self.webVersion = matches[0]

        print(f"* MaintenanceTool found new version: {self.webVersion}")

    def _onErrorOccurred(self, error):
        print(f"* MaintenanceTool process got error: '{error}'")

    # STATIC METHODS

    @staticmethod
    def exeRelativePath():
        if sys.platform.startswith('win'):
            return "maintenancetool.exe"
        elif sys.platform.startswith('darwin'):
            return "../../../MaintenanceTool.app/Contents/MacOS/MaintenanceTool"
        else:
            return "maintenancetool"
