import QtQuick 2.13

import Gui.Logic 1.0 as ExLogic
import Gui.Globals 1.0 as ExGlobals

Loader {
    source: {
        if (ExGlobals.Constants.proxy.current1dPlottingLib === 'qtcharts') {
            return ExLogic.Paths.component('ExperimentDataChartQtCharts.qml')
        } else if (ExGlobals.Constants.proxy.current1dPlottingLib === 'matplotlib') {
            return ExLogic.Paths.component('ExperimentDataChartMatplotlib.qml')
        } else if (ExGlobals.Constants.proxy.current1dPlottingLib === 'bokeh') {
            return ExLogic.Paths.component('ExperimentDataChartBokeh.qml')
        }
    }
}
