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
            text: (ExGlobals.Constants.proxy.experiment.isSpinPolarized ?
                EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.beam.polarization.value * 100.0) :
                qsTr(""))
            onEditingFinished:{
                var value = Number(text)/100.0;
                var value_string = value.toString();
                editParameterValue(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.beam.polarization["@id"], value_string)
            }

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
            text: (ExGlobals.Constants.proxy.experiment.isSpinPolarized ?
                EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.beam.efficiency.value * 100.0) :
                qsTr(""))
            onEditingFinished: {
                var value = Number(text)/100.0;
                var value_string = value.toString();
                editParameterValue(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.beam.efficiency["@id"], value_string)
            }
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
