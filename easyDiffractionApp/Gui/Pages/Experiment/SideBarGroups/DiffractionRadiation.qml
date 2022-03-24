// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals


Grid {
    columns: 2
    columnSpacing: EaStyle.Sizes.fontPixelSize

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("Polarization")
        }

        EaElements.Parameter {
            width: inputFieldWidth()
            units: "%"
            text: "0.0"
            // text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.polarization.value)
            // onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.polarization["@id"], text)
        }
    }

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("Polarizing efficiency")
        }

        EaElements.Parameter {
            width: inputFieldWidth()
            units: "%"
            text: "100.0"
            // text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.polarizing_efficiency.value)
            // onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.polarizing_efficiency["@id"], text)
        }
    }

    // Logic

    function inputFieldWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - columnSpacing * (columns - 1)) / columns
    }

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }
}
