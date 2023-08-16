// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        //visible: Globals.Proxies.main.experiment.dataBlocksNoMeas.length > 1
        bottomPadding: 0
        collapsible: false
        last: true

        Loader { source: 'SideBarText/Experiments.qml' }
    }

    EaElements.GroupBox {
        collapsible: false

        Loader { source: 'SideBarText/TextView.qml' }
    }

}
