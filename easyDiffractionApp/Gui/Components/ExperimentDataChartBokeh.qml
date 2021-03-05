import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BokehChartView {
    measuredData: ExGlobals.Constants.proxy.bokeh.measuredDataObj

    plotRanges: ExGlobals.Constants.proxy.bokeh.experimentPlotRangesObj

    xAxisTitle: qsTr("2theta (deg)")
    yMainAxisTitle: qsTr("Intensity")
}

