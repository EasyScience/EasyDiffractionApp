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

    // Zero shift
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("Zero:")
    }
    EaElements.Parameter {
        width: inputFieldWidth()
        units: "μs"
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.zero_shift.value)
        onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.zero_shift["@id"], text)
    }

    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("2θ:")
    }
    EaElements.Parameter {
        width: inputFieldWidth()
        units: "deg"
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.ttheta_bank.value)
        onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.ttheta_bank["@id"], text)
    }

    // Dtt1/DIFC
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("Dtt1:")
    }
    EaElements.Parameter {
        width: inputFieldWidth()
        units: "" // "μs/Å" ???
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.dtt1.value)
        onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.dtt1["@id"], text)
    }

    // Dtt2/DIFA
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("Dtt2:")
    }
    EaElements.Parameter {
        width: inputFieldWidth()
        units: "" // ???
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.dtt2.value)
        onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.dtt2["@id"], text)
    }

    // Logic

    function labelWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - spacing * 7 - inputFieldWidth() * 4) / 4
    }

    function inputFieldWidth() {
        return EaStyle.Sizes.fontPixelSize * 5.0
    }

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }
}
