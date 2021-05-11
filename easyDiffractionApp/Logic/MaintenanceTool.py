import os
import sys
import re

from PySide2.QtCore import QObject, QProcess, Property, Signal, Slot
from PySide2.QtWidgets import QApplication


class MaintenanceTool(QObject):

    # SIGNALS

    updateFound = Signal()
    updateNotFound = Signal()
    updateFailed = Signal()

    webVersionChanged = Signal()
    errorMessageChanged = Signal()
    silentCheckChanged = Signal()

    # INIT

    def __init__(self, parent=None):
        super().__init__(parent)

        # private members
        self._web_version = ""
        self._error_message = ""
        self._silent_check = True

        self._process = QProcess()
        self._process.setWorkingDirectory(QApplication.applicationDirPath())
        #self._process.setWorkingDirectory("/Applications/easyDiffraction/MaintenanceTool.app/Contents/MacOS")
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
        arguments = ["--updater", "--verbose"]

        updater_started = QProcess.startDetached(program, arguments)

        if updater_started:
            QApplication.quit()

    # PUBLIC PROPERTIES

    @Property(str, notify=webVersionChanged)
    def webVersion(self):
        return self._web_version

    @Property(str, notify=errorMessageChanged)
    def errorMessage(self):
        return self._error_message

    @Property(bool, notify=silentCheckChanged)
    def silentCheck(self):
        return self._silent_check

    @silentCheck.setter
    def silentCheck(self, silent_check: bool):
        if self._silent_check == silent_check:
            return

        self._silent_check = silent_check
        self.silentCheckChanged.emit()

    # PRIVATE METHODS

    def _onStarted(self):
        print("* MaintenanceTool process started")
        self._web_version = ""
        self._error_message = ""
        self.webVersionChanged.emit()
        self.errorMessageChanged.emit()

    def _onFinished(self, exit_code: int, exit_status: QProcess.ExitStatus):
        print(f"* MaintenanceTool process finished with exit code: '{exit_code}' and exit status: '{exit_status}'")

        # Get updater process output and error, if any
        std_out = self._process.readAllStandardOutput().data().decode('utf-8')
        std_err = self._process.readAllStandardError().data().decode('utf-8')

        # Debug printing
        if std_out:
            print(f"* MaintenanceTool standard output:\n{std_out}")
        if std_err:
            print(f"* MaintenanceTool standard error:\n{std_err}")

        # Something went wrong
        if exit_code != 0 or exit_status != QProcess.ExitStatus.NormalExit:
            print(f"* MaintenanceTool process failed")
            self._error_message = f"MaintenanceTool process finished with\n* exit code: {exit_code} \n* exit status: {exit_status}"
            self.errorMessageChanged.emit()
            if not self.silentCheck:
                self.updateFailed.emit()
            return

        # Process finished succesfully
        print(f"* MaintenanceTool process succeeded; checking for updates...")

        # Check if a new version of any of the app component is found
        pattern = r'<update.*version="([A-Za-z0-9.-]*)".*/>'
        matches = re.findall(pattern, std_out)

        # No new versions are found
        if not matches:
            print("* MaintenanceTool did not find any updates")
            if not self.silentCheck:
                self.updateNotFound.emit()
            return

        # New version is found
        print(f"* MaintenanceTool found component(s) with new version(s): {matches}")
        self._web_version = matches[0]  # TODO: Update this if multiple components are available
        self.webVersionChanged.emit()
        self.updateFound.emit()

    def _onErrorOccurred(self, error):
        print(f"* MaintenanceTool process got error: '{error}'")
        self._error_message = error
        self.errorMessageChanged.emit()
        if not self.silentCheck:
            self.updateFailed.emit()

    # STATIC METHODS

    @staticmethod
    def exeRelativePath():
        if sys.platform.startswith('win'):
            return "maintenancetool.exe"
        elif sys.platform.startswith('darwin'):
            return "../../../MaintenanceTool.app/Contents/MacOS/MaintenanceTool"
        else:
            return "maintenancetool"
