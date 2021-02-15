import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BokehChartView {
    measuredData: ExGlobals.Constants.proxy.bokeh.measuredDataObj

    xAxisTitle: qsTr("2theta (deg)")
    yAxisTitle: qsTr("Intensity")

    experimentLineColor: EaStyle.Colors.chartForegrounds[0]
    calculatedLineColor: EaStyle.Colors.chartForegrounds[1]

    backgroundColor: EaStyle.Colors.chartPlotAreaBackground
}

