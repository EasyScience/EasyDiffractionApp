// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    readonly property int commonSpacing: EaStyle.Sizes.fontPixelSize * 1.5

    color: EaStyle.Colors.mainContentBackground

    Column {

        anchors.left: parent.left
        anchors.leftMargin: commonSpacing
        anchors.top: parent.top
        anchors.topMargin: commonSpacing * 0.5
        spacing: commonSpacing

        EaElements.TextInput {
            font.family: EaStyle.Fonts.secondFontFamily
            font.pixelSize: EaStyle.Sizes.fontPixelSize * 3
            font.weight: Font.ExtraLight
            text: ExGlobals.Constants.proxy.project.projectInfoAsJson.name
            onEditingFinished: ExGlobals.Constants.proxy.project.editProjectInfo("name", text)
        }

        Grid {
            columns: 2
            rowSpacing: 0
            columnSpacing: commonSpacing

            EaElements.Label {
                font.bold: true
                text: qsTr("Short description:")
            }
            EaElements.TextInput {
                text: ExGlobals.Constants.proxy.project.projectInfoAsJson.short_description
                onEditingFinished: ExGlobals.Constants.proxy.project.editProjectInfo("short_description", text)
            }

            EaElements.Label {
                visible: ExGlobals.Constants.proxy.project.projectCreated
                font.bold: true
                text: qsTr("Location:")
            }
            EaElements.Label {
                visible: ExGlobals.Constants.proxy.project.projectCreated
                text: ExGlobals.Constants.proxy.project.currentProjectPath
            }

            EaElements.Label {
                font.bold: true
                text: qsTr("Phases:")
            }
            EaElements.Label {
                text: ExGlobals.Constants.proxy.project.projectInfoAsJson.samples
                //onEditingFinished: ExGlobals.Constants.proxy.project.editProjectInfo("samples", text)
            }

            EaElements.Label {
                font.bold: true
                text: qsTr("Experiments:")
            }
            EaElements.Label {
                text: ExGlobals.Constants.proxy.project.projectInfoAsJson.experiments
                //onEditingFinished: ExGlobals.Constants.proxy.project.editProjectInfo("experiments", text)
            }

            /*
            EaElements.Label {
                font.bold: true
                text: qsTr("Calculations:")
            }
            EaElements.TextInput {
                text: ExGlobals.Constants.proxy.project.projectInfoAsJson.calculations
                onEditingFinished: ExGlobals.Constants.proxy.project.editProjectInfo("calculations", text)
            }
            */

            EaElements.Label {
                font.bold: true
                text: qsTr("Modified:")
            }
            EaElements.Label {
                text: ExGlobals.Constants.proxy.project.projectInfoAsJson.modified
            }
        }

    }

}
