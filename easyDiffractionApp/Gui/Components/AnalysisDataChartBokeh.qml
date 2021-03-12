import QtQuick 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseBokeh {
    measuredData: ExGlobals.Constants.proxy.plotting1d.bokehMeasuredDataObj
    calculatedData: ExGlobals.Constants.proxy.plotting1d.bokehCalculatedDataObj
    braggData: ExGlobals.Constants.proxy.plotting1d.bokehBraggDataObj
    differenceData: ExGlobals.Constants.proxy.plotting1d.bokehDifferenceDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.analysisPlotRangesObj

    xAxisTitle: qsTr("2theta (deg)")
    yMainAxisTitle: qsTr("Intensity")
    yDifferenceAxisTitle: qsTr("Difference")

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}

