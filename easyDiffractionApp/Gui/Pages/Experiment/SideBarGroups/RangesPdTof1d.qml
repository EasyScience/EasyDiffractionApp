// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals


// sigma (Gaussian width), gamma (Lorentzian width), alpha/beta (TOF width)

// CW
// U, V, W (float) Cagliotti profile coefficients for Gaussian instrumental broadening
// X, Y, Z (float) Cauchy (Lorentzian) instrumental broadening coefficients

// GSAS... TOF
// alpha - Exponential rise profile coefficients
// beta-0 beta-1 beta-q - Exponential decay profile coefficients
// sig-0 sig-1 sig-2 sig-q - Gaussian profile coefficients
// X,Y,Z - Lorentzian profile coefficients

// FP... TOF
// ALPH0, BETA0, ALPH1, BETA1 - Exponential decay parameters for TOF patterns

// GSAS... TOF: Thus the two convolutions between the Ikeda-Carpenter function and a Gaussian and Lorentzian are needed. The Gaussian part is
// FP... Npr=9 T.O.F. Convolution pseudo-Voigt with back-to-back exponential functions
// FP... convolution of a double exponential with a TCH pseudo-Voigt for TOF.
// ... Thompson-Cox-Hasting (TCH) pseudo-Voigt peak profile function h

// ???
// alpha, beta-0, beta-1, beta-q - TOF profile terms
// sig-0, sig-1, sig-2, sig-q - TOF profile terms
// U, V, W - Gaussian peak profile terms
// X, Y, Z - Lorentzian peak profile terms


Grid {
    columns: 3
    columnSpacing: EaStyle.Sizes.fontPixelSize

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("ToF-min")
        }

        EaElements.Parameter {
            id: xMin
            enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
            width: inputFieldWidth()
            units: "μs"
            text: formatParameter(ExGlobals.Constants.proxy.parameters.simulationParametersAsObj.x_min)
            onEditingFinished: updateParameters()
        }
    }

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("ToF-max")
        }

        EaElements.Parameter {
            id: xMax
            enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
            width: inputFieldWidth()
            units: "μs"
            text: formatParameter(ExGlobals.Constants.proxy.parameters.simulationParametersAsObj.x_max)
            onEditingFinished: updateParameters()
        }
    }

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("ToF-step")
        }

        EaElements.Parameter {
            id: xStep
            enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
            width: inputFieldWidth()
            units: "μs"
            text: formatParameter(ExGlobals.Constants.proxy.parameters.simulationParametersAsObj.x_step)
            onEditingFinished: updateParameters()
        }
    }

    // Logic

    function inputFieldWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - columnSpacing * (columns - 1)) / columns
    }

    function formatParameter(value) {
        return EaLogic.Utils.toFixed(value, 0)
    }

    function updateParameters() {
        const json = {
            "x_min": parseFloat(xMin.text),
            "x_max": parseFloat(xMax.text),
            "x_step": parseFloat(xStep.text)
        }
        ExGlobals.Constants.proxy.parameters.simulationParametersAsObj = JSON.stringify(json)
    }
}

