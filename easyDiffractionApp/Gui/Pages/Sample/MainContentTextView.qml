import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Item {

    ScrollView {
        anchors.fill: parent

        EaElements.TextArea {
            //text: EaLogic.Utils.prettyJson(ExGlobals.Constants.proxy.phasesObj)
            //onEditingFinished: ExGlobals.Constants.proxy.phasesObj = text
            text: ExGlobals.Constants.proxy.phasesCif
            //onEditingFinished: ExGlobals.Constants.proxy.phasesCif = text
        }
    }



}
