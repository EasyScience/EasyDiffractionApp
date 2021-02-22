import QtQuick 2.13
import QtQuick.Controls 2.13
import QtCharts 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    property string xAxisTitle: qsTr("2theta (deg)")
    property string yAxisTitle: qsTr("Intensity")

    color: EaStyle.Colors.mainContentBackground

    EaCharts.ChartView {
        anchors.fill: parent

        anchors.margins: -12 + EaStyle.Sizes.fontPixelSize * 2

        EaCharts.ValueAxis {
            id: axisX

            title: xAxisTitle

            min: ExGlobals.Constants.proxy.qtCharts.experimentXmin
            max: ExGlobals.Constants.proxy.qtCharts.experimentXmax
        }

        EaCharts.ValueAxis {
            id: axisY

            title: yAxisTitle

            min: ExGlobals.Constants.proxy.qtCharts.experimentYmin
            max: ExGlobals.Constants.proxy.qtCharts.experimentYmax
        }

        EaCharts.AreaSeries {
            color: EaStyle.Colors.chartForegrounds[0]

            axisX: axisX
            axisY: axisY

            lowerSeries: LineSeries {
                id: measuredLower
                Component.onCompleted: ExGlobals.Constants.proxy.qtCharts.setExperimentMeasuredLower(measuredLower)
            }

            upperSeries: LineSeries {
                id: measuredUpper
                Component.onCompleted: ExGlobals.Constants.proxy.qtCharts.setExperimentMeasuredUpper(measuredUpper)
            }
        }
    }
}
