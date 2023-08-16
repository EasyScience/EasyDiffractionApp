// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls
import QtCore

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals


EaComponents.TableView {
    id: tableView

    showHeader: false
    tallRows: true
    maxRowCountShow: 6

    defaultInfoText: qsTr("No recent projects found")

    // Table model
    model: Globals.Proxies.main.project.recent
    onModelChanged: {
        if (model.length > 0) {
            settings.setValue('recentProjects', JSON.stringify(Globals.Proxies.main.project.recent))
        }
    }
    Component.onCompleted: Globals.Proxies.main.project.recent = JSON.parse(settings.value('recentProjects', '[]'))
    // Table model

    // Header row
    header: EaComponents.TableViewHeader {

        EaComponents.TableViewLabel {
            enabled: false
            width: EaStyle.Sizes.fontPixelSize * 2.5
            //text: qsTr("No.")
        }

        EaComponents.TableViewLabel {
            flexibleWidth: true
            horizontalAlignment: Text.AlignLeft
            text: qsTr("file name / file path")
        }
    }
    // Header row

    // Table rows
    delegate: EaComponents.TableViewDelegate {

        mouseArea.onPressed: {
            Globals.Proxies.disableAllPagesExceptProject()
            Globals.Proxies.resetAll()

            Globals.Vars.modelPageEnabled = true
            Globals.Vars.experimentPageEnabled = true

            const filePath = tableView.model[index]
            //const fileUrl = Qt.resolvedUrl(filePath)
            Globals.Proxies.main.project.loadRecentFromFile(filePath)

            Globals.Vars.analysisPageEnabled = true
            Globals.Vars.summaryPageEnabled = true
        }

        EaComponents.TableViewLabel {
            text: index + 1
            color: EaStyle.Colors.themeForegroundMinor
        }

        EaComponents.TableViewTwoRowsAdvancedLabel {
            fontIcon: 'archive'
            text: projectDirName(tableView.model[index])
            minorText: tableView.model[index]
            ToolTip.text: tableView.model[index]
        }
    }
    // Table rows

    // Persistent settings
    Settings {
        id: settings
        location: EaGlobals.Vars.settingsFile // Gives WASM error on run
        category: 'Project.Recent'
    }

    // Logic

    function baseFileName(filePath) {
        //const filePath = tableView.model[index]
        const fileName = filePath.split('\\').pop().split('/').pop()
        const baseFileName = fileName.split('.').shift()
        return baseFileName
    }

    function projectDirName(filePath) {
        //const filePath = tableView.model[index]
        let dirName = filePath.split('\\').slice(-2).reverse().pop()
        dirName = dirName.split('/').slice(-2).reverse().pop()
        return dirName
    }

}
