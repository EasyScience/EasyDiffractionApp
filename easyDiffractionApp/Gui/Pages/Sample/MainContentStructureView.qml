/*
import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

ExComponents.SampleStructure3dVtk {}
*/

import QtQuick 2.13

import Gui.Globals 1.0 as ExGlobals

Loader {
    source: ExGlobals.Constants.proxy.current3dPlottingLib === 'vtk' ?
                "../../Components/SampleStructure3dVtk.qml" :
                "../../Components/SampleStructure3dQtDataVisualization.qml"
}
