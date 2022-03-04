// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import easyApp.Gui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseQtCharts {
    measuredData: ExGlobals.Constants.proxy.plotting1d.qtchartsMeasuredDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.experimentPlotRangesObj

    xAxisTitle: {
        if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCW') {
            return "2θ (deg)"
        } else if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DTOF') {
            return "TOF (μs)"
        }
    }
    yMainAxisTitle: "Imeas"
}
