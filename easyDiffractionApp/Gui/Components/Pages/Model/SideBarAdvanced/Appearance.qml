// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


EaElements.GroupColumn {

    EaElements.CheckBox {
        text: qsTr('Display coordinate vectors')
        checked: Globals.Vars.showCoordinateVectorsOnModelPage
        onCheckedChanged: Globals.Vars.showCoordinateVectorsOnModelPage = checked
    }

}
