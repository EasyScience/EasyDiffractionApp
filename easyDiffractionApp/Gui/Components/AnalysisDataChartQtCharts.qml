import QtQuick 2.13
import QtQuick.Controls 2.13
import QtCharts 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    property bool showMeasured: false
    property bool showDifference: false

    property string xAxisTitle: qsTr("2theta (deg)")
    property string mainYAxisTitle: qsTr("Intensity")
    property string differenceYAxisTitle: qsTr("Difference")

    color: EaStyle.Colors.mainContentBackground

    // Main (top) chart

    EaCharts.ChartView {
        id: mainChart

        anchors.top: parent.top
        anchors.bottom: differenceChart.top
        anchors.left: parent.left
        anchors.right: parent.right

        anchors.margins: -12 + EaStyle.Sizes.fontPixelSize * 2
        anchors.bottomMargin: differenceChart.visible ? 0 : anchors.topMargin

        //antialiasing: true

        EaCharts.ValueAxis {
            id: axisX
            title: xAxisTitle
            titleVisible: !differenceChart.visible
            //labelsVisible: !differenceChart.visible
            min: ExGlobals.Constants.proxy.qtCharts.analysisXmin
            max: ExGlobals.Constants.proxy.qtCharts.analysisXmax

            //onRangeChanged: { print("X 1:", min, max); applyNiceNumbers(); print("X 2:", min, max) }
        }

        EaCharts.ValueAxis {
            id: axisY

            title: mainYAxisTitle
            min: ExGlobals.Constants.proxy.qtCharts.analysisYmin
            max: ExGlobals.Constants.proxy.qtCharts.analysisYmax

            //onRangeChanged: { print("Y 1:", min, max); applyNiceNumbers(); print("Y 2:", min, max) }
        }

        EaCharts.AreaSeries {
            visible: ExGlobals.Constants.proxy.showMeasuredSeries

            color: EaStyle.Colors.chartForegrounds[0]

            axisX: axisX
            axisY: axisY

            lowerSeries: LineSeries {
                id: measuredLower
                Component.onCompleted: ExGlobals.Constants.proxy.qtCharts.setAnalysisMeasuredLower(measuredLower)
            }

            upperSeries: LineSeries {
                id: measuredUpper
                Component.onCompleted: ExGlobals.Constants.proxy.qtCharts.setAnalysisMeasuredUpper(measuredUpper)
            }
        }

        EaCharts.LineSeries {
            id: calculated

            color: EaStyle.Colors.chartForegrounds[1]

            axisX: axisX
            axisY: axisY

            Component.onCompleted: ExGlobals.Constants.proxy.qtCharts.setAnalysisCalculated(calculated)
        }
    }

    // Difference (bottom) chart

    EaCharts.ChartView {
        id: differenceChart

        visible: ExGlobals.Constants.proxy.showDifferenceChart && ExGlobals.Variables.experimentLoaded

        height: visible ? 0.3 * parent.height : 0

        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        anchors.margins: visible ? -12 + EaStyle.Sizes.fontPixelSize * 2 : 0
        anchors.topMargin: 0

        allowZoom: false
        animationDuration: mainChart.animationDuration

        //antialiasing: true

        EaCharts.AreaSeries {
            color: EaStyle.Colors.chartForegrounds[2]

            axisX: EaCharts.ValueAxis {
                title: xAxisTitle
                min: axisX.min
                max: axisX.max
            }

            axisY: EaCharts.ValueAxis {
                title: differenceYAxisTitle

                tickType: ValueAxis.TicksFixed
                tickCount: 3

                min: ExGlobals.Constants.proxy.qtCharts.differenceYmin
                max: ExGlobals.Constants.proxy.qtCharts.differenceYmax
            }

            lowerSeries: LineSeries {
                id: differenceLower
                Component.onCompleted: ExGlobals.Constants.proxy.qtCharts.setAnalysisDifferenceLower(differenceLower)
            }

            upperSeries: LineSeries {
                id: differenceUpper
                Component.onCompleted: ExGlobals.Constants.proxy.qtCharts.setAnalysisDifferenceUpper(differenceUpper)
            }
        }
    }
}
