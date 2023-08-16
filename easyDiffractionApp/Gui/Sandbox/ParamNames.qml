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

//import Gui.Globals as Globals


EaComponents.TableView {
    id: tableView

    property var param: {
        "blockType": "model",
        "blockIcon": "layer-group",
        "blockIndex": 0,
        "blockName": "co2sio4",
        "groupIcon": "atom",
        "loopName": "_atom_site",
        "prettyLoopName": "atom",
        "rowIndex": 2,
        "rowName": "Si",
        "prettyRowName": "",
        "icon": "map-marker-alt",
        "name": "_fract_x",
        "prettyName": "fract x",
        "title": "x" }

    showHeader: false
    tallRows: true
    maxRowCountShow: model.length

    // Table model
    model: [
        { value: EaGlobals.Vars.ShortestWithIconsAndPrettyLabels,
            text: qsTr('Shortest iconified name with pretty labels') },
        { value: EaGlobals.Vars.ReducedWithIconsAndPrettyLabels,
            text: qsTr('Shorter iconified name with pretty labels') },
        { value: EaGlobals.Vars.FullWithIconsAndPrettyLabels,
            text: qsTr('Full iconified name with pretty labels') },
        { value: EaGlobals.Vars.FullWithPrettyLabels,
            text: qsTr('Full plain text name with pretty labels') },
        { value: EaGlobals.Vars.FullWithLabels,
            text: qsTr('Full plain text name with labels') },
        { value: EaGlobals.Vars.FullWithIndices,
            text: qsTr('Full plain text name with indices') }
    ]
    onModelChanged: {
        if (model.length > 0) {
            //settings.setValue('recentProjects', JSON.stringify(Globals.Proxies.main.project.recent))
        }
    }
    //Component.onCompleted: Globals.Proxies.main.project.recent = JSON.parse(settings.value('recentProjects', '[]'))
    // Table model

    // Header row
    header: EaComponents.TableViewHeader {

        EaComponents.TableViewLabel {
            enabled: false
            width: EaStyle.Sizes.fontPixelSize * 2.5
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
        mouseArea.onPressed: EaGlobals.Vars.paramNameFormat = currentIndex

        EaElements.RadioButton {
            checked: index === EaGlobals.Vars.paramNameFormat
            anchors.verticalCenter: parent.verticalCenter
            Component.onCompleted: console.error(`${index} - ${EaGlobals.Vars.paramNameFormat}`)
        }

        EaComponents.TableViewTwoRowsAdvancedLabel {
            text: tableView.model[index].text
            minorText: EaGlobals.Funcs.paramName(param, tableView.model[index].value)
        }
    }
    // Table rows



    // Persistent settings
    Settings {
        //id: settings
        //location: EaGlobals.Vars.settingsFile // Gives WASM error on run
        //category: 'Project.Recent'
    }

    // Logic



}

