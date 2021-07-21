import QtQuick 2.13

import easyApp.Gui.Logic 1.0 as EaLogic
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseBokeh {
    measuredData: ExGlobals.Constants.proxy.plotting1d.bokehMeasuredDataObj
    calculatedData: ExGlobals.Constants.proxy.plotting1d.bokehCalculatedDataObj
    differenceData: ExGlobals.Constants.proxy.plotting1d.bokehDifferenceDataObj
    braggData: ExGlobals.Constants.proxy.plotting1d.bokehBraggDataObj
    backgroundData: ExGlobals.Constants.proxy.plotting1d.bokehBackgroundDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.analysisPlotRangesObj

    xAxisTitle: "2θ (deg)"
    yMainAxisTitle: {
        let title = 'Icalc'
        if (EaLogic.Utils.hasData(measuredData)) title = 'Imeas, ' + title
        if (EaLogic.Utils.hasData(backgroundData)) title = title + ', Ibkg'
        return title
    }
    yDifferenceAxisTitle: "Imeas - Icalc"

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}

