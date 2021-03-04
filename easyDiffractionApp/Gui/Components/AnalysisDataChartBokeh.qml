import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BokehChartView {
    showMeasured: true
    showCalculated: true
    showBragg: true
    showDifference: true

    measuredData: ExGlobals.Constants.proxy.bokeh.measuredDataObj
    calculatedData: ExGlobals.Constants.proxy.bokeh.calculatedDataObj
    braggData: ExGlobals.Constants.proxy.bokeh.braggDataObj
    differenceData: ExGlobals.Constants.proxy.bokeh.differenceDataObj

    plotRanges: ExGlobals.Constants.proxy.bokeh.analysisPlotRangesObj

    xAxisTitle: qsTr("2theta (deg)")
    yMainAxisTitle: qsTr("Intensity")
    yDifferenceAxisTitle: qsTr("Difference")
}

