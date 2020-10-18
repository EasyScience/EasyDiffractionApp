import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents
import QtQuick 2.13
import QtQuick.Controls 2.13
import Backend 1.0

Column {

    FigureCanvas {
        id: mplView
        objectName : "figure"
        dpi_ratio: Screen.devicePixelRatio
        anchors.fill: parent
    }

    Row {
        ToolButton {
            text: qsTr("home")
            onClicked: {
                displayBridge.home();
            }
        }

        Button {
            text: qsTr("back")
            onClicked: {
                displayBridge.back();
            }
        }

        Button {
            text: qsTr("forward")
            onClicked: {
                displayBridge.forward();
            }
        }

        ToolSeparator{}

        Button {
            id: pan
            text: qsTr("pan")
            checkable: true
            onClicked: {
                if (zoom.checked) {
                    zoom.checked = false;
                }
                displayBridge.pan();
            }
        }

        Button {
            id: zoom
            text: qsTr("zoom")
            checkable: true
            onClicked: {
                if (pan.checked) {
                    // toggle pan off
                    pan.checked = false;
                }
                displayBridge.zoom();
            }
        }
        ToolSeparator {}
        TextInput {
            id: location
            readOnly: true
            text: displayBridge.coordinates
        }
    }
}