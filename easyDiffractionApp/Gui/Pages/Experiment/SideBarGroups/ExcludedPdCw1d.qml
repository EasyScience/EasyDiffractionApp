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

    // Column {
    //     EaElements.Label {
    //         enabled: false
    //         text: qsTr("Type")
    //     }

    //     EaElements.ComboBox {
    //         width: EaStyle.Sizes.sideBarContentWidth
    //         model: ["Point background"]
    //     }
    // }

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("Regions")
        }

        EaComponents.TableView {

            defaultInfoText: qsTr("No Excluded Regions Added")

            // Table model

            model: XmlListModel {
                xml: ExGlobals.Constants.proxy.background.asXml
                // xml: ExGlobals.Constants.proxy.experiment.regionsAsXml
                query: "/data/data"

                XmlRole { name: "x"; query: "x/value/number()" }
                XmlRole { name: "y"; query: "y/value/number()" }

                XmlRole { name: "pointName"; query: "name/string()" }

                XmlRole { name: "xId"; query: "x/__id/string()" }
                XmlRole { name: "yId"; query: "y/__id/string()" }
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
                    headerText: "From (deg)"
                    text: EaLogic.Utils.toFixed(model.x)
                    onEditingFinished: editParameterValue(model.xId, text)
                }

                EaComponents.TableViewTextInput {
                    id: yLabel
                    horizontalAlignment: Text.AlignRight
                    width: xLabel.width
                    headerText: "To (deg)"
                    text: EaLogic.Utils.toFixed(model.y)
                    onEditingFinished: editParameterValue(model.yId, text)
                }

                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 7
                }

                EaComponents.TableViewButton {
                    headerText: "Del."
                    fontIcon: "minus-circle"
                    ToolTip.text: qsTr("Remove this point")
                    onClicked: ExGlobals.Constants.proxy.background.removePoint(model.pointName)
                }

            }
        }
    }

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            fontIcon: "plus-circle"
            text: qsTr("Append new region")
            onClicked: ExGlobals.Constants.proxy.background.addDefaultPoint()
        }

        EaElements.SideBarButton {
            fontIcon: "undo-alt"
            text: qsTr("Reset all regions")
            onClicked: ExGlobals.Constants.proxy.background.setDefaultPoints()
        }
    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }
}


