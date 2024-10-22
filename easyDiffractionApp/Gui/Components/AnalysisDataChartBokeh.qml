// SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseBokeh {
    measuredData: ExGlobals.Constants.proxy.plotting1d.bokehMeasuredDataObj
    calculatedData: ExGlobals.Constants.proxy.plotting1d.bokehCalculatedDataObj
    differenceData: ExGlobals.Constants.proxy.plotting1d.bokehDifferenceDataObj
    braggData: ExGlobals.Constants.proxy.plotting1d.bokehBraggDataObj
    backgroundData: ExGlobals.Constants.proxy.plotting1d.bokehBackgroundDataObj
    phaseData: ExGlobals.Constants.proxy.plotting1d.bokehPhasesDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.analysisPlotRangesObj
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
    yMainAxisTitle: {
        let title = 'Icalc'
        if (hasMeasuredData) title = 'Imeas, Icalc'
        if (hasBackgroundData) title += ', Ibkg'
        return title
    }
    yDifferenceAxisTitle: "Imeas - Icalc"

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}

