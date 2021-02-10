import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Item {

    ScrollView {
        anchors.fill: parent

        EaElements.TextArea {
            font.family: EaStyle.Fonts.monoFontFamily
            text: ExGlobals.Constants.proxy.projectInfoAsCif
            //onEditingFinished: ExGlobals.Constants.proxy.projectInfoAsCif = text
        }
    }

    EaComponents.TableViewButton {
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        fontIcon: "sync-alt"
        ToolTip.text: qsTr("Update")
        onClicked: forceActiveFocus()
    }

}
