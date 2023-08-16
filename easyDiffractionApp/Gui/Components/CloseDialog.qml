// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Elements as EaElements
import Gui.Globals as Globals


EaElements.Dialog {
    visible: false

    title: qsTr("Save Changes")

    EaElements.Label {
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("The project has not been saved. Do you want to exit?")
    }

    footer: EaElements.DialogButtonBox {
        EaElements.Button {
            text: qsTr("Save and exit")
            onClicked: {
                Globals.Proxies.main.project.save()
                applicationWindow.quit()
            }
        }

        EaElements.Button {
            text: qsTr("Exit without saving")
            onClicked: applicationWindow.quit()
        }
    }
}




