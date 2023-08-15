// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaElements.GroupColumn {

    // Table
    EaComponents.TableView {
        id: tableView

        maxRowCountShow: 6
        defaultInfoText: qsTr("No atoms defined")

        // Table model
        // We only use the length of the model object defined in backend logic and
        // directly access that model in every row using the TableView index property.
        model: {
            if (typeof Globals.Proxies.main.model.dataBlocks[Globals.Proxies.main.model.currentIndex] === 'undefined') {
                return 0
            }
            return Globals.Proxies.main.model.dataBlocks[Globals.Proxies.main.model.currentIndex].loops._atom_site.length
        }
        onModelChanged: {
            currentIndex = model - 1
            positionViewAtEnd()
        }
        // Table model

        // Header row
        header: EaComponents.TableViewHeader {

            EaComponents.TableViewLabel {
                enabled: false
                width: EaStyle.Sizes.fontPixelSize * 3.0
                //text: qsTr("no.")
            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_label', 0).title ?? ''  // NEED FIX
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.tableRowHeight
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 3.0
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_type_symbol', 0).title ?? ''  // NEED FIX
            }

            EaComponents.TableViewLabel {
                id: fractXLabel
                width: EaStyle.Sizes.fontPixelSize * 4.8
                horizontalAlignment: Text.AlignHCenter
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_fract_x', 0).title ?? ''  // NEED FIX
            }

            EaComponents.TableViewLabel {
                width: fractXLabel.width
                horizontalAlignment: Text.AlignHCenter
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_fract_y', 0).title ?? ''  // NEED FIX
            }

            EaComponents.TableViewLabel {
                width: fractXLabel.width
                horizontalAlignment: Text.AlignHCenter
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_fract_z', 0).title ?? ''  // NEED FIX
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 3.0
                horizontalAlignment: Text.AlignHCenter
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("WP")
            }

            EaComponents.TableViewLabel {
                width: fractXLabel.width
                horizontalAlignment: Text.AlignHCenter
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_occupancy', 0).title ?? ''  // NEED FIX
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.tableRowHeight
                //text: qsTr("del.")
            }

        }
        // Header row

        // Table rows
        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                text: index + 1
                color: EaStyle.Colors.themeForegroundMinor
            }

            EaComponents.TableViewParameter {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_label', index)
                onEditingFinished: Globals.Proxies.setModelLoopParamWithFullUpdate(parameter, 'value', text)
            }

            EaComponents.TableViewButton {
                fontIcon: "atom"
                backgroundColor: "transparent"
                borderColor: "transparent"
                iconColor: Globals.Proxies.main.model.atomData(
                               Globals.Proxies.modelLoopParam('_atom_site', '_type_symbol', index).value,
                               'color')
            }

            EaComponents.TableViewParameter {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_type_symbol', index)
                onEditingFinished: Globals.Proxies.setModelLoopParamWithFullUpdate(parameter, 'value', text)
                warned: !Globals.Proxies.main.model.isotopesNames.includes(text)
            }

            EaComponents.TableViewParameter {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_fract_x', index)
                onEditingFinished: Globals.Proxies.setModelLoopParamWithFullUpdate(parameter, 'value', Number(text))
                fitCheckBox.onToggled: Globals.Proxies.setModelLoopParam(parameter, 'fit', fitCheckBox.checked)
            }

            EaComponents.TableViewParameter {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_fract_y', index)
                onEditingFinished: Globals.Proxies.setModelLoopParamWithFullUpdate(parameter, 'value', Number(text))
                fitCheckBox.onToggled: Globals.Proxies.setModelLoopParam(parameter, 'fit', fitCheckBox.checked)
            }

            EaComponents.TableViewParameter {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_fract_z', index)
                onEditingFinished: Globals.Proxies.setModelLoopParamWithFullUpdate(parameter, 'value', Number(text))
                fitCheckBox.onToggled: Globals.Proxies.setModelLoopParam(parameter, 'fit', fitCheckBox.checked)
            }

            EaComponents.TableViewParameter {
                enabled: false
                text: Globals.Proxies.modelLoopParam('_atom_site', '_multiplicity', index).value +
                      Globals.Proxies.modelLoopParam('_atom_site', '_Wyckoff_symbol', index).value
            }

            EaComponents.TableViewParameter {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_occupancy', index)
                onEditingFinished: Globals.Proxies.setModelLoopParam(parameter, 'value', Number(text))
                fitCheckBox.onToggled: Globals.Proxies.setModelLoopParam(parameter, 'fit', fitCheckBox.checked)
            }

            EaComponents.TableViewButton {
                enabled: tableView !== null && tableView.model > 1
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this atom")
                onClicked: Globals.Proxies.removeModelLoopRow('_atom_site', index)
            }

        }
        // Table rows

    }
    // Table

    // Control buttons below table
    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            fontIcon: "plus-circle"
            text: qsTr("Append new atom")
            onClicked: {
                console.debug(`Clicking '${text}' button: ${this}`)
                console.debug('*** Appending new atom ***')
                Globals.Proxies.appendModelLoopRow('_atom_site')
            }
        }

        EaElements.SideBarButton {
            fontIcon: "clone"
            text: qsTr("Duplicate selected atom")
            onClicked: {
                console.debug(`Clicking '${text}' button: ${this}`)
                console.debug('*** Duplicating selected atom ***')
                Globals.Proxies.duplicateModelLoopRow('_atom_site', tableView.currentIndex)
            }
        }
    }
    // Control buttons below table

}
