import QtQuick 2.13

import Gui.Logic 1.0 as ExLogic
import Gui.Globals 1.0 as ExGlobals

Loader {
    source: ExGlobals.Constants.proxy.current3dPlottingLib === 'vtk' ?
                ExLogic.Paths.component('SampleStructure3dVtk.qml') :
                ExLogic.Paths.component('SampleStructure3dQtDataVisualization.qml')
}
