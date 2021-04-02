import QtQuick 2.14
import QtQuick.Controls 2.14

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements

import Gui.Globals 1.0 as ExGlobals

EaElements.Dialog {
    id: dialog
    title: qsTr("Save Changes")
    parent: Overlay.overlay

    x: (parent.width - width) * 0.5
    y: (parent.height - height) * 0.5

    spacing: 2 * EaStyle.Sizes.fontPixelSize
    EaElements.Label {
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("The project has not been saved. Do you want to exit?")
    }
    footer: EaElements.DialogButtonBox {
        spacing: 2 * EaStyle.Sizes.fontPixelSize
        bottomPadding: EaStyle.Sizes.fontPixelSize * 1.2
        rightPadding: EaStyle.Sizes.fontPixelSize * 1.2
        EaElements.Button {
            text: qsTr("Save and exit")
            onClicked: {
                ExGlobals.Constants.proxy.saveProject()
                Qt.quit()
            }
        }
        EaElements.Button {
            text: qsTr("Exit without saving")
            onClicked: {
                Qt.quit()
            }
        }
    }
}

