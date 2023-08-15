// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
import QtCore

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic


EaComponents.TableView {
    id: tableView

    maxRowCountShow: 9
    defaultInfoText: qsTr("No recent projects found")

    // Table model
    model: [
        "/Users/as/Development/GitHub/easyScience/EasyExampleApp/examples/2-models_2-experiments/project.cif",
        "/Users/as/Development/GitHub/easyScience/EasyExampleApp/examples/2-models_2-experiments/project.cif",
        "/Users/as/Development/GitHub/easyScience/EasyExampleApp/examples/2-models_2-experiments/project.cif",
        "/Users/as/Development/GitHub/easyScience/EasyExampleApp/examples/Co2SiO4/project.cif",
        "/Users/as/Development/GitHub/easyScience/EasyExampleApp/examples/Co2SiO4-Mult/project.cif"
    ]
    // Table model

    // Header row
    header: EaComponents.TableViewHeader {
        visible: false
        height: 0

        EaComponents.TableViewLabel {
            enabled: false
            width: EaStyle.Sizes.fontPixelSize * 2.5
        }

        EaComponents.TableViewLabel {
            flexibleWidth: true
            horizontalAlignment: Text.AlignLeft
            color: EaStyle.Colors.themeForegroundMinor
            text: qsTr("file")
        }

        /*
        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.tableRowHeight
        }
        */

    }
    // Header row

    ButtonGroup { id: buttonGroup }

    // Table rows
    delegate: EaComponents.TableViewDelegate {
        height: 1.5 * EaStyle.Sizes.tableRowHeight

        EaComponents.TableViewLabel {
            text: index + 1
            color: EaStyle.Colors.themeForegroundMinor
        }

        /*
        EaComponents.TableViewAdvancedLabel {
            height: 40
            EaComponents.TableViewAdvancedLabel {
                text: baseFileName(tableView.model[index])
                //ToolTip.text: tableView.model[index]
            }

            EaComponents.TableViewAdvancedLabel {
                text: tableView.model[index]
                //ToolTip.text: tableView.model[index]
            }
        }
        */

        EaComponents.TableViewTwoRowsAdvancedLabel {
            //highlighted: true
            //width: 300
            fontIcon: 'rocket'
            text: baseFileName(tableView.model[index])
            minorText: tableView.model[index]
            //ToolTip.text: tableView.model[index]
            ButtonGroup.group: buttonGroup
            onClicked: {
                const filePath = tableView.model[index]
                const fileUrl = Qt.resolvedUrl(filePath)
                console.info(fileUrl)
                checked = true
            }
        }

    }
    // Table rows

    // Logic

    function baseFileName(filePath) {
        //const filePath = tableView.model[index]
        const fileName = filePath.split('\\').pop().split('/').pop()
        const baseFileName = fileName.split('.').shift()
        return baseFileName
    }

}
