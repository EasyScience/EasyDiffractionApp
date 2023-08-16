// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Elements as EaElements
import Gui.Globals as Globals


EaElements.SplashScreen {

    appNamePrefix: Globals.Configs.appConfig.namePrefixForLogo
    appNameSuffix: Globals.Configs.appConfig.nameSuffixForLogo
    appVersion: qsTr('Version') + ` ${Globals.Configs.appConfig.version} (${Globals.Configs.appConfig.date})`
    logoSource: Globals.Configs.appConfig.icon

    initialGuiCompleted: Globals.Vars.applicationWindowCreated &&
                         Globals.Vars.homePageCreated

    onAnimationFinishedChanged: Globals.Vars.splashScreenAnimoFinished = animationFinished

    Component.onCompleted: console.debug(`Splash screen loaded: ${this}`)
    Component.onDestruction: console.debug(`Splash screen destroyed: ${this}`)

}
