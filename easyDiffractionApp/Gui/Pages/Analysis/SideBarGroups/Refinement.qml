// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Row {
    spacing: 2 * EaStyle.Sizes.fontPixelSize

    EaElements.CheckBox {
        topPadding: 0

        text: "\u2191 + \u2193"
        ToolTip.text: qsTr("Sum: spin-up \uff0b spin-down component")

        checked: ExGlobals.Constants.proxy.experiment.refineSum
        onCheckedChanged: ExGlobals.Constants.proxy.experiment.refineSum = checked
    }

    EaElements.CheckBox {
        topPadding: 0

        text: "\u2191 \u2212 \u2193"
        ToolTip.text: qsTr("Difference: spin-up \uff0d spin-down component")

        checked: ExGlobals.Constants.proxy.experiment.refineDiff
        onCheckedChanged: ExGlobals.Constants.proxy.experiment.refineDiff = checked
    }

    EaElements.CheckBox {
        topPadding: 0

        text: "\u2191"
        ToolTip.text: qsTr("Spin-up component")

        checked: ExGlobals.Constants.proxy.experiment.refineUp
        onCheckedChanged: ExGlobals.Constants.proxy.experiment.refineUp = checked
    }

    EaElements.CheckBox {
        topPadding: 0

        text: "\u2193"
        ToolTip.text: qsTr("Spin-down component")

        checked: ExGlobals.Constants.proxy.experiment.refineDown
        onCheckedChanged: ExGlobals.Constants.proxy.experiment.refineDown = checked
    }
}
