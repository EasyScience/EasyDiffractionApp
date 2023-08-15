// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


Column {
    spacing: EaStyle.Sizes.fontPixelSize

    EaElements.SideBarButton {
        enabled: Globals.Proxies.main.experiment.defined
        wide: true

        fontIcon: Globals.Proxies.main.fitting.isFittingNow ? 'stop-circle' : 'play-circle'
        text: Globals.Proxies.main.fitting.isFittingNow ? qsTr('Cancel fitting') : qsTr('Start fitting')

        onClicked: {
            console.debug(`Clicking '${text}' button: ${this}`)
            Globals.Proxies.main.fitting.startStop()
        }

        Component.onCompleted: Globals.Refs.app.analysisPage.startFittingButton = this

        Loader { source: "FitStatusDialog.qml" }
    }

}
