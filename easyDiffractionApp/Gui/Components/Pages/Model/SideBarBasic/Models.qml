// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals


Column {
    spacing: EaStyle.Sizes.fontPixelSize

    // Table
    EaComponents.TableView {
        id: tableView

        property int modelCurrentIndex: Globals.Proxies.main.model.currentIndex

        defaultInfoText: qsTr("No models defined")

        maxRowCountShow: 5
        onModelCurrentIndexChanged: currentIndex = Globals.Proxies.main.model.currentIndex

        // Table model
        model: Globals.Proxies.main.model.dataBlocks
        /*
        onModelChanged: {
            if (model) {
                Globals.Proxies.main.model.currentIndex = Globals.Proxies.main.model.dataBlocks.length - 1
                positionViewAtEnd()
            }
        }
        */
        // Table model

        // Header row
        header: EaComponents.TableViewHeader {

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 3.0
                //text: qsTr("no.")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.tableRowHeight
                //text: qsTr("color")
            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("label")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.tableRowHeight
                //text: qsTr("del.")
            }

        }
        // Header row

        // Table rows
        delegate: EaComponents.TableViewDelegate {
            mouseArea.onPressed: Globals.Proxies.main.model.currentIndex = tableView.currentIndex

            EaComponents.TableViewLabel {
                enabled: false
                text: index + 1
            }

            EaComponents.TableViewButton {
                fontIcon: "layer-group"
                ToolTip.text: qsTr("Calculated pattern color")
                backgroundColor: "transparent"
                borderColor: "transparent"
                iconColor: EaStyle.Colors.models[index]
            }

            EaComponents.TableViewParameter {
                selected: index === Globals.Proxies.main.model.currentIndex
                text: tableView.model[index].name.value
            }

            EaComponents.TableViewButton {
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this model")
                onClicked: Globals.Proxies.main.model.removeModel(index)
            }

        }
        // Table rows

        Component.onCompleted: Globals.Refs.app.modelPage.modelsExplorer = this

    }
    // Table

    // Control buttons below table
    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            fontIcon: "upload"
            text: qsTr("Load model(s) from file(s)")
            onClicked: {
                console.debug(`Clicking '${text}' button: ${this}`)
                if (Globals.Vars.isTestMode) {
                    console.debug('*** Loading model from resources (test mode) ***')
                    const fpaths = [':/Examples/Co2SiO4-Mult-Phases/models/co2sio4.cif',
                                    ':/Examples/Co2SiO4-Mult-Phases/models/coo.cif']
                    Globals.Proxies.main.model.loadModelsFromResources(fpaths)
                } else {
                    openCifFileDialog.open()
                }
            }
            Component.onCompleted: Globals.Refs.app.modelPage.loadNewModelFromFileButton = this
        }

        EaElements.SideBarButton {
            fontIcon: "plus-circle"
            text: qsTr("Define model manually")
            onClicked: {
                console.debug(`Clicking '${text}' button: ${this}`)
                console.debug('*** Adding default model ***')
                Globals.Proxies.main.model.addDefaultModel()
            }
            Component.onCompleted: Globals.Refs.app.modelPage.addNewModelManuallyButton = this
        }
    }
    // Control buttons below table

    // Misc

    FileDialog{
        id: openCifFileDialog
        fileMode: FileDialog.OpenFiles
        nameFilters: [ "CIF files (*.cif)"]
        onAccepted: {
            console.debug('*** Loading model(s) from file(s) ***')
            Globals.Proxies.main.model.loadModelsFromFiles(selectedFiles)
        }
    }

}
