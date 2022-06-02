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
    columnSpacing: 2 * EaStyle.Sizes.fontPixelSize
    verticalItemAlignment: Grid.AlignVCenter

    EaElements.CheckBox {
        id: refinementSumCheckBox
        checked: ExGlobals.Constants.proxy.experiment.refineSum
        onCheckedChanged: ExGlobals.Constants.proxy.experiment.refineSum = checked
        text: qsTr("Up + Down")
    }

    EaElements.CheckBox {
        id: refinementDiffCheckBox
        checked: ExGlobals.Constants.proxy.experiment.refineDiff
        onCheckedChanged: ExGlobals.Constants.proxy.experiment.refineDiff = checked
        text: qsTr("Up - Down")
    }
    EaElements.CheckBox {
        id: refinementUpCheckBox
        checked: ExGlobals.Constants.proxy.experiment.refineUp
        onCheckedChanged: {
            ExGlobals.Constants.proxy.experiment.refineUp = checked;

        }
        text: qsTr("Up")
    }

    EaElements.CheckBox {
        id: refinementDownCheckBox
        checked: ExGlobals.Constants.proxy.experiment.refineDown
        onCheckedChanged: ExGlobals.Constants.proxy.experiment.refineDown = checked
        text: qsTr("Down")
    }
}
