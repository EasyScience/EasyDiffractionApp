// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

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
        EaElements.Label {
            enabled: false
            text: qsTr("Type")
        }

        EaElements.ComboBox {
            width: EaStyle.Sizes.sideBarContentWidth
            model: ["Point background"]
        }
    }

    Column {
        EaElements.Label {
            enabled: false
            text: qsTr("Points")
        }

        EaComponents.TableView {

            defaultInfoText: qsTr("No Background Points Added")

            // Table model

            model: XmlListModel {
                xml: ExGlobals.Constants.proxy.background.asXml
                query: "/root/item"

                XmlRole { name: "x"; query: "x/value/number()" }
                XmlRole { name: "y"; query: "y/value/number()" }

                XmlRole { name: "pointName"; query: "name/string()" }

                XmlRole { name: "xId"; query: "x/key[4]/string()" }
                XmlRole { name: "yId"; query: "y/key[4]/string()" }
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
                    headerText: "TOF"
                    text: EaLogic.Utils.toFixed(model.x, 0)
                    onEditingFinished: editParameterValue(model.xId, text)
                }

                EaComponents.TableViewTextInput {
                    id: yLabel
                    horizontalAlignment: Text.AlignRight
                    width: xLabel.width
                    headerText: "Intensity"
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
            text: qsTr("Append new point")
            onClicked: ExGlobals.Constants.proxy.background.addPoint()
        }

        EaElements.SideBarButton {
            fontIcon: "undo-alt"
            text: qsTr("Reset to default points")
            onClicked: ExGlobals.Constants.proxy.background.setDefaultPoints()
        }
    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }
}


