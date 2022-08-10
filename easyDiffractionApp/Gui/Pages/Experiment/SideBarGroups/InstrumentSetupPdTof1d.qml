// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals


Grid {
    columns: 4
    columnSpacing: EaStyle.Sizes.fontPixelSize

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("Zero shift")
        }

        EaElements.Parameter {
            width: inputFieldWidth()
            units: "μs"
            text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.zero_shift.value)
            onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.zero_shift["@id"], text)
        }
    }

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("2θ detector bank")
        }

        EaElements.Parameter {
            width: inputFieldWidth()
            units: "deg"
            text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.ttheta_bank.value)
            onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.ttheta_bank["@id"], text)
        }
    }

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("Dtt1 / DIFC")
        }

        EaElements.Parameter {
            width: inputFieldWidth()
            units: "" // "μs/Å" ???
            text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.dtt1.value)
            onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.dtt1["@id"], text)
        }
    }

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("Dtt2 / DIFA")
        }

        EaElements.Parameter {
            width: inputFieldWidth()
            units: "" // ???
            text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.dtt2.value)
            onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.dtt2["@id"], text)
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

