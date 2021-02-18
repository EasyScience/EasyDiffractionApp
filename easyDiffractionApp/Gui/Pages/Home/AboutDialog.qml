import QtQuick 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.AboutDialog {
    visible: EaGlobals.Variables.showAppAboutDialog
    onClosed: EaGlobals.Variables.showAppAboutDialog = false

    appIconPath: ExGlobals.Constants.appLogo
    essIconPath: ExGlobals.Constants.essLogo
    eulaUrl: ExGlobals.Constants.eulaUrl
    oslUrl: ExGlobals.Constants.oslUrl
    appUrl: ExGlobals.Constants.appUrl
    appPrefixName: ExGlobals.Constants.appPrefixName
    appSuffixName: ExGlobals.Constants.appSuffixName
    description: ExGlobals.Constants.description
    appVersion: ExGlobals.Constants.appVersion
    appDate: ExGlobals.Constants.appDate
}
