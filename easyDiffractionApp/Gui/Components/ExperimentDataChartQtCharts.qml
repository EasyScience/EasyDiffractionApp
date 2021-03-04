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

            min: ExGlobals.Constants.proxy.qtCharts.experimentPlotRangesObj.min_x
            max: ExGlobals.Constants.proxy.qtCharts.experimentPlotRangesObj.max_x
        }

        EaCharts.ValueAxis {
            id: axisY

            title: yAxisTitle

            min: ExGlobals.Constants.proxy.qtCharts.experimentPlotRangesObj.min_y
            max: ExGlobals.Constants.proxy.qtCharts.experimentPlotRangesObj.max_y
        }

        EaCharts.AreaSeries {
            color: EaStyle.Colors.chartForegrounds[0]

            axisX: axisX
            axisY: axisY

            lowerSeries: EaCharts.LineSeries {
                customPoints: ExGlobals.Constants.proxy.qtCharts.measuredDataObj.xy_lower
            }

            upperSeries: EaCharts.LineSeries {
                customPoints: ExGlobals.Constants.proxy.qtCharts.measuredDataObj.xy_upper
            }
        }
    }
}
