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
    readonly property string branchName: typeof EaGlobals.Variables.projectConfig.ci.app.info !== 'undefined'
                                      ? EaGlobals.Variables.projectConfig.ci.app.info.branch_name
                                      : 'master'
    readonly property string appVersion: EaGlobals.Variables.projectConfig.tool.poetry.version
                                         + (typeof EaGlobals.Variables.projectConfig.ci.app.info !== 'undefined' && branchName !== 'master'
                                            ? `.${EaGlobals.Variables.projectConfig.ci.app.info.commit_sha_short} [${EaGlobals.Variables.projectConfig.ci.app.info.branch_name}]`
                                            : '' )
    readonly property string appDate: typeof EaGlobals.Variables.projectConfig.ci.app.info !== 'undefined'
                                      ? EaGlobals.Variables.projectConfig.ci.app.info.date
                                      : '01.01.2001'
    readonly property string appLogo: Qt.resolvedUrl("../Resources/Logo/App.svg")
    readonly property string appUrl: "https://github.com/easyScience/easyDiffractionApp"
    readonly property string essLogo: Qt.resolvedUrl("../Resources/Logo/ESSlogo.png")
    readonly property string eulaUrl: `https://raw.githubusercontent.com/easyScience/easyDiffractionApp/${branchName}/LICENSE.md`
    readonly property string oslUrl: `https://raw.githubusercontent.com/easyScience/easyDiffractionApp/${branchName}/DEPENDENCIES.md`
    readonly property string description: "easyDiffraction is a scientific software for\n modelling and analysis of neutron diffraction data.\n\n" +
    "easyDiffraction is build by ESS DMSC in\n Copenhagen, Denmark."
    readonly property int sampleScale: 100
}
