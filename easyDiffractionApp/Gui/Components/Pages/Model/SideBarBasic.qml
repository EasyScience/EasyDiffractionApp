// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: Globals.Proxies.modelGroupTitle(qsTr("Models"))
        icon: 'layer-group'
        collapsed: false
        last: !Globals.Proxies.main.model.defined

        Loader { source: 'SideBarBasic/Models.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Space group")
        icon: 'satellite'
        visible: Globals.Proxies.main.model.defined

        Loader { source: 'SideBarBasic/SpaceGroup.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Cell")
        icon: 'cube'
        visible: Globals.Proxies.main.model.defined

        Loader { source: 'SideBarBasic/Cell.qml' }
    }

    EaElements.GroupBox {
        title: Globals.Proxies.modelLoopTitle(qsTr('Atom site'), '_atom_site')
        icon: 'atom'
        visible: Globals.Proxies.main.model.defined

        Loader { source: 'SideBarBasic/AtomSite.qml' }
    }

    EaElements.GroupBox {
        title: Globals.Proxies.modelLoopTitle(qsTr('Atomic displacement'), '_atom_site')
        icon: 'arrows-alt'
        visible: Globals.Proxies.main.model.defined

        Loader { source: 'SideBarBasic/AtomSiteAdp.qml' }
    }

}
