// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls

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

    defaultInfoText: qsTr("No examples available")

    model: Globals.Proxies.main.project.examples

    // header
    header: EaComponents.TableViewHeader {
        EaComponents.TableViewLabel {
            enabled: false
            width: EaStyle.Sizes.fontPixelSize * 2.5
        }

        EaComponents.TableViewLabel {
            flexibleWidth: true
            horizontalAlignment: Text.AlignLeft
            text: qsTr("name / description")
        }
    }
    // header

    // delegate
    delegate: EaComponents.TableViewDelegate {
        mouseArea.onPressed: {
            Globals.Proxies.disableAllPagesExceptProject()
            Globals.Proxies.resetAll()

            Globals.Vars.modelPageEnabled = true
            Globals.Vars.experimentPageEnabled = true

            const filePath = tableView.model[index].path
            Globals.Proxies.main.project.loadExampleFromSoure(filePath)

            Globals.Vars.analysisPageEnabled = true
            Globals.Vars.summaryPageEnabled = true
        }

        EaComponents.TableViewLabel {
            text: index + 1
            color: EaStyle.Colors.themeForegroundMinor
        }

        EaComponents.TableViewTwoRowsAdvancedLabel {
            fontIcon: 'archive'
            text: tableView.model[index].name
            minorText: tableView.model[index].description
            ToolTip.text: tableView.model[index].description
        }
    }
    // delegate

}
