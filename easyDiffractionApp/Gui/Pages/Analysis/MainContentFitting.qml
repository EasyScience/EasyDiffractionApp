import QtQuick 2.13

import Gui.Globals 1.0 as ExGlobals

Loader {
    source: ExGlobals.Constants.proxy.currentPlottingLib === 'matplotlib' ?
                "../../Components/AnalysisDataChartMatplotlib.qml" :
                "../../Components/AnalysisDataChartQtCharts.qml"
}
