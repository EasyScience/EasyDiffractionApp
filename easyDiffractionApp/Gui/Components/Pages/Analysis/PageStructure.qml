// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls
//import QtQuick.XmlListModel 2.15

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals
import Gui.Components as Components


EaComponents.ContentPage {
    defaultInfo: Globals.Proxies.main.model.defined &&
                 Globals.Proxies.main.experiment.defined ?
                     "" :
                     qsTr("No analysis done")

    mainView: EaComponents.MainContent {
        tabs: [
            EaElements.TabButton {
                text: Globals.Proxies.main.experiment.defined ?
                          qsTr("Fitting") :
                          qsTr("Simulation")
            }
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
            EaElements.TabButton { text: qsTr("Advanced controls"); enabled: Globals.Proxies.main.analysis.defined },
            EaElements.TabButton { text: qsTr("Text mode"); enabled: false }
        ]

        items: [
            Loader { source: 'SideBarBasic.qml' },
            Loader { source: 'SideBarAdvanced.qml' },
            Loader { source: 'SideBarText.qml' }
        ]

        continueButton.enabled: Globals.Proxies.main.summary.isCreated

        continueButton.onClicked: {
            console.debug(`Clicking '${continueButton.text}' button: ${this}`)
            Globals.Vars.summaryPageEnabled = true
            Globals.Refs.app.appbar.summaryButton.toggle()
        }

        Component.onCompleted: Globals.Refs.app.analysisPage.continueButton = continueButton
    }

    Component.onCompleted: console.debug(`Analysis page loaded: ${this}`)
    Component.onDestruction: console.debug(`Analysis page destroyed: ${this}`)
}
