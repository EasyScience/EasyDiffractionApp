// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    readonly property var projectConfig: QtObject {
        readonly property var release: QtObject {
            readonly property string appName: 'EasyDiffraction'
            readonly property string version: '0.9.0-pre-alpha.1'
            readonly property string appIssuesUrl: 'https://github.com/EasyScience/EasyExampleApp/issues'
            readonly property string homePageUrl: 'https://easydiffraction.org'
            readonly property string docsUrl: 'https://easydiffraction.org/#docs'
            readonly property string contactUrl: 'https://easydiffraction.org/#contact'
        }
        readonly property var ci: QtObject {
            property var app: QtObject {}
        }
    }

    readonly property var appConfig: QtObject {
        readonly property string name: projectConfig.release.appName
        readonly property string namePrefix: "Easy"
        readonly property string nameSuffix: name.replace(namePrefix, "")
        readonly property string namePrefixForLogo: namePrefix.toLowerCase()
        readonly property string nameSuffixForLogo: nameSuffix.toLowerCase()

        readonly property string icon: iconPath('App.svg')

        readonly property string version: projectConfig.release.version

        readonly property string homePageUrl: projectConfig.release.homePageUrl
        readonly property string issuesUrl: projectConfig.release.appIssuesUrl
        readonly property string docsUrl: projectConfig.release.docsUrl
        readonly property string contactUrl: projectConfig.release.contactUrl

        readonly property bool remote: typeof projectConfig.ci.app.info !== 'undefined'

        readonly property string date: remote ?
                                           projectConfig.ci.app.info.build_date :
                                           new Date().toISOString().slice(0,10)

        readonly property string commit: remote ?
                                             projectConfig.ci.app.info.commit_sha_short :
                                             ''
        readonly property string commitUrl: remote ?
                                               projectConfig.ci.app.info.commit_url :
                                               ''
        readonly property string branch: remote ?
                                             projectConfig.ci.app.info.branch_name :
                                             ''
        readonly property string branchUrl: remote ?
                                                projectConfig.ci.app.info.branch_url :
                                                ''

        readonly property string licenseUrl: githubRawContentUrl(branch, 'LICENSE.md')
        readonly property string dependenciesUrl: githubRawContentUrl(branch, 'DEPENDENCIES.md')

        readonly property string description:
`${name} is a scientific software for modelling and
analysis of diffraction data.

${name} is developed by ESS DMSC`

        readonly property var developerIcons: [
            { url: "https://ess.eu", icon: iconPath('ESS.png'), heightScale: 3.0 }
        ]
        readonly property string developerYearsFrom: "2019"
        readonly property string developerYearsTo: "2023"
    }

    // Logic

    function iconPath(fileName) {
        return Qt.resolvedUrl(`../Resources/Logo/${fileName}`)
    }

    function githubRawContentUrl(branch, file) {
        return `https://raw.githubusercontent.com/easyscience/EasyExampleApp/${branch}/${file}`
    }
}
