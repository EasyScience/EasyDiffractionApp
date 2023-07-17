// SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals


Column {
    spacing: EaStyle.Sizes.fontPixelSize * 0.5

    Column {

        EaComponents.TableView {

            defaultInfoText: qsTr("No Excluded Regions Added")

            // Table model
            model: XmlListModel {
                xml: ExGlobals.Constants.proxy.experiment.regionsAsXml
                query: "/data/data"

                XmlRole { name: "min"; query: "min/number()" }
                XmlRole { name: "max"; query: "max/number()" }

                XmlRole { name: "pointName"; query: "name/string()" }

            }

            // Table rows

            delegate: EaComponents.TableViewDelegate {

                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 2.5
                    headerText: "No."
                    text: model.index + 1
                }

                EaComponents.TableViewTextInput {
                    id: xLabel
                    horizontalAlignment: Text.AlignRight
                    width: EaStyle.Sizes.fontPixelSize * 11.6
                    headerText: "From (μs)"
                    text: EaLogic.Utils.toFixed(model.min)
                    onEditingFinished: ExGlobals.Constants.proxy.experiment.editExcludedRegion(model.pointName, 0, text)
                }

                EaComponents.TableViewTextInput {
                    id: yLabel
                    horizontalAlignment: Text.AlignRight
                    width: xLabel.width
                    headerText: "To (μs)"
                    text: EaLogic.Utils.toFixed(model.max)
                    onEditingFinished: ExGlobals.Constants.proxy.experiment.editExcludedRegion(model.pointName, 1, text)
                }

                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 7
                }

                EaComponents.TableViewButton {
                    headerText: "Del."
                    fontIcon: "minus-circle"
                    ToolTip.text: qsTr("Remove this point")
                    onClicked: ExGlobals.Constants.proxy.experiment.removeRegion(model.pointName)
                }

            }
        }
    }

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            fontIcon: "plus-circle"
            text: qsTr("Append new region")
            onClicked: ExGlobals.Constants.proxy.experiment.addDefaultRegion()
        }

        EaElements.SideBarButton {
            fontIcon: "undo-alt"
            text: qsTr("Remove all regions")
            onClicked: ExGlobals.Constants.proxy.experiment.removeRegions()
        }
    }
}


