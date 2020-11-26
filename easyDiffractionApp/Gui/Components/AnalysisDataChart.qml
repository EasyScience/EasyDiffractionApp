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

    color: EaStyle.Colors.mainContentBackground

    Rectangle {
        id: chartControlsContainer

        z: 900

        height: 50

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

                onClicked: _matplotlibBridge.home(analysisDataChart.objectName)
            }

            EaElements.ToolButton {
                fontIcon: "\uf2ea"
                ToolTip.text: qsTr("Back")

                onClicked: _matplotlibBridge.back(analysisDataChart.objectName)
            }

            EaElements.ToolButton {
                fontIcon: "\uf2f9"
                ToolTip.text: qsTr("Forward")

                onClicked: _matplotlibBridge.forward(analysisDataChart.objectName)
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
                    _matplotlibBridge.pan(analysisDataChart.objectName)
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
                    _matplotlibBridge.zoom(analysisDataChart.objectName)
                }
            }
        }
    }

    Rectangle {
        id: analysisDataChartContainer

        z: 800

        anchors.top: chartControlsContainer.bottom
        anchors.bottom: differenceDataChartContainer.top
        anchors.left: parent.left
        anchors.right: parent.right

        color: EaStyle.Colors.mainContentBackground

        FigureCanvas {
            id: analysisDataChart
            objectName: "analysisDataChart"

            anchors.fill: parent

            anchors.topMargin: -52
            anchors.bottomMargin: 0
            anchors.leftMargin: 5
            anchors.rightMargin: -50

            dpi_ratio: Screen.devicePixelRatio

            Component.onCompleted: ExGlobals.Constants.proxy.setAnalysisFigureObjName(objectName)
        }
    }

    Rectangle {
        id: differenceDataChartContainer

        height: ExGlobals.Variables.experimentLoaded ? parent.height * 0.3 : 0

        anchors.bottom: parent.bottom
        anchors.left: analysisDataChartContainer.anchors.left
        anchors.right: analysisDataChartContainer.anchors.right


        color: EaStyle.Colors.mainContentBackground

        FigureCanvas {
            id: differenceDataChart
            objectName: "differenceDataChart"

            anchors.fill: parent

            anchors.topMargin: 0
            anchors.bottomMargin: 15
            anchors.leftMargin: analysisDataChart.anchors.leftMargin
            anchors.rightMargin: analysisDataChart.anchors.rightMargin

            dpi_ratio: Screen.devicePixelRatio

            Component.onCompleted: ExGlobals.Constants.proxy.setDifferenceFigureObjName(objectName)
        }
    }

    onIsDarkThemeChanged: updateMatplotlibStyle()
    onIsExperimentStepDoneChanged: updateMatplotlibStyle()

    // Logic

    function updateMatplotlibStyle() {
        _matplotlibBridge.updateFont(EaStyle.Fonts.fontSource,
                                     analysisDataChart.objectName)
        _matplotlibBridge.updateStyle(EaStyle.Colors.isDarkTheme,
                                      EaStyle.Colors.matplotlibRcParams,
                                      analysisDataChart.objectName)
    }
}
