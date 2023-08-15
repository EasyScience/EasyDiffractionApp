// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals
import Gui.Components as Components


EaComponents.ContentPage {
    defaultInfo: Globals.Proxies.main.experiment.defined ?
                     "" :
                     qsTr("No experiments defined")

    mainView: EaComponents.MainContent {
        tabs: [
            EaElements.TabButton { text: qsTr("Chart view") }
        ]

        items: [
            Loader {
                source: `MainContent/${EaGlobals.Vars.currentLib1d}1dTab.qml`
                onStatusChanged: if (status === Loader.Ready) console.debug(`${source} loaded`)
            }
        ]
    }

    sideBar: EaComponents.SideBar {
        tabs: [
            EaElements.TabButton { text: qsTr("Basic controls") },
            EaElements.TabButton { text: qsTr("Advanced controls"); enabled: false },
            EaElements.TabButton { text: qsTr("Text mode"); enabled: Globals.Proxies.main.experiment.defined }
        ]

        items: [
            Loader { source: 'SideBarBasic.qml' },
            Loader { source: 'SideBarAdvanced.qml' },
            Loader { source: 'SideBarText.qml' }
        ]

        continueButton.enabled: Globals.Proxies.main.experiment.defined

        continueButton.onClicked: {
            console.debug(`Clicking '${continueButton.text}' button: ${this}`)
            Globals.Vars.analysisPageEnabled = true
            Globals.Refs.app.appbar.analysisButton.toggle()
        }

        Component.onCompleted: Globals.Refs.app.experimentPage.continueButton = continueButton
    }

    Component.onCompleted: console.debug(`Experiment page loaded: ${this}`)
    Component.onDestruction: console.debug(`Experiment page destroyed: ${this}`)
}
