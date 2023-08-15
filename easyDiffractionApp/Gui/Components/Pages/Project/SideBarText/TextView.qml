// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Animations as EaAnimations
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


Rectangle {
    id: container

    width: EaStyle.Sizes.sideBarContentWidth
    height: 36 * EaStyle.Sizes.fontPixelSize +
            (applicationWindow.height - EaStyle.Sizes.appWindowMinimumHeight)

    color: enabled ? EaStyle.Colors.textViewBackground : EaStyle.Colors.textViewBackgroundDisabled
    Behavior on color { EaAnimations.ThemeChange {} }

    border.color: EaStyle.Colors.appBarComboBoxBorder

    // ListView
    ListView {
        id: listView

        anchors.fill: parent
        anchors.topMargin: EaStyle.Sizes.fontPixelSize
        anchors.bottomMargin: EaStyle.Sizes.fontPixelSize
        anchors.leftMargin: EaStyle.Sizes.fontPixelSize

        clip: true

        ScrollBar.vertical: EaElements.ScrollBar {
            policy: ScrollBar.AsNeeded
            interactive: false
        }

        model: [Globals.Proxies.main.project.dataBlockCif]

        // ListView Delegate
        delegate: TextEdit {
            readOnly: true

            font.family: EaStyle.Fonts.monoFontFamily
            font.pixelSize: EaStyle.Sizes.fontPixelSize

            color: !enabled || readOnly ?
                       EaStyle.Colors.themeForegroundMinor :
                       EaStyle.Colors.themeForeground
            Behavior on color { EaAnimations.ThemeChange {} }

            selectionColor: EaStyle.Colors.themeAccent
            Behavior on selectionColor { EaAnimations.ThemeChange {} }

            selectedTextColor: EaStyle.Colors.themeBackground
            Behavior on selectedTextColor { EaAnimations.ThemeChange {} }

            text: listView.model[index]
       }
        // ListView Delegate

    }
    // ListView
}
