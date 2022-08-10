// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Animations 1.0 as EaAnimations
import easyApp.Gui.Elements 1.0 as EaElements

Rectangle {
    color: EaStyle.Colors.contentBackground
    Behavior on color { EaAnimations.ThemeChange {} }

    EaElements.Label {
        enabled: false
        anchors.centerIn: parent
        font.family: EaStyle.Fonts.secondFontFamily
        font.pixelSize: EaStyle.Sizes.fontPixelSize * 3
        font.weight: Font.ExtraLight
        text: 'Not implemented'
    }
}
