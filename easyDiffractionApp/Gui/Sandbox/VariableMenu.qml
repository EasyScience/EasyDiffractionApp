// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
//import QtQuick.Controls.Material

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

Window {
    visible: true
    width: 350
    height: 100

    // Menu
    EaElements.Menu {
        id: contextMenu

        width: layout.implicitWidth

        // Layout
        Grid {
            id: layout

            leftPadding: 1.25 * EaStyle.Sizes.fontPixelSize
            rightPadding: 1.25 * EaStyle.Sizes.fontPixelSize
            topPadding: 0.5 * EaStyle.Sizes.fontPixelSize
            bottomPadding: 0.75 * EaStyle.Sizes.fontPixelSize
            rowSpacing: 0.75 * EaStyle.Sizes.fontPixelSize
            columnSpacing: 1.5 * EaStyle.Sizes.fontPixelSize

            rows: 2

            // Header
            EaElements.Label {
                color: EaStyle.Colors.themeForegroundMinor
                text: 'name'
            }
            EaElements.Label {
                color: EaStyle.Colors.themeForegroundMinor
                text: 'value'
            }
            EaElements.Label {
                color: EaStyle.Colors.themeForegroundMinor
                text: 'error'
            }
            EaElements.Label {
                color: EaStyle.Colors.themeForegroundMinor
                text: 'vary'
            }
            // Headert

            // Content
            EaElements.Button {
                text: '_cell_length_a'
                checked: true
                onClicked: Qt.openUrlExternally("https://github.com/EasyScience/EasyExampleApp")
            }

            EaElements.Label {
                text: '10.3381'
                font.bold: varyCheckBox.checked
            }
            EaElements.Label {
                text: '0.0275'
            }
            EaElements.CheckBox {
                id: varyCheckBox
                padding: 0
                checked: true
            }
            // Content
        }
        // Layout
    }
    // Menu

    Component.onCompleted: {
        EaStyle.Colors.theme = EaStyle.Colors.LightTheme
        contextMenu.open()
    }

}
