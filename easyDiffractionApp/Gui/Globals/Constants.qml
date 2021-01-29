pragma Singleton

import QtQuick 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import Gui.Logic 1.0 as ExLogic

QtObject {
    readonly property var proxy: typeof _pyQmlProxyObj !== "undefined" && _pyQmlProxyObj !== null ?
                                     _pyQmlProxyObj :
                                     new ExLogic.PyQmlProxy.PyQmlProxy()

    readonly property string appName: EaGlobals.Variables.projectConfig.tool.poetry.name
    readonly property string appPrefixName: "easy"
    readonly property string appSuffixName: appName.replace(appPrefixName, "")
    readonly property string appVersion: EaGlobals.Variables.projectConfig.tool.poetry.version
    readonly property string appDate: new Date().toISOString().slice(0,10) // TODO: Get from phython logic formatted as "9 Apr 2020"
    readonly property string appLogo: Qt.resolvedUrl("../Resources/Logo/App.svg")
    readonly property string appUrl: "https://github.com/easyScience/easyDiffractionApp"
    readonly property string essLogo: Qt.resolvedUrl("../Resources/Logo/ESSlogo.png")
    readonly property string eulaUrl: "https://raw.githubusercontent.com/easyScience/easyDiffractionApp/master/LICENSE.md"
    readonly property string oslUrl: "https://raw.githubusercontent.com/easyScience/easyDiffractionApp/master/externalLicences.md"
    readonly property string description: "easyDiffraction is a scientific software for\n modelling and analysis of neutron diffraction data.\n\n" +
    "easyDiffraction is build by ESS DMSC in\n Copenhagen, Denmark."
    readonly property int sampleScale: 100
}
