import QtQuick 2.13

import Gui.Globals 1.0 as ExGlobals

Loader {
    source: ExGlobals.Constants.proxy.current1dPlottingLib === 'matplotlib' ?
                "../../Components/ExperimentDataChartMatplotlib.qml" :
                "../../Components/ExperimentDataChartQtCharts.qml"
}
