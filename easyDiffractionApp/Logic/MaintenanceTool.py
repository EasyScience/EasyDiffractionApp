import os
import pathlib
import re
import requests
import sys

from PySide2.QtCore import QObject, QProcess, Property, Signal, Slot
from PySide2.QtWidgets import QApplication


class MaintenanceTool(QObject):

    # SIGNALS

    updateFound = Signal()
    updateNotFound = Signal()
    updateFailed = Signal()

    silentCheckChanged = Signal()
    errorMessageChanged = Signal()
    webVersionChanged = Signal()
    releaseNotesChanged = Signal()

    # INIT

    def __init__(self, parent=None):
        super().__init__(parent)

        # private members
        self._silent_check = True
        self._error_message = ""
        self._web_version = ""

        self._release_notes = ""

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

    @Property(bool, notify=silentCheckChanged)
    def silentCheck(self):
        return self._silent_check

    @silentCheck.setter
    def silentCheck(self, silent_check: bool):
        if self._silent_check == silent_check:
            return

        self._silent_check = silent_check
        self.silentCheckChanged.emit()

    @Property(str, notify=errorMessageChanged)
    def errorMessage(self):
        return self._error_message

    @Property(str, notify=webVersionChanged)
    def webVersion(self):
        return self._web_version

    @Property(str, notify=releaseNotesChanged)
    def releaseNotes(self):
        return self._release_notes

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
        self._release_notes = self._getReleaseNotes()
        self.webVersionChanged.emit()
        self.releaseNotesChanged.emit()

        # Trigger frontend dialog opening
        self.updateFound.emit()

    def _onErrorOccurred(self, error):
        print(f"* MaintenanceTool process got error: '{error}'")
        self._error_message = error
        self.errorMessageChanged.emit()
        if not self.silentCheck:
            self.updateFailed.emit()

    def _getAppChangelog(self):
        path = MaintenanceTool.appChangelogPath()
        try:
            return pathlib.Path(path).read_text()
        except Exception as exception:
            print(f"* Failed to read local file {path} with exception {exception}")
            return ""

    def _getWebChangelog(self):
        url = MaintenanceTool.webChangelogUrl()
        try:
            result = requests.get(url)
            if result.ok:
                return result.text
            else:
                print(f"* Failed to read web file {url} with code '{result.status_code}' and reason '{result.reason}'")
                return ""
        except Exception as exception:
            print(f"* Failed to read web file {url} with exception {exception}")
            return ""

    def _getReleaseNotes(self):
        app_changelog = self._getAppChangelog()
        web_changelog = self._getWebChangelog()
        # remove overlapping part
        release_notes = web_changelog.replace(app_changelog, "")
        # TODO: Temporary solution to change default headers size and and empty lines (QML Text.MarkdownText)
        release_notes = re.sub(r'\n### ', "\n____\n#### ", release_notes)
        release_notes = re.sub(r'\n# ', "\n____\n____\n### ", release_notes)
        release_notes = re.sub(r'^# ', "### ", release_notes)
        return release_notes

    # STATIC METHODS

    @staticmethod
    def exeRelativePath():
        if sys.platform.startswith('win'):
            return "maintenancetool.exe"
        elif sys.platform.startswith('darwin'):
            return "../../../MaintenanceTool.app/Contents/MacOS/MaintenanceTool"
        else:
            return "maintenancetool"

    @staticmethod
    def appChangelogPath():
        if sys.platform.startswith('win'):
            relative_path = "CHANGELOG.md"
        elif sys.platform.startswith('darwin'):
            relative_path = "../../../CHANGELOG.md"
        else:
            relative_path = "CHANGELOG.md"
        path = os.path.join(QApplication.applicationDirPath(), relative_path)
        path = os.path.join("/Applications/easyDiffraction/MaintenanceTool.app/Contents/MacOS", relative_path)
        return path

    @staticmethod
    def webChangelogUrl():
        if sys.platform.startswith('win'):
            os_dir = "Windows"
        elif sys.platform.startswith('darwin'):
            os_dir = "macOS"
        else:
            os_dir = "Linux"
        url = f'https://download.easydiffraction.org/onlineRepository/{os_dir}/CHANGELOG.md'
        return url
