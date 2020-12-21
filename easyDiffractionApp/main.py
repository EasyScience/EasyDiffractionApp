import os
import sys

# Logging
def isTestMode():
    if len(sys.argv) > 1:
        if 'test' in sys.argv[1:]:
            return True
    return False
if not isTestMode():
    import easyAppLogic.Logging

# PySide
from PySide2.QtCore import QUrl, qDebug, qCritical
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType

# easyScience
import pyproject
import easyAppGui
from easyAppLogic.Translate import Translator
from easyDiffractionApp.Logic.PyQmlProxy import PyQmlProxy

# Matplotlib
mpl_cfg = os.path.join(os.path.join(os.path.dirname(sys.argv[0]), 'easyDiffractionApp'), 'DisplayModels', 'cfg')
os.environ['MPLCONFIGDIR'] = mpl_cfg
from matplotlib_backend_qtquick.backend_qtquickagg import (
    FigureCanvasQtQuickAgg)
from matplotlib_backend_qtquick.qt_compat import QtGui, QtQml, QtCore
from easyDiffractionApp.Logic.MatplotlibBackend import DisplayBridge

# VTK
from easyDiffractionApp.Logic.VTKBackend import VTKcanvasHandler
from easyDiffractionApp.Logic.VTK.QVTKFrameBufferObjectItem import FboItem

# Config
CONFIG = pyproject.config()


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
        # sys_argv += ['-style', 'material']  #! MUST HAVE
        self._m_vtkFboItem = None
        QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)
        QtGui.QSurfaceFormat.setDefaultFormat(defaultFormat(False))  # from vtk 8.2.0
        super(App, self).__init__(sys_argv)

    def startApplication(self):
        qDebug('CanvasHandler::startApplication()')
        self._m_vtkFboItem.rendererInitialized.disconnect(self.startApplication)

    def vtkSetup(self, root_window):
        # Get reference to the QVTKFramebufferObjectItem in QML
        self._m_vtkFboItem = root_window.findChild(FboItem, 'vtkFboItem')

        # Give the vtkFboItem reference to the CanvasHandler
        if (self._m_vtkFboItem):
            qDebug('CanvasHandler::CanvasHandler: setting vtkFboItem to CanvasHandler')
            self._m_vtkFboItem.rendererInitialized.connect(self.startApplication)
        else:
            qCritical('CanvasHandler::CanvasHandler: Unable to get vtkFboItem instance')
            return

def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) # DOESN'T WORK, USE SCRIPT INSTEAD

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

    # Application
    app = App(sys.argv)
    app.setApplicationName(CONFIG['tool']['poetry']['name'])
    app.setApplicationVersion(CONFIG['tool']['poetry']['version'])
    app.setOrganizationName(CONFIG['tool']['poetry']['name'])
    app.setOrganizationDomain(CONFIG['tool']['poetry']['name'])

    # QML application engine
    engine = QQmlApplicationEngine()

    # Main proxy object between python logic and QML GUI
    py_qml_proxy_obj = PyQmlProxy()

    # App translator
    translator = Translator(app, engine, translations_path, languages)
    #translator.selectSystemLanguage()

    # Matplotlib display bridge
    matplotlib_bridge = DisplayBridge()
    qmlRegisterType(FigureCanvasQtQuickAgg, 'MatplotlibBackend', 1, 0, 'FigureCanvas')

    # VTK handler
    vtk_handler = VTKcanvasHandler()
    qmlRegisterType(FboItem, 'QtVTK', 1, 0, 'VtkFboItem')

    # Expose the Python objects to QML
    engine.rootContext().setContextProperty('_pyQmlProxyObj', py_qml_proxy_obj)
    engine.rootContext().setContextProperty('_translator', translator)
    engine.rootContext().setContextProperty('_projectConfig', CONFIG)
    engine.rootContext().setContextProperty('_isTestMode', isTestMode())
    engine.rootContext().setContextProperty('_matplotlibBridge', matplotlib_bridge)
    engine.rootContext().setContextProperty('_vtkHandler', vtk_handler)

    # Add paths to search for installed modules
    engine.addImportPath(easyAppGui_path)
    engine.addImportPath(gui_path)

    # Load the root QML file
    engine.load(main_qml_path)

    # Root application window
    root_window = engine.rootObjects()[0]

    # Matplotlib setup
    matplotlib_bridge.context = root_window

    # VTK setup
    app.vtkSetup(root_window)
    vtk_handler.fbo = app._m_vtkFboItem
    vtk_handler.context = root_window
    py_qml_proxy_obj.setVtkHandler(vtk_handler)

    # Event loop
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
