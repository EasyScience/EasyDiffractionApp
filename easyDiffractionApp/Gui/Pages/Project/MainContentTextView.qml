import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Elements 1.0 as EaElements

import Gui.Globals 1.0 as ExGlobals

ScrollView {
    EaElements.TextArea {
        readOnly: true
        text: ExGlobals.Constants.proxy.projectInfoAsCif
        //onEditingFinished: ExGlobals.Constants.proxy.projectInfoAsCif = text
    }
}
