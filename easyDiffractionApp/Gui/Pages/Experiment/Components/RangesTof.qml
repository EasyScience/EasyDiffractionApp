// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals


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

