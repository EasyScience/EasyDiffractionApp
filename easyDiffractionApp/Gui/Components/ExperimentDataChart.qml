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
    property bool isExperimentStepDone: ExGlobals.Variables.experimentLoaded || ExGlobals.Variables.experimentSkipped

    color: "white"

    FigureCanvas {
        id: experimentDataChart
        objectName: "experimentDataChart"

        anchors.fill: parent
        anchors.topMargin: -25
        anchors.bottomMargin: 0
        anchors.rightMargin: -55
        dpi_ratio: Screen.devicePixelRatio

        Component.onCompleted: ExGlobals.Constants.proxy.setExperimentFigureObjName(objectName)
    }

    Row {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 10
        spacing: 5

        EaElements.ToolButton {
            fontIcon: "home"
            ToolTip.text: qsTr("Home")

            onClicked: _matplotlibBridge.home(experimentDataChart.objectName)
        }

        EaElements.ToolButton {
            fontIcon: "\uf2ea"
            ToolTip.text: qsTr("Back")

            onClicked: _matplotlibBridge.back(experimentDataChart.objectName)
        }

        EaElements.ToolButton {
            fontIcon: "\uf2f9"
            ToolTip.text: qsTr("Forward")

            onClicked: _matplotlibBridge.forward(experimentDataChart.objectName)
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
                _matplotlibBridge.pan(experimentDataChart.objectName)
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
                _matplotlibBridge.zoom(experimentDataChart.objectName)
            }
        }
    }

    onIsDarkThemeChanged: updateMatplotlibStyle()
    onIsExperimentStepDoneChanged: updateMatplotlibStyle()

    // Logic

    function updateMatplotlibStyle() {
        _matplotlibBridge.updateFont(EaStyle.Fonts.fontSource,
                                     experimentDataChart.objectName)
        _matplotlibBridge.updateStyle(EaStyle.Colors.isDarkTheme,
                                      EaStyle.Colors.matplotlibRcParams,
                                      experimentDataChart.objectName)
    }
}

