import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

Item {
    readonly property int commonSpacing: EaStyle.Sizes.fontPixelSize * 1.5

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
            text: ExGlobals.Constants.proxy.projectInfoAsJson.name
            onEditingFinished: ExGlobals.Constants.proxy.editProjectInfoByKey("name", text)
        }

        Grid {
            columns: 2
            rowSpacing: 0
            columnSpacing: commonSpacing

            EaElements.Label {
                font.bold: true
                text: qsTr("Keywords:")
            }
            EaElements.TextInput {
                text: ExGlobals.Constants.proxy.projectInfoAsJson.keywords
                onEditingFinished: ExGlobals.Constants.proxy.editProjectInfoByKey("keywords", text)
            }

            EaElements.Label {
                font.bold: true
                text: qsTr("Samples:")
            }
            EaElements.TextInput {
                text: ExGlobals.Constants.proxy.projectInfoAsJson.samples
                onEditingFinished: ExGlobals.Constants.proxy.editProjectInfoByKey("samples", text)
            }

            EaElements.Label {
                font.bold: true
                text: qsTr("Experiments:")
            }
            EaElements.TextInput {
                text: ExGlobals.Constants.proxy.projectInfoAsJson.experiments
                onEditingFinished: ExGlobals.Constants.proxy.editProjectInfoByKey("experiments", text)
            }

            EaElements.Label {
                font.bold: true
                text: qsTr("Calculations:")
            }
            EaElements.TextInput {
                text: ExGlobals.Constants.proxy.projectInfoAsJson.calculations
                onEditingFinished: ExGlobals.Constants.proxy.editProjectInfoByKey("calculations", text)
            }

            EaElements.Label {
                font.bold: true
                text: qsTr("Modified:")
            }
            EaElements.Label {
                text: ExGlobals.Constants.proxy.projectInfoAsJson.modified
            }
        }

    }

}
