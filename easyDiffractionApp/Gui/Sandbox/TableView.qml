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


Column {
    height: childrenRect.height
    //width: 400
    spacing: 1

    //////////////////////
    // Empty regular table
    EaComponents.TableView {
        defaultInfoText: qsTr("No recent projects found: regular table")
        model: []
        header: EaComponents.TableViewHeader {
            visible: false
            height: 0
            EaComponents.TableViewLabel { width: EaStyle.Sizes.fontPixelSize * 2.5 }
            EaComponents.TableViewLabel { flexibleWidth: true }
        }
        delegate: EaComponents.TableViewDelegate {
            height: 1.5 * EaStyle.Sizes.tableRowHeight
            EaComponents.TableViewLabel {}
            EaComponents.TableViewTwoRowsAdvancedLabel {}
        }
    }
    // Empty regular table
    //////////////////////

    ///////////////////
    // Empty tall table
    EaComponents.TableView {
        showHeader: false
        tallRows: true
        maxRowCountShow: 3
        defaultInfoText: qsTr("No recent projects found: tall table")
        model: []
        header: EaComponents.TableViewHeader {
            EaComponents.TableViewLabel { width: EaStyle.Sizes.fontPixelSize * 2.5 }
            EaComponents.TableViewLabel { flexibleWidth: true }
        }
        delegate: EaComponents.TableViewDelegate {
            height: 1.5 * EaStyle.Sizes.tableRowHeight
            EaComponents.TableViewLabel {}
            EaComponents.TableViewTwoRowsAdvancedLabel {}
        }
    }
    // Empty tall table
    ///////////////////

    ////////////////
    // Regular table
    EaComponents.TableView {
        id: tableView

        maxRowCountShow: 3
        model: [
            { name: 'Co2SiO4' },
            { name: 'CoO' },
            { name: 'O2' },
            { name: 'qwe' }
        ]

        defaultInfoText: qsTr("No models defined")

        // Header row
        header: EaComponents.TableViewHeader {
            //visible: false
            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 3.0
            }
            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.tableRowHeight
            }
            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("label")
            }
            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.tableRowHeight
            }
        }
        // Header row

        // Table rows
        delegate: EaComponents.TableViewDelegate {
            //mouseArea.onPressed: {}

            EaComponents.TableViewAdvancedLabel {
                text: index + 1
                checkable: true
                checked: index === parent.parent.ListView.view.currentIndex
                color: checked ?
                           EaStyle.Colors.themeForegroundHovered :
                           EaStyle.Colors.themeForegroundMinor
                ButtonGroup.group: regularTableButtonGroup
            }
            EaComponents.TableViewButton {
                fontIcon: "layer-group"
                ToolTip.text: qsTr("Calculated pattern color")
                backgroundColor: "transparent"
                borderColor: "transparent"
                iconColor: EaStyle.Colors.chartForegrounds[0]
            }
            EaComponents.TableViewParameter {
                text: tableView.model[index].name.value
            }
            EaComponents.TableViewButton {
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this model")
                //onPressed: {}
            }
        }
        // Table rows

        ButtonGroup { id: regularTableButtonGroup }
    }
    // Regular table
    ////////////////




    /////////////
    // Tall table
    EaComponents.TableView {
        id: tallTable

        showHeader: false
        tallRows: true
        maxRowCountShow: 3

        defaultInfoText: qsTr("No recent projects found")

        // Table model
        model: [
            "/Users/as/Development/GitHub/easyScience/EasyExampleApp/examples/Co2SiO4/project.cif",
            "/Users/as/Development/GitHub/easyScience/EasyExampleApp/examples/1-model_1-experiments/project.cif",
            "/Users/as/Development/GitHub/easyScience/EasyExampleApp/examples/2-models_2-experiments/project.cif",
            "/Users/as/Development/GitHub/easyScience/EasyExampleApp/examples/Co2SiO4-Mult/project.cif",
            "/Users/as/Development/GitHub/easyScience/EasyExampleApp/examples/2-models_2-experiments/project.cif"
        ]
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
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("file")
            }
        }
        // Header row

        // Table rows
        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                text: index + 1
                color: EaStyle.Colors.themeForegroundMinor
            }

            EaComponents.TableViewTwoRowsAdvancedLabel {
                fontIcon: 'layer-group'
                text: projectDirName(tallTable.model[index])
                minorText: tallTable.model[index]
                //ToolTip.text: tallTable.model[index]
                ButtonGroup.group: tallTableButtonGroup
                onClicked: {
                    const filePath = tallTable.model[index]
                    const fileUrl = Qt.resolvedUrl(filePath)
                    console.info(fileUrl)
                    checked = true
                }
            }
        }
        // Table rows

        ButtonGroup { id: tallTableButtonGroup }
    }
    // Tall table
    /////////////



    // Logic

    function baseFileName(filePath) {
        const fileName = filePath.split('\\').pop().split('/').pop()
        const baseFileName = fileName.split('.').shift()
        return baseFileName
    }

    function projectDirName(filePath) {
        let dirName = filePath.split('\\').slice(-2).reverse().pop()
        dirName = dirName.split('/').slice(-2).reverse().pop()
        return dirName
    }

}


