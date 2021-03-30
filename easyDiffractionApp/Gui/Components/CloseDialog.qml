import QtQuick 2.14
import QtQuick.Controls 2.14

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements

import Gui.Globals 1.0 as ExGlobals

EaElements.Dialog {
    id: dialog
    title: "Save Changes"
    parent: Overlay.overlay

    x: (parent.width - width) * 0.5
    y: (parent.height - height) * 0.5

    modal: true

    Column {
        spacing: 2 * EaStyle.Sizes.fontPixelSize
        EaElements.Label {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "The project has not been saved. Do you want to exit?"
        }

        Row {
            spacing: 2 * EaStyle.Sizes.fontPixelSize
            anchors.horizontalCenter: parent.horizontalCenter

            EaElements.TabButton {
                    fontIcon: "\uf0c7"
                    text: "Save and exit"
                    onClicked: {
                        ExGlobals.Constants.proxy.saveProject()
                        Qt.quit()
                        dialog.close()
                    }
            }

            EaElements.TabButton {
                fontIcon: "\uf057"
                text: "Exit without saving"
                onClicked: {
                    dialog.close()
                    Qt.quit()
                }
            }
        }
    }
}

