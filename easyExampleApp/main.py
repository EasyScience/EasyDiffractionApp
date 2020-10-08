import os, sys
from PySide2.QtCore import QUrl
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

import pyproject
import easyAppGui
from easyAppLogic.Translate import Translator
from easyExampleApp.Logic.PyQmlProxy import PyQmlProxy


CONFIG = pyproject.config()

def isTestMode():
    if len(sys.argv) > 1:
        if 'test' in sys.argv[1:]:
            return True
    return False

def main():
    current_path = os.path.dirname(sys.argv[0])
    package_path = os.path.join(current_path, "easyExampleApp")
    if not os.path.exists(package_path):
        package_path = current_path

    main_qml_path = QUrl.fromLocalFile(os.path.join(package_path, "Gui", "main.qml"))
    gui_path = str(QUrl.fromLocalFile(package_path).toString())
    easyAppGui_path = os.path.join(easyAppGui.__path__[0], "..")

    languages = CONFIG['ci']['app']['translations']['languages']
    translations_dir = CONFIG['ci']['app']['translations']['dir']
    translations_path = os.path.join(package_path, *translations_dir.split('/'))

    # Create a proxy object between python logic and QML GUI
    py_qml_proxy_obj = PyQmlProxy()

    # Create application and qml application engine
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Create translator
    translator = Translator(app, engine, translations_path, languages)
    #translator.selectSystemLanguage()

    # Application settings
    #app.setApplicationName(py_qml_proxy_obj.appName)
    app.setApplicationName(CONFIG['tool']['poetry']['name'])
    app.setApplicationVersion(CONFIG['tool']['poetry']['version'])

    # Qml application engine settings
    engine.rootContext().setContextProperty("_pyQmlProxyObj", py_qml_proxy_obj)
    engine.rootContext().setContextProperty("_translator", translator)
    engine.rootContext().setContextProperty("_projectConfig", CONFIG)
    engine.rootContext().setContextProperty("_isTestMode", isTestMode())
    engine.addImportPath(easyAppGui_path)
    engine.addImportPath(gui_path)
    engine.load(main_qml_path)

    # Event loop
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
