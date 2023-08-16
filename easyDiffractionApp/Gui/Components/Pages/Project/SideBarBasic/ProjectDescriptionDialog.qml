// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.ProjectDescriptionDialog {
    visible: EaGlobals.Vars.showProjectDescriptionDialog
    onClosed: EaGlobals.Vars.showProjectDescriptionDialog = false

    onAccepted: {
        Globals.Proxies.main.project.setName(projectName)
        Globals.Proxies.main.project.setMainParam('_description', 'value', projectDescription ? projectDescription : '.')
        Globals.Proxies.main.project.location = projectLocation
        Globals.Proxies.main.project.create()
    }

    Component.onCompleted: {
        projectName = Globals.Proxies.main.project.dataBlock.name.value
        projectDescription = Globals.Proxies.main.project.dataBlock.params['_description'].value
        projectLocation = Globals.Proxies.main.project.location
    }
}
