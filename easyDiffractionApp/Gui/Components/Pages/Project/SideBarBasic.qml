// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Get started")
        icon: 'rocket'
        collapsed: false

        Loader { source: 'SideBarBasic/GetStarted.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Examples")
        icon: 'database'

        Loader { source: 'SideBarBasic/Examples.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Recent projects")
        icon: 'archive'

        Loader { source: 'SideBarBasic/Recent.qml' }
    }

}
