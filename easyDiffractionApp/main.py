import os
import sys
import platform
import argparse

# PySide
from PySide2.QtCore import QUrl, qDebug, qCritical
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import Qt
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtWebEngine import QtWebEngine
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView  # to call hook-PySide2.QtWebEngineWidgets.py

# easyScience
import utils
import easyAppGui
from easyAppLogic.Translate import Translator
from easyDiffractionApp.Logic.PyQmlProxy import PyQmlProxy

# Global vars
CONFIG = utils.conf()
TEST_MODE = False


class App(QApplication):
    def __init__(self, sys_argv):
        #QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # DOESN'T WORK, USE SCRIPT INSTEAD
        #QCoreApplication.setAttribute(Qt.AA_UseDesktopOpenGL, True)
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
        import easyAppLogic.Logging
    if args.testmode:
        TEST_MODE = True

    # Paths
    current_path = os.path.dirname(sys.argv[0])
    package_path = os.path.join(current_path, 'easyDiffractionApp')
    if not os.path.exists(package_path):
        package_path = current_path

    main_qml_path = QUrl.fromLocalFile(os.path.join(package_path, 'Gui', 'main.qml'))
    gui_path = str(QUrl.fromLocalFile(package_path).toString())
    easyAppGui_path = os.path.join(easyAppGui.__path__[0], '..')

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

    # QML application engine
    engine = QQmlApplicationEngine()

    # Python objects to be exposed to QML
    py_qml_proxy_obj = PyQmlProxy()
    translator = Translator(app, engine, translations_path, languages)

    # Expose the Python objects to QML
    engine.rootContext().setContextProperty('_pyQmlProxyObj', py_qml_proxy_obj)
    engine.rootContext().setContextProperty('_translator', translator)
    engine.rootContext().setContextProperty('_projectConfig', CONFIG)
    engine.rootContext().setContextProperty('_isTestMode', TEST_MODE)

    # Add paths to search for installed modules
    engine.addImportPath(easyAppGui_path)
    engine.addImportPath(gui_path)

    # Load the root QML file
    engine.load(main_qml_path)

    # Root application window
    root_window = engine.rootObjects()[0]

    # Customize app window titlebar
    if platform.system() == "Darwin":
        import ctypes, objc, Cocoa

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
