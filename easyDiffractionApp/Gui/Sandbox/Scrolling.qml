// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents


Rectangle {
    property int numLabels: 50

    width: 300
    height: 500
    color: '#444'

    // EaComponents.SideBarColumn
    EaComponents.SideBarColumn {
        anchors.fill: parent

        // EaElements.GroupBox
        EaElements.GroupBox {
            title: qsTr("Scrolling example")
            collapsed: false
            last: true

            // Column
            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                // Repeater
                Repeater {
                    model: numLabels

                    EaElements.Label {
                        text: `Label ${index+1} of ${numLabels}`
                    }
                }
                // Repeater
            }
            // Column
        }
        // EaElements.GroupBox
    }
    // EaComponents.SideBarColumn
}
