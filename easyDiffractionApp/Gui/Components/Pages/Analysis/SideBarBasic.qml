// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick

import EasyApp.Gui.Style 1.0 as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        collapsible: false
        last: true

        Loader { source: 'SideBarBasic/Experiments.qml' }
    }

    EaElements.GroupBox {
        //title: qsTr("Parameters")
        collapsible: false
        last: true

        Loader { source: 'SideBarBasic/Fittables.qml' }
    }

    EaElements.GroupBox {
        //title: qsTr("Fitting")
        collapsible: false

        Loader { source: 'SideBarBasic/Fitting.qml' }
    }

}
