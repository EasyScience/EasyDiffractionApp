# SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
# SPDX-License-Identifier: BSD-3-Clause
# © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

# Import logger from EasyApp module
import sys
EASYAPP_LOCAL_PATH = '../../EasyApp'
sys.path.append(EASYAPP_LOCAL_PATH)
from EasyApp.Logic.Logging import console


if __name__ == '__main__':

    from PySide6.QtCore import qInstallMessageHandler
    qInstallMessageHandler(console.qmlMessageHandler)
    console.debug('Custom Qt message handler defined')

    from Logic.Helpers import EnvironmentVariables
    EnvironmentVariables.set()
    console.debug('Environment variables defined')

    # Magically fixes the following issues in QtQuick3D on macOS for local run
    # - Particles not supported due to missing RGBA32F and RGBA16F texture format support
    # - No GLSL shader code found (versions tried:  QList(120) ) in baked shader
    # - Failed to build graphics pipeline state
    from Logic.Helpers import WebEngine
    WebEngine.initialize()
    console.debug('QtWebEngine for the QML GUI components initialized')

    from Logic.Helpers import Application
    app = Application(sys.argv)
    console.debug(f'Qt Application created {app}')

    from PySide6.QtQml import QQmlApplicationEngine
    engine = QQmlApplicationEngine()
    console.debug(f'QML application engine created {engine}')

    from Logic.Helpers import ResourcePaths
    resourcePaths = ResourcePaths()
    for p in resourcePaths.imports:
        engine.addImportPath(p)
    console.debug('Resource paths exposed to QML')

    from Logic.Helpers import PersistentSettingsHandler
    settingsHandler = PersistentSettingsHandler()
    engine.rootContext().setContextProperty('pySettingsPath', settingsHandler.path)
    console.debug('Persistent settings file path exposed to QML')

    from Logic.Helpers import CommandLineArguments
    cliArgs = CommandLineArguments()
    engine.rootContext().setContextProperty('pyIsTestMode', cliArgs.testmode)
    console.debug('pyIsTestMode object exposed to QML')

    engine.load(resourcePaths.splashScreenQml)
    console.debug('Splash screen QML component loaded')

    if not engine.rootObjects():
        sys.exit(-1)
    console.debug('QML engine has root component')

    from Logic.Helpers import PyProxyWorker
    from PySide6.QtCore import QThreadPool
    worker = PyProxyWorker(engine)
    worker.pyProxyExposedToQml.connect(lambda: engine.load(resourcePaths.mainQml))
    threadpool = QThreadPool.globalInstance()
    threadpool.start(worker.exposePyProxyToQml)
    console.debug('PyProxy object is creating in a separate thread and exposing to QML')

    console.debug('Application event loop is about to start')
    exitCode = app.exec()

    console.debug(f'Application is about to exit with code {exitCode}')
    sys.exit(exitCode)
