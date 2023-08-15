# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import argparse
import orjson
import os
import pathlib
import sys
import time
from urllib.parse import urlparse

from PySide6.QtCore import QObject, QCoreApplication, Signal, Slot, Property, Qt
from PySide6.QtGui import QStyleHints
from PySide6.QtWidgets import QApplication

from EasyApp.Logic.Logging import console


class PersistentSettingsHandler:

    def __init__(self):
        self.path = self.getPath()

    def getPath(self):
        appName = QCoreApplication.instance().applicationName()
        homeDirPath = pathlib.Path.home()
        name = 'settings.ini'
        path = str(homeDirPath.joinpath(f'.{appName}', name))
        console.info(f'Persistent settings: {path}')
        return path


class ResourcePaths:

    def __init__(self):
        self.mainQml = ''  # Current app main.qml file
        self.splashScreenQml = ''  # Splash screen .qml file
        self.imports = []  # EasyApp qml components (EasyApp/...) & Current app qml components (Gui/...)
        self.settings_ini = ''  # Persistent settings ini file location
        self.setPaths()

    def setPaths(self):
        console.debug('Trying to import python resources.py file with EasyApp')
        try:
            import resources
            console.info(f'Resources: {resources}')
            self.mainQml = 'qrc:/Gui/main.qml'
            self.splashScreenQml = 'qrc:/Gui/Components/SplashScreen.qml'
            #self.imports = ['qrc:/EasyApp', 'qrc:/']

            import EasyApp
            easyAppPath = os.path.abspath(EasyApp.__path__[0])
            console.info(f'EasyApp module: {easyAppPath}')

            self.imports = [os.path.join(easyAppPath, '..'), 'qrc:/']
            return
        except ImportError:
            console.debug('No rc resources file found')

        console.debug('Trying to import the locally installed EasyApp module')
        try:
            import EasyApp
            easyAppPath = os.path.abspath(EasyApp.__path__[0])
            console.info(f'EasyApp module: {easyAppPath}')
            self.mainQml = 'Gui/main.qml'
            self.splashScreenQml = 'Gui/Components/SplashScreen.qml'
            self.imports = [os.path.join(easyAppPath, '..'), '.']
            return
        except ImportError:
            console.debug('No EasyApp module is installed')

        console.error('No EasyApp module found')


class CommandLineArguments:

    def __new__(cls):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            '-t',
            '--testmode',
            action='store_true',
            help='run the application in test mode: run tests, take screenshots and exit the application'
        )

        return parser.parse_args()


class EnvironmentVariables:

    @staticmethod
    def set():
        os.environ['QSG_RHI_BACKEND'] = 'opengl'  # For QtCharts XYSeries useOpenGL
        os.environ['QT_RHI_SHADER_DEBUG'] = '1'  # https://doc.qt.io/qt-6/qtquick3d-tool-shadergen.html
        #qsetenv("QT_QPA_PLATFORM", "windows:darkmode=[1|2]")
        #os.environ['QT_QPA_PLATFORM'] = 'windows:darkmode=[1|2]'
        #os.environ['QT_MESSAGE_PATTERN'] = "\033[32m%{time h:mm:ss.zzz}%{if-category}\033[32m %{category}:%{endif} %{if-debug}\033[34m%{function}%{endif}%{if-warning}\033[31m%{backtrace depth=3}%{endif}%{if-critical}\033[31m%{backtrace depth=3}%{endif}%{if-fatal}\033[31m%{backtrace depth=3}%{endif}\033[0m %{message}"


class WebEngine:

    @staticmethod
    def initialize():
        try:
            from PySide6.QtWebEngineQuick import QtWebEngineQuick
        except ModuleNotFoundError:
            console.debug('No module named "PySide6.QtWebEngineQuick" is found')
            pass
        else:
            QtWebEngineQuick.initialize()

    @staticmethod
    def runJavaScriptWithoutCallback(webEngine, script):
        callback = None
        webEngine.runJavaScript(script, callback)


class IO:

    @staticmethod
    def generalizePath(fpath: str) -> str:
        """
        Generalize the filepath to be platform-specific, so all file operations
        can be performed.
        :param URI rcfPath: URI to the file
        :return URI filename: platform specific URI
        """
        return fpath  # NEED FIX: Check on different platforms
        filename = urlparse(fpath).path
        if not sys.platform.startswith("win"):
            return filename
        if filename[0] == '/':
            filename = filename[1:].replace('/', os.path.sep)
        return filename

    @staticmethod
    def formatMsg(type, *args):
        types = {'main': '•', 'sub': ' ◦'}
        mark = types[type]
        widths = [22,21,20,10]
        widths[0] -= len(mark)
        msgs = []
        for idx, arg in enumerate(args):
            msgs.append(f'{arg:<{widths[idx]}}')
        msg = ' ▌ '.join(msgs)
        msg = f'{mark} {msg}'
        return msg


class Converter:

    @staticmethod
    def jsStrToPyBool(value):
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            #console.debug(f'Input value "{value}" is not supported. It should either be "true" or "false".')
            pass

    @staticmethod
    def dictToJson(obj):
        # Dump to json
        dumpOption = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2
        jsonBytes = orjson.dumps(obj, option=dumpOption)
        json = jsonBytes.decode()
        return json
        #if not formatted:
        #    return jsonStr
        ## Format to have arrays shown in one line. Can orjson do this?
        #formatOptions = jsbeautifier.default_options()
        #formatOptions.indent_size = 2
        #formattedJsonStr = jsbeautifier.beautify(jsonStr, formatOptions)
        #return formattedJsonStr


class Application(QApplication):  # QGuiApplication crashes when using in combination with QtCharts
    def __init__(self, sysArgv):
        super(Application, self).__init__(sysArgv)
        self.setApplicationName('EasyExample')
        self.setOrganizationName('EasyScience')
        self.setOrganizationDomain('easyscience.software')


class BackendHelpers(QObject):
    systemColorSchemeChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._styleHints = QApplication.instance().styleHints()
        self.schemes = { Qt.ColorScheme.Unknown: 0,
                         Qt.ColorScheme.Light: 1,
                         Qt.ColorScheme.Dark: 2 }
        self._systemColorScheme = self.schemes[self._styleHints.colorScheme()]
        console.debug(f"Initial system color scheme: {self._systemColorScheme} (0 - unknown, 1 - light, 2 - dark)")
        self._styleHints.colorSchemeChanged.connect(self.onSystemColorSchemeChanged)

    @Property(int, notify=systemColorSchemeChanged)
    def systemColorScheme(self):
        return self._systemColorScheme

    def onSystemColorSchemeChanged(self):
        console.debug(f"Previous system color scheme: {self._systemColorScheme}")
        self._systemColorScheme = self.schemes[self._styleHints.colorScheme()]
        console.debug(f"New system color scheme: {self._systemColorScheme}")
        self.systemColorSchemeChanged.emit()

    @Slot(int)
    def exitApp(self, exitCode):
        console.debug(f'Force exiting application with code {exitCode}')
        os._exit(exitCode)

    @Slot(str, result=bool)
    def fileExists(self, path):
        exists = pathlib.Path(path).is_file()
        #if exists:
        #    console.debug(f'File {path} exists')
        #else:
        #    console.debug(f"File {path} doesn't exist")
        return exists

    @Slot('QVariant', result=str)
    def listToUri(self, fpathParts):
        fpathParts = fpathParts.toVariant()
        fpath = os.path.join(*fpathParts)
        if fpath[:2] == ':/':  # qrc format
            return 'qrc' + fpath
        exists = pathlib.Path(fpath).is_file()
        if not exists:
            return ''
        furi = pathlib.Path(fpath).as_uri()
        if sys.platform.startswith("win") and furi[0] == '/':
            furi = furi[1:].replace('/', os.path.sep)
        return furi

class PyProxyWorker(QObject):
    pyProxyExposedToQml = Signal()

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self._engine = engine

    def exposePyProxyToQml(self):
        from Logic.PyProxy import PyProxy
        time.sleep(0.5)
        console.debug('Slept for 0.5s to allow splash screen to start')
        mainThread = QCoreApplication.instance().thread()
        proxy = PyProxy()
        console.debug('PyProxy object created')
        proxy.moveToThread(mainThread)
        self._engine.rootContext().setContextProperty('pyProxy', proxy)
        self.pyProxyExposedToQml.emit()
        console.debug('PyProxy object exposed to QML')
