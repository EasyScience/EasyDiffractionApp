pragma Singleton

import QtQuick 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import Gui.Logic 1.0 as ExLogic

QtObject {
    readonly property var proxy: _pyQmlProxyObj ?? new ExLogic.PyQmlProxy.PyQmlProxy()

    readonly property string appName: EaGlobals.Variables.projectConfig.tool.poetry.name
    readonly property string appPrefixName: "easy"
    readonly property string appSuffixName: appName.replace(appPrefixName, "")

    readonly property string appLogo: logo('App.svg')
    readonly property string appUrl: EaGlobals.Variables.projectConfig.tool.poetry.homepage

    readonly property string appVersion: EaGlobals.Variables.projectConfig.tool.poetry.version
    readonly property string appDate: EaGlobals.Variables.projectConfig.ci.app.info.build_date ?? '01 Jan 2001'

    readonly property string commit: EaGlobals.Variables.projectConfig.ci.app.info.commit_sha_short ?? ''
    readonly property string commitUrl: EaGlobals.Variables.projectConfig.ci.app.info.commit_url ?? ''

    readonly property string branch: EaGlobals.Variables.projectConfig.ci.app.info.branch_name ?? ''
    readonly property string branchUrl: EaGlobals.Variables.projectConfig.ci.app.info.branch_url ?? ''

    readonly property string eulaUrl: githubRawContent(branch, 'LICENSE.md')
    readonly property string oslUrl: githubRawContent(branch, 'DEPENDENCIES.md')

    readonly property string description:
`${appName} is a scientific software for
modelling and analysis of neutron diffraction data.

${appName} is build by ESS DMSC in
Copenhagen, Denmark.`

    readonly property string essLogo: logo('ESSlogo.png')

    // Logic

    function logo(file) {
        return Qt.resolvedUrl(`../Resources/Logo/${file}`)
    }

    function githubRawContent(branch, file) {
        return `https://raw.githubusercontent.com/easyScience/easyDiffractionApp/${branch}/${file}`
    }
}
