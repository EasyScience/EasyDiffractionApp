import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Window 2.12

import MatplotlibBackend 1.0

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

Rectangle {
    property bool isDarkTheme: EaStyle.Colors.isDarkTheme
    property var matplotlibRcParams: EaStyle.Colors.matplotlibRcParams
    onIsDarkThemeChanged: displayBridge.updateStyle(isDarkTheme, matplotlibRcParams)
    Component.onCompleted: {
        displayBridge.updateFont(EaStyle.Fonts.fontSource)
        displayBridge.updateStyle(isDarkTheme, matplotlibRcParams)
    }

    color: "white"

    FigureCanvas {
        objectName: "figure"

        anchors.fill: parent
        anchors.topMargin: -25
        anchors.bottomMargin: 0
        anchors.rightMargin: -55
        dpi_ratio: Screen.devicePixelRatio
    }

    Row {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 10
        spacing: 5

        EaElements.ToolButton {
            fontIcon: "home"
            ToolTip.text: qsTr("Home")

            onClicked: displayBridge.home()
        }

        EaElements.ToolButton {
            fontIcon: "\uf2ea"
            ToolTip.text: qsTr("Back")

            onClicked: displayBridge.back()
        }

        EaElements.ToolButton {
            fontIcon: "\uf2f9"
            ToolTip.text: qsTr("Forward")

            onClicked: displayBridge.forward()
        }

        Rectangle {
            width: 4
            height: 4
            radius: 2
            anchors.verticalCenter: parent.verticalCenter
            color: EaStyle.Colors.themeForeground
        }

        EaElements.ToolButton {
            id: pan

            fontIcon: "arrows-alt"
            ToolTip.text: qsTr("Pan")
            checkable: true

            onClicked: {
                if (zoom.checked) {
                    zoom.checked = false
                }
                displayBridge.pan()
            }
        }

        EaElements.ToolButton {
            id: zoom

            fontIcon: "expand"
            ToolTip.text: qsTr("Zoom")
            checkable: true

            onClicked: {
                if (pan.checked) {
                    pan.checked = false
                }
                displayBridge.zoom()
            }
        }
    }
}
