import os, sys

from PySide2.QtCore import QUrl, qDebug, qCritical
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType

import pyproject
import easyAppGui
from easyAppLogic.Translate import Translator
import easyAppLogic.Logging
from easyDiffractionApp.Logic.PyQmlProxy import PyQmlProxy

# Setup matplotlib styles
from easyDiffractionApp.Logic.VTKBackend import VTKcanvasHandler

mpl_cfg = os.path.join(os.path.join(os.path.dirname(sys.argv[0]), "easyDiffractionApp"), 'DisplayModels', 'cfg')
os.environ['MPLCONFIGDIR'] = mpl_cfg

from matplotlib_backend_qtquick.backend_qtquickagg import (
    FigureCanvasQtQuickAgg)
from matplotlib_backend_qtquick.qt_compat import QtGui, QtQml, QtCore
from easyDiffractionApp.Logic.MatplotlibBackend import DisplayBridge
from easyDiffractionApp.Logic.VTK.QVTKFrameBufferObjectItem import FboItem

CONFIG = pyproject.config()


def isTestMode():
    if len(sys.argv) > 1:
        if 'test' in sys.argv[1:]:
            return True
    return False


def defaultFormat(stereo_capable):
    """ Po prostu skopiowałem to z https://github.com/Kitware/VTK/blob/master/GUISupport/Qt/QVTKRenderWindowAdapter.cxx
     i działa poprawnie bufor głębokości
  """
    fmt = QtGui.QSurfaceFormat()
    fmt.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
    fmt.setVersion(3, 2)
    fmt.setProfile(QtGui.QSurfaceFormat.CoreProfile)
    fmt.setSwapBehavior(QtGui.QSurfaceFormat.DoubleBuffer)
    fmt.setRedBufferSize(8)
    fmt.setGreenBufferSize(8)
    fmt.setBlueBufferSize(8)
    fmt.setDepthBufferSize(8)
    fmt.setAlphaBufferSize(8)
    fmt.setStencilBufferSize(0)
    fmt.setStereo(stereo_capable)
    fmt.setSamples(0)

    return fmt


class App(QApplication):

    def __init__(self, sys_argv):
        # sys_argv += ["-style", "material"]  #! MUST HAVE
        self._m_vtkFboItem = None
        QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)
        QtGui.QSurfaceFormat.setDefaultFormat(defaultFormat(False))  # from vtk 8.2.0
        super(App, self).__init__(sys_argv)

    def startApplication(self):
        qDebug('CanvasHandler::startApplication()')
        self._m_vtkFboItem.rendererInitialized.disconnect(self.startApplication)

    def setup(self, engine):
        # Get reference to the QVTKFramebufferObjectItem in QML
        rootObject = engine.rootObjects()[0]  # returns QObject
        self._m_vtkFboItem = rootObject.findChild(FboItem, 'vtkFboItem')

        # Give the vtkFboItem reference to the CanvasHandler
        if (self._m_vtkFboItem):
            qDebug('CanvasHandler::CanvasHandler: setting vtkFboItem to CanvasHandler')
            self._m_vtkFboItem.rendererInitialized.connect(self.startApplication)
        else:
            qCritical('CanvasHandler::CanvasHandler: Unable to get vtkFboItem instance')
            return

def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    current_path = os.path.dirname(sys.argv[0])
    package_path = os.path.join(current_path, "easyDiffractionApp")
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

    # Expose VTK
    qmlRegisterType(FboItem, 'QtVTK', 1, 0, 'VtkFboItem')

    # Create application and qml application engine
    app = App(sys.argv)
    engine = QQmlApplicationEngine()

    # Display Bridge
    displayBridge = DisplayBridge()

    handler = VTKcanvasHandler()

    # Expose the Python object to QML
    context = engine.rootContext()
    context.setContextProperty("displayBridge", displayBridge)
    context.setContextProperty('canvasHandler', handler)


    # matplotlib stuff
    qmlRegisterType(FigureCanvasQtQuickAgg, "MatplotlibBackend", 1, 0, "FigureCanvas")

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

    win = engine.rootObjects()[0]
    displayBridge.context = win
    displayBridge.updateWithCanvas('figure')

    app.setup(engine)

    handler.fbo = app._m_vtkFboItem
    handler.context = win
    py_qml_proxy_obj.vtkHandler = handler

    # Event loop
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
