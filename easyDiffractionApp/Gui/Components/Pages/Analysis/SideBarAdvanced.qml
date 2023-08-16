// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Parameter names")
        icon: "paint-brush"
        collapsed: false

        Loader { source: 'SideBarAdvanced/ParamNames.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Calculation engine")
        icon: 'calculator'

        Loader { source: 'SideBarAdvanced/Calculator.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Minimization engine")
        icon: 'level-down-alt'

        Loader { source: 'SideBarAdvanced/Minimizer.qml' }
    }
}
