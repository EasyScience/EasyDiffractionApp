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

        property int experimentCurrentIndex: Globals.Proxies.main.experiment.currentIndex

        defaultInfoText: qsTr("No experiments defined")

        maxRowCountShow: 5
        onExperimentCurrentIndexChanged: currentIndex = Globals.Proxies.main.experiment.currentIndex

        // Table model
        model: Globals.Proxies.main.experiment.dataBlocksNoMeas
        /*
        onModelChanged: {
            if (model) {
                Globals.Proxies.main.experiment.currentIndex = Globals.Proxies.main.experiment.dataBlocksNoMeas.length - 1
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
            mouseArea.onPressed: Globals.Proxies.main.experiment.currentIndex = tableView.currentIndex

            EaComponents.TableViewLabel {
                enabled: false
                text: index + 1
            }

            EaComponents.TableViewButton {
                fontIcon: "microscope"
                ToolTip.text: qsTr("Measured pattern color")
                backgroundColor: "transparent"
                borderColor: "transparent"
                iconColor: EaStyle.Colors.chartForegroundsExtra[2]
            }

            EaComponents.TableViewParameter {
                selected: index === Globals.Proxies.main.experiment.currentIndex
                text: tableView.model[index].name.value
            }

            EaComponents.TableViewButton {
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this dataset")
                onClicked: Globals.Proxies.main.experiment.removeExperiment(index)
            }

        }
        // Table rows

    }
    // Table

    // Control buttons below table
    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            //enabled: !Globals.Proxies.main.experiment.defined
            fontIcon: "upload"
            text: qsTr("Load experiment(s) from file(s)")
            onClicked: {
                console.debug(`Clicking '${text}' button: ${this}`)
                if (Globals.Vars.isTestMode) {
                    console.debug('*** Loading experiment from resources (test mode) ***')
                    const fpaths = [':/Examples/Co2SiO4-Mult-Phases/experiments/d20.cif']
                    Globals.Proxies.main.experiment.loadExperimentsFromResources(fpaths)
                } else {
                    openCifFileDialog.open()
                }
            }
            Component.onCompleted: Globals.Refs.app.experimentPage.importDataFromLocalDriveButton = this
        }

        EaElements.SideBarButton {
            //enabled: !Globals.Proxies.main.experiment.defined
            enabled: false
            fontIcon: "plus-circle"
            text: qsTr("Define experiment manually")
            onClicked: {
                console.debug(`Clicking '${text}' button: ${this}`)
                console.debug('*** Adding default experiment ***')
                Globals.Proxies.main.experiment.addDefaultExperiment()
            }
            Component.onCompleted: Globals.Refs.app.experimentPage.addDefaultExperimentDataButton = this
        }
    }
    // Control buttons below table

    // Misc

    FileDialog{
        id: openCifFileDialog
        fileMode: FileDialog.OpenFiles
        nameFilters: [ "CIF files (*.cif)", "ASCII data files (*.xye)"]
        onAccepted: {
            console.debug('*** Loading experiment(s) from file(s) ***')
            Globals.Proxies.main.experiment.loadExperimentsFromFiles(selectedFiles)
        }
    }

}
