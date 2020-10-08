import easyAppGui.Globals 1.0 as EaGlobals

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

ExComponents.DataChartView {
    visible: ExGlobals.Variables.analysisPageEnabled

    showMeasured: true
}
