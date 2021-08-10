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

Row {
    spacing: EaStyle.Sizes.fontPixelSize * 0.5

    // Min
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: "ToF-min:"
    }
    EaElements.Parameter {
        id: xMin
        enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
        width: textFieldWidth()
        units: "μs"
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.simulationParametersAsObj.x_min, 3)
        onEditingFinished: updateParameters()
    }

    // Max
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: "ToF-max:"
    }
    EaElements.Parameter {
        id: xMax
        enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
        width: textFieldWidth()
        units: "μs"
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.simulationParametersAsObj.x_max, 3)
        onEditingFinished: updateParameters()
    }

    // Step
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: "ToF-step:"
    }
    EaElements.Parameter {
        id: xStep
        enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
        width: textFieldWidth()
        units: "μs"
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.simulationParametersAsObj.x_step, 3)
        onEditingFinished: updateParameters()
    }

    // Logic

    function labelWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - spacing * 5 - textFieldWidth() * 3) / 3
    }

    function textFieldWidth() {
        return EaStyle.Sizes.fontPixelSize * 7.0
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
