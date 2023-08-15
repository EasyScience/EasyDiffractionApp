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
    height: 34.5 * EaStyle.Sizes.fontPixelSize +
            (applicationWindow.height - EaStyle.Sizes.appWindowMinimumHeight)

    color: enabled ? EaStyle.Colors.textViewBackground : EaStyle.Colors.textViewBackgroundDisabled
    Behavior on color { EaAnimations.ThemeChange {} }

    border.color: EaStyle.Colors.appBarComboBoxBorder

    // ListView
    ListView {
        id: listView

        property var firstDelegateRef: null
        property bool cifEdited: {
            //console.error(Globals.Proxies.main.model.currentIndex)
            //console.error(JSON.stringify(Globals.Proxies.main.model.dataBlocksCif))
            //console.error(Globals.Proxies.main.model.currentIndex)

            listView.firstDelegateRef === null || typeof Globals.Proxies.main.model.dataBlocksCif[Globals.Proxies.main.model.currentIndex] === 'undefined' ?
                                     false :
                                     listView.firstDelegateRef.text !== Globals.Proxies.main.model.dataBlocksCif[Globals.Proxies.main.model.currentIndex][0]
        }

        anchors.fill: parent
        anchors.topMargin: EaStyle.Sizes.fontPixelSize
        anchors.bottomMargin: EaStyle.Sizes.fontPixelSize
        anchors.leftMargin: EaStyle.Sizes.fontPixelSize

        clip: true

        ScrollBar.vertical: EaElements.ScrollBar {
            policy: ScrollBar.AsNeeded
            interactive: false
        }

        model: Globals.Proxies.main.model.dataBlocksCif[Globals.Proxies.main.model.currentIndex]

        // ListView Delegate
        delegate: TextEdit {
            readOnly: true

            font.family: EaStyle.Fonts.monoFontFamily
            font.pixelSize: EaStyle.Sizes.fontPixelSize

            color: !enabled || readOnly ?
                       EaStyle.Colors.themeForegroundDisabled :
                       EaStyle.Colors.themeForeground
            Behavior on color { EaAnimations.ThemeChange {} }

            selectionColor: EaStyle.Colors.themeAccent
            Behavior on selectionColor { EaAnimations.ThemeChange {} }

            selectedTextColor: EaStyle.Colors.themeBackground
            Behavior on selectedTextColor { EaAnimations.ThemeChange {} }

            text: listView.model[index]

            Component.onCompleted: {
                if (index === 0) {
                    readOnly = false
                    listView.firstDelegateRef = this
                }
            }
       }
        // ListView Delegate

    }
    // ListView

    // Tool buttons
    Row {
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.topMargin: EaStyle.Sizes.fontPixelSize
        anchors.rightMargin: EaStyle.Sizes.fontPixelSize
        spacing: 0.25 * EaStyle.Sizes.fontPixelSize

        EaElements.TabButton {
            enabled: listView.cifEdited
            highlighted: listView.cifEdited
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "check"
            ToolTip.text: qsTr("Apply changes")
            //onClicked: forceActiveFocus()
            onClicked: {
                Globals.Proxies.main.model.replaceModel(listView.firstDelegateRef.text)
                forceActiveFocus()
            }
        }
    }
    // Tool buttons
}
