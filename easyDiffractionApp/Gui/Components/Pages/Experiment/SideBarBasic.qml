// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: Globals.Proxies.experimentGroupTitle(qsTr("Experiments"))
        icon: 'microscope'
        collapsed: false
        last: !Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/Experiments.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Diffraction radiation")
        icon: 'radiation'
        visible: Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/DiffrnRadiation.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Measured range")
        icon: 'arrows-alt-h'
        visible: Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/PdMeas2Theta.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Instrument resolution")
        icon: 'grip-lines-vertical'
        visible: Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/PdInstrResolution.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Peak asymmetry")
        icon: 'balance-scale-left'
        visible: Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/PdInstrReflexAsymmetry.qml' }
    }

    EaElements.GroupBox {
        title: Globals.Proxies.experimentLoopTitle(qsTr('Background'), '_pd_background')
        icon: 'wave-square'
        visible: Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/PdBackground.qml' }
    }

    EaElements.GroupBox {
        title: Globals.Proxies.experimentLoopTitle(qsTr('Associated phases'), '_phase')
        icon: 'layer-group'
        visible: Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/Phase.qml' }
    }

}
