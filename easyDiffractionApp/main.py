# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import os
import sys
import pathlib
import platform
import argparse
import darkdetect
import pip, toml # for PyInstaller to include these modules from utils.py

# PySide
from PySide2.QtCore import QUrl
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import Qt, QIcon
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtWebEngine import QtWebEngine
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView  # to call hook-PySide2.QtWebEngineWidgets.py

# easyScience
import utils
import easyApp as easyApp2
from easyApp.Logic.Translate import Translator
from easyApp.Logic.Maintenance import Updater
import easyDiffractionApp
from easyDiffractionApp.Logic.PyQmlProxy import PyQmlProxy

# Global vars
CONFIG = utils.conf()


class App(QApplication):
    def __init__(self, sys_argv):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # DOESN'T WORK?!, USE SCRIPT INSTEAD
        QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)
        super(App, self).__init__(sys_argv)


def main():
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logtofile', action='store_true',
                        help='enable logging in the file easyDiffraction.log in the system directory tmp instead of the terminal')
    parser.add_argument('-t', '--testmode', action='store_true',
                    help='run the application in test mode: run the tutorial, record a video and exit the application')
    args = parser.parse_args()
    if args.logtofile:
        import easyApp.Logging

    # Paths
    project_name = CONFIG['tool']['poetry']['name']
    current_path = easyDiffractionApp.__path__[0]
    
    package_path = os.path.join(current_path, f'{project_name}')
    if not os.path.exists(package_path):
        package_path = current_path

    main_qml_path = QUrl.fromLocalFile(os.path.join(package_path, 'Gui', 'main.qml'))
    gui_path = str(QUrl.fromLocalFile(package_path).toString())
    app_icon_path = os.path.join(package_path, 'Gui', 'Resources', 'Logo', 'App.png')
    easyApp_path = os.path.join(easyApp2.__path__[0], '..')

    home_path = pathlib.Path.home()
    app_name = CONFIG['release']['app_name']
    settings_path = str(home_path.joinpath(f'.{app_name}', 'settings.ini'))

    languages = CONFIG['ci']['app']['translations']['languages']
    translations_dir = CONFIG['ci']['app']['translations']['dir']
    translations_path = os.path.join(package_path, *translations_dir.split('/'))

    # QtWebEngine
    QtWebEngine.initialize()

    # Application
    app = App(sys.argv)
    app.setApplicationName(CONFIG['tool']['poetry']['name'])
    app.setApplicationVersion(CONFIG['tool']['poetry']['version'])
    app.setOrganizationName(CONFIG['tool']['poetry']['name'])
    app.setOrganizationDomain(CONFIG['tool']['poetry']['name'])
    app.setWindowIcon(QIcon(app_icon_path))

    app.setWindowIcon(QIcon(os.path.join(package_path, 'Gui', 'Resources', 'Logo', 'App.png')))
    # QML application engine
    engine = QQmlApplicationEngine()

    # Python objects to be exposed to QML
    py_qml_proxy_obj = PyQmlProxy()
    translator = Translator(app, engine, translations_path, languages)

    # Expose the Python objects to QML
    engine.rootContext().setContextProperty('_pyQmlProxyObj', py_qml_proxy_obj)
    engine.rootContext().setContextProperty('_settingsPath', settings_path)
    engine.rootContext().setContextProperty('_translator', translator)
    engine.rootContext().setContextProperty('_projectConfig', CONFIG)
    engine.rootContext().setContextProperty('_isTestMode', args.testmode)
    try:
        isDark = darkdetect.isDark()
    except FileNotFoundError:
        isDark = False
    engine.rootContext().setContextProperty('_isSystemThemeDark', isDark)

    # Register types to be instantiated in QML
    qmlRegisterType(Updater, 'easyApp.Logic.Maintenance', 1, 0, 'Updater')

    # Add paths to search for installed modules
    engine.addImportPath(easyApp_path)
    engine.addImportPath(gui_path)

    # Load the root QML file
    engine.load(main_qml_path)

    # Customize app window titlebar
    if platform.system() == "Darwin":
        import ctypes, objc, Cocoa

        # Root application window
        root_obj = engine.rootObjects()
        if not root_obj:
            sys.exit(-1)
        root_window = root_obj[0]

        ptr = int(root_window.winId())
        view = objc.objc_object(c_void_p=ctypes.c_void_p(ptr))
        window = view._.window

        window.setStyleMask_(window.styleMask() | Cocoa.NSFullSizeContentViewWindowMask)
        window.setTitlebarAppearsTransparent_(True)
        window.setTitleVisibility_(Cocoa.NSWindowTitleHidden)

    # Event loop
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
