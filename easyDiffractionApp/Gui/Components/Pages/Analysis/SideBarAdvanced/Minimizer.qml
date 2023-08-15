// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


EaElements.GroupRow {

    EaElements.ComboBox {
        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3
        topInset: minimizerLabel.height
        topPadding: topInset + padding
        model: ['Lmfit']
        EaElements.Label {
            id: minimizerLabel
            text: qsTr("Minimizer")
            color: EaStyle.Colors.themeForegroundMinor
        }
    }

    EaElements.TextField {
        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3
        topInset: methodLabel.height
        topPadding: topInset + padding
        horizontalAlignment: TextInput.AlignLeft
        onAccepted: focus = false
        text: Globals.Proxies.main.fitting.minimizerMethod
        onTextEdited: Globals.Proxies.main.fitting.minimizerMethod = text
        EaElements.Label {
            id: methodLabel
            text: qsTr("Method")
            color: EaStyle.Colors.themeForegroundMinor
        }
    }

    EaElements.TextField {
        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3
        topInset: toleranceLabel.height
        topPadding: topInset + padding
        horizontalAlignment: TextInput.AlignLeft
        onAccepted: focus = false
        text: Globals.Proxies.main.fitting.minimizerTol
        onTextEdited: Globals.Proxies.main.fitting.minimizerTol = text
        EaElements.Label {
            id: toleranceLabel
            text: qsTr("Tolerance")
            color: EaStyle.Colors.themeForegroundMinor
        }
    }
}
