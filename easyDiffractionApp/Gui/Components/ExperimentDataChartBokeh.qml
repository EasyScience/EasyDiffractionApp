// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick

import easyApp.Gui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseBokeh {
    measuredData: ExGlobals.Constants.proxy.plotting1d.bokehMeasuredDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.experimentPlotRangesObj

    isSpinPolarized: ExGlobals.Constants.proxy.experiment.isSpinPolarized
    setSpinComponent: ExGlobals.Constants.proxy.experiment.setSpinComponent
    spinComponent: ExGlobals.Constants.proxy.experiment.spinComponent

    xAxisTitle: {
        if ((ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCW') || (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCWpol')) {
            return "2θ (deg)"
        } else if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DTOF') {
            return "TOF (μs)"
        }
    }
    yMainAxisTitle: "Imeas"
}
