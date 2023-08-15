// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


Column {
    spacing: EaStyle.Sizes.fontPixelSize

    // Name field + format selector
    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        // Name field
        EaElements.TextField {
            id: nameField
            width: saveButton.width - formatField.width - parent.spacing
            topInset: nameLabel.height
            topPadding: topInset + padding
            horizontalAlignment: TextInput.AlignLeft
            placeholderText: qsTr("Enter report file name here")
            //Component.onCompleted: text = 'report'
            EaElements.Label {
                id: nameLabel
                text: qsTr("Name")
            }
        }

        // Format selector
        EaElements.ComboBox {
            id: formatField
            topInset: formatLabel.height
            topPadding: topInset + padding
            //bottomInset: 0
            width: EaStyle.Sizes.fontPixelSize * 10
            textRole: "text"
            valueRole: "value"
            model: [
                { value: 'html', text: qsTr("Interactive HTML") },
                { value: 'pdf', text: qsTr("Static PDF") }
            ]
            EaElements.Label {
                id: formatLabel
                text: qsTr("Format")
            }
        }
    }

    // Location field
    EaElements.TextField {
        id: reportLocationField
        width: saveButton.width
        topInset: locationLabel.height
        topPadding: topInset + padding
        rightPadding: chooseButton.width
        horizontalAlignment: TextInput.AlignLeft
        placeholderText: qsTr("Enter report location here")
        EaElements.Label {
            id: locationLabel
            text: qsTr("Location")
        }
        EaElements.ToolButton {
            id: chooseButton
            anchors.right: parent.right
            topPadding: parent.topPadding
            showBackground: false
            fontIcon: "folder-open"
            ToolTip.text: qsTr("Choose report parent directory")
            onClicked: reportParentDirDialog.open()
        }
    }

    // Save button
    EaElements.SideBarButton {
        id: saveButton
        wide: true
        fontIcon: 'download'
        text: qsTr('Save')
        onClicked: {
            console.debug(`Clicking '${text}' button: ${this}`)
            if (formatField.currentValue === 'html') {
                Globals.Proxies.main.summary.saveHtmlReport(reportLocationField.text)
            } else if (formatField.currentValue === 'pdf') {
                //Globals.Vars.reportWebView.printToPdf(reportLocationField.text)
            }
        }
    }

    // Save directory dialog
    FolderDialog {
        id: reportParentDirDialog
        title: qsTr("Choose report parent directory")
        //folder: Globals.Proxies.main.project.currentProjectPath
        //Component.onCompleted: selectedFolder = projectPathDict().parent
    }

}
