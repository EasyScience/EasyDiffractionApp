import QtQuick 2.13

import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseQtCharts {
    measuredData: ExGlobals.Constants.proxy.qtCharts.measuredDataObj
    calculatedData: ExGlobals.Constants.proxy.qtCharts.calculatedDataObj
    braggData: ExGlobals.Constants.proxy.qtCharts.braggDataObj
    differenceData: ExGlobals.Constants.proxy.qtCharts.differenceDataObj

    plotRanges: ExGlobals.Constants.proxy.qtCharts.analysisPlotRangesObj

    xAxisTitle: qsTr("2theta (deg)")
    yMainAxisTitle: qsTr("Intensity")
    yDifferenceAxisTitle: qsTr("Difference")

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}
