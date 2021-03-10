import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.ChemDoodleChartView {
    cifStr: JSON.stringify(ExGlobals.Constants.proxy.phasesAsExtendedCif)

    foregroundColor: EaStyle.Colors.themeForeground
    backgroundColor: EaStyle.Colors.chartPlotAreaBackground
}
