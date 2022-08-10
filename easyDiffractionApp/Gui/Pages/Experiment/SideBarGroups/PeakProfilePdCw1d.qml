// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls
import QtQml.XmlListModel

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
            text: qsTr("Profile function")
        }

        EaElements.ComboBox {
            width: EaStyle.Sizes.sideBarContentWidth
            model: ["Pseudo-Voigt"]
        }
    }

    Row {
        spacing: EaStyle.Sizes.tableColumnSpacing * 2

        Column {
            EaElements.Label {
                enabled: false
                text: qsTr("Gaussian instrumental broadening")
            }

            EaComponents.TableView {
                id: tableViewGauss

                width: EaStyle.Sizes.sideBarContentWidth * 3 / 5 - EaStyle.Sizes.fontPixelSize / 2

                model: XmlListModel {
                    xml: ExGlobals.Constants.proxy.parameters.instrumentParametersAsXml
                    query: `/root/item`

                    XmlListModelRole { name: "u"; query: "resolution_u/value/number()" }
                    XmlListModelRole { name: "v"; query: "resolution_v/value/number()" }
                    XmlListModelRole { name: "w"; query: "resolution_w/value/number()" }

                    XmlListModelRole { name: "uId"; query: "resolution_u/key[4]/string()" }
                    XmlListModelRole { name: "vId"; query: "resolution_v/key[4]/string()" }
                    XmlListModelRole { name: "wId"; query: "resolution_w/key[4]/string()" }
                }

                delegate: EaComponents.TableViewDelegate {

                    EaComponents.TableViewTextInput {
                        width: tableViewGauss.width / contentRowData.length
                        headerText: "U"
                        text: EaLogic.Utils.toFixed(model.u)
                        onEditingFinished: editParameterValue(model.uId, text)
                    }

                    EaComponents.TableViewTextInput {
                        width: tableViewGauss.width / contentRowData.length
                        headerText: "V"
                        text: EaLogic.Utils.toFixed(model.v)
                        onEditingFinished: editParameterValue(model.vId, text)
                    }

                    EaComponents.TableViewTextInput {
                        width: tableViewGauss.width / contentRowData.length
                        headerText: "W"
                        text: EaLogic.Utils.toFixed(model.w)
                        onEditingFinished: editParameterValue(model.wId, text)
                    }
                }
            }
        }

        Column {
            EaElements.Label {
                enabled: false
                text: qsTr("Lorentzian sample broadening")
            }

            EaComponents.TableView {
                id: tableViewLorentz

                width: EaStyle.Sizes.sideBarContentWidth * 2 / 5 - EaStyle.Sizes.fontPixelSize / 2

                model: XmlListModel {
                    xml: ExGlobals.Constants.proxy.parameters.instrumentParametersAsXml
                    query: `/root/item`

                    XmlListModelRole { name: "x"; query: "resolution_x/value/number()" }
                    XmlListModelRole { name: "y"; query: "resolution_y/value/number()" }

                    XmlListModelRole { name: "xId"; query: "resolution_x/key[4]/string()" }
                    XmlListModelRole { name: "yId"; query: "resolution_y/key[4]/string()" }
                }

                delegate: EaComponents.TableViewDelegate {

                    EaComponents.TableViewTextInput {
                        width: tableViewLorentz.width / contentRowData.length
                        headerText: "X"
                        text: EaLogic.Utils.toFixed(model.x)
                        onEditingFinished: editParameterValue(model.xId, text)
                    }

                    EaComponents.TableViewTextInput {
                        width: tableViewLorentz.width / contentRowData.length
                        headerText: "Y"
                        text: EaLogic.Utils.toFixed(model.y)
                        onEditingFinished: editParameterValue(model.yId, text)
                    }
                }
            }
        }
    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }
}

