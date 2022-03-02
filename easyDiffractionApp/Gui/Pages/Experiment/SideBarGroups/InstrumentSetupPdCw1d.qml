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
            text: qsTr("Zero shift")
        }

        EaElements.Parameter {
            width: inputFieldWidth()
            units: "deg" //ExGlobals.Constants.proxy.parameters.patternParametersAsObj.zero_shift.units
            text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.zero_shift.value)
            onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.zero_shift["@id"], text)
        }
    }

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("Wavelength")
        }

        EaElements.Parameter {
            width: inputFieldWidth()
            units: "Å" //ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.wavelength.units
            text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.wavelength.value)
            onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.wavelength["@id"], text)
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
