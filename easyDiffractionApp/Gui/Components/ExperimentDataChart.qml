import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Window 2.12

import MatplotlibBackend 1.0

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    property bool showLegend: ExGlobals.Variables.showLegend

    color: EaStyle.Colors.mainContentBackground

    Rectangle {
        id: chartControlsContainer

        height: EaStyle.Sizes.toolButtonHeight + EaStyle.Sizes.fontPixelSize

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right

        color: EaStyle.Colors.mainContentBackground

        Row {
            anchors.centerIn: parent
            spacing: 5

            EaElements.ToolButton {
                fontIcon: "home"
                ToolTip.text: qsTr("Home")

                onClicked: _matplotlibBridge.home(experimentDataChart)
            }

            EaElements.ToolButton {
                fontIcon: "\uf2ea"
                ToolTip.text: qsTr("Back")

                onClicked: _matplotlibBridge.back(experimentDataChart)
            }

            EaElements.ToolButton {
                fontIcon: "\uf2f9"
                ToolTip.text: qsTr("Forward")

                onClicked: _matplotlibBridge.forward(experimentDataChart)
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
                    _matplotlibBridge.pan(experimentDataChart)
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
                    _matplotlibBridge.zoom(experimentDataChart)
                }
            }
        }
    }

    Rectangle {
        id: experimentDataChartContainer

        anchors.top: chartControlsContainer.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        onHeightChanged: ExGlobals.Constants.proxy.updateFigureMargins(experimentDataChart)
        onWidthChanged: ExGlobals.Constants.proxy.updateFigureMargins(experimentDataChart)

        color: EaStyle.Colors.mainContentBackground

        FigureCanvas {
            id: experimentDataChart
            objectName: "experimentDataChart"

            anchors.fill: parent

            anchors.topMargin: -0.5 * EaStyle.Sizes.fontPixelSize
            anchors.bottomMargin: EaStyle.Sizes.fontPixelSize
            anchors.leftMargin: EaStyle.Sizes.fontPixelSize
            anchors.rightMargin: EaStyle.Sizes.fontPixelSize

            dpi_ratio: Screen.devicePixelRatio

            Component.onCompleted: ExGlobals.Constants.proxy.setExperimentFigureCanvas(experimentDataChart)
        }
    }

    onShowLegendChanged: ExGlobals.Constants.proxy.showMatplotlibLegend(showLegend, experimentDataChart)
}


