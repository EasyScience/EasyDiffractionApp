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
    onIsDarkThemeChanged: _matplotlibBridge.updateStyle(isDarkTheme, matplotlibRcParams)
    Component.onCompleted: {
        _matplotlibBridge.updateFont(EaStyle.Fonts.fontSource, experimentDataChart.objectName)
        _matplotlibBridge.updateStyle(isDarkTheme, matplotlibRcParams, experimentDataChart.objectName)
    }

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
}


/*
import QtQuick 2.13
import QtQuick.Controls 2.13
import QtCharts 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    property bool showMeasured: false
    property bool showCalculated: false
    property bool showDifference: false

    color: EaStyle.Colors.mainContentBackground

    EaCharts.ChartView {
        anchors.fill: parent

        EaCharts.ValueAxis {
            id: axisX

            title: "2theta (deg)"

            tickCount: 4

            min: 0
            max: 10
        }

        EaCharts.ValueAxis {
            id: axisY

            title: "Intensity (arb. units)"

            min: -6
            max: 6
        }

        EaCharts.AreaSeries {
            visible: showMeasured

            axisX: axisX
            axisY: axisY

            lowerSeries: LineSeries {
                id: lowerMeasuredSeries

                // defult points
                XYPoint { x: 0; y: -3.8 }
                XYPoint { x: 1; y: -2.7 }
                XYPoint { x: 2; y:  0.2 }
                XYPoint { x: 3; y:  2.1 }
                XYPoint { x: 4; y:  3.2 }
                XYPoint { x: 5; y:  2.2 }
                XYPoint { x: 6; y:  0.1 }
                XYPoint { x: 7; y: -2.3 }
                XYPoint { x: 8; y: -3.6 }
                XYPoint { x: 9; y: -2.7 }
                XYPoint { x: 9.4; y: -2.2 }

                ///Component.onCompleted: ExGlobals.Constants.proxy.addLowerMeasuredSeriesRef(lowerMeasuredSeries)
            }

            upperSeries: LineSeries {
                id: upperMeasuredSeries

                // defult points
                XYPoint { x: 0; y: -3.2 }
                XYPoint { x: 1; y: -2.1 }
                XYPoint { x: 2; y:  0.6 }
                XYPoint { x: 3; y:  2.8 }
                XYPoint { x: 4; y:  3.7 }
                XYPoint { x: 5; y:  2.5 }
                XYPoint { x: 6; y:  0.7 }
                XYPoint { x: 7; y: -2.1 }
                XYPoint { x: 8; y: -3.1 }
                XYPoint { x: 9; y: -2.2 }
                XYPoint { x: 9.4; y: -2.0 }

                ///Component.onCompleted: ExGlobals.Constants.proxy.addUpperMeasuredSeriesRef(upperMeasuredSeries)
            }
        }

        EaCharts.LineSeries {
            id: calculatedSeries

            visible: showCalculated

            axisX: axisX
            axisY: axisY

            // defult points
            XYPoint { x: 0; y: -3 }
            XYPoint { x: 1; y: -2 }
            XYPoint { x: 2; y:  0 }
            XYPoint { x: 3; y:  2 }
            XYPoint { x: 4; y:  3 }
            XYPoint { x: 5; y:  2 }
            XYPoint { x: 6; y:  0 }
            XYPoint { x: 7; y: -2 }
            XYPoint { x: 8; y: -3 }
            XYPoint { x: 9; y: -2 }
            XYPoint { x: 9.4; y: -1 }

            Component.onCompleted: {
                if (visible) {
                    ExGlobals.Constants.proxy.setCalculatedSeriesRef(calculatedSeries)
                }
            }
        }
    }
}
*/

