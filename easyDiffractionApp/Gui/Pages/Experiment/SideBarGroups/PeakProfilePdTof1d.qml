// SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13
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
            model: ["Gauss * Exponential"]
        }
    }

    Row {
        spacing: EaStyle.Sizes.tableColumnSpacing * 2

        Column {
            EaElements.Label {
                enabled: false
                text: qsTr("Gaussian broadening")
            }

            EaComponents.TableView {
                id: tableViewGauss

                width: EaStyle.Sizes.sideBarContentWidth * 3 / 6 - EaStyle.Sizes.fontPixelSize / 2

                model: XmlListModel {
                    // xml: ExGlobals.Constants.proxy.parameters.instrumentParametersAsXml
                    // query: `/data`

                    // XmlListModelRole { name: "sigma0"; query: "sigma0/value/number()" }
                    // XmlListModelRole { name: "sigma1"; query: "sigma1/value/number()" }
                    // XmlListModelRole { name: "sigma2"; query: "sigma2/value/number()" }

                    // XmlListModelRole { name: "sigma0_enabled"; query: "sigma0/enabled/string()" }
                    // XmlListModelRole { name: "sigma1_enabled"; query: "sigma1/enabled/string()" }
                    // XmlListModelRole { name: "sigma2_enabled"; query: "sigma2/enabled/string()" }

                    // XmlListModelRole { name: "sigma0Id"; query: "sigma0/__id/string()" }
                    // XmlListModelRole { name: "sigma1Id"; query: "sigma1/__id/string()" }
                    // XmlListModelRole { name: "sigma2Id"; query: "sigma2/__id/string()" }
                }

                delegate: EaComponents.TableViewDelegate {

                    EaComponents.TableViewTextInput {
                        enabled: model.sigma0_enabled === 'True'
                        width: tableViewGauss.width / contentRowData.length
                        headerText: "σ0"
                        text: EaLogic.Utils.toFixed(model.sigma0)
                        onEditingFinished: editParameterValue(model.sigma0Id, text)
                    }

                    EaComponents.TableViewTextInput {
                        enabled: model.sigma1_enabled === 'True'
                        width: tableViewGauss.width / contentRowData.length
                        headerText: "σ1"
                        text: EaLogic.Utils.toFixed(model.sigma1)
                        onEditingFinished: editParameterValue(model.sigma1Id, text)
                    }

                    EaComponents.TableViewTextInput {
                        enabled: model.sigma2_enabled === 'True'
                        width: tableViewGauss.width / contentRowData.length
                        headerText: "σ2"
                        text: EaLogic.Utils.toFixed(model.sigma2)
                        onEditingFinished: editParameterValue(model.sigma2Id, text)
                    }
                }
            }
        }

        Column {
            EaElements.Label {
                enabled: false
                text: qsTr("Lorentzian broadening")
            }

            EaComponents.TableView {
                id: tableViewLorentz

                width: EaStyle.Sizes.sideBarContentWidth * 3 / 6 - EaStyle.Sizes.fontPixelSize / 2

                model: XmlListModel {
                    // xml: ExGlobals.Constants.proxy.parameters.instrumentParametersAsXml
                    // query: `/data`

                    // XmlListModelRole { name: "gamma0"; query: "gamma0/value/number()" }
                    // XmlListModelRole { name: "gamma1"; query: "gamma1/value/number()" }
                    // XmlListModelRole { name: "gamma2"; query: "gamma2/value/number()" }

                    // XmlListModelRole { name: "gamma0_enabled"; query: "gamma0/enabled/string()" }
                    // XmlListModelRole { name: "gamma1_enabled"; query: "gamma1/enabled/string()" }
                    // XmlListModelRole { name: "gamma2_enabled"; query: "gamma2/enabled/string()" }

                    // XmlListModelRole { name: "gamma0Id"; query: "gamma0/__id/string()" }
                    // XmlListModelRole { name: "gamma1Id"; query: "gamma1/__id/string()" }
                    // XmlListModelRole { name: "gamma2Id"; query: "gamma2/__id/string()" }
                }

                delegate: EaComponents.TableViewDelegate {

                    EaComponents.TableViewTextInput {
                        enabled: model.gamma0_enabled === 'True'
                        width: tableViewLorentz.width / contentRowData.length
                        headerText: "γ0"
                        text: EaLogic.Utils.toFixed(model.gamma0)
                        onEditingFinished: editParameterValue(model.gamma0Id, text)
                    }

                    EaComponents.TableViewTextInput {
                        enabled: model.gamma1_enabled === 'True'
                        width: tableViewLorentz.width / contentRowData.length
                        headerText: "γ1"
                        text: EaLogic.Utils.toFixed(model.gamma1)
                        onEditingFinished: editParameterValue(model.gamma1Id, text)
                    }

                    EaComponents.TableViewTextInput {
                        enabled: model.gamma2_enabled === 'True'
                        width: tableViewLorentz.width / contentRowData.length
                        headerText: "γ2"
                        text: EaLogic.Utils.toFixed(model.gamma2)
                        onEditingFinished: editParameterValue(model.gamma2Id, text)
                    }
                }
            }
        }
    }

    Row {
        spacing: EaStyle.Sizes.tableColumnSpacing * 2

        Column {
            EaElements.Label {
                enabled: false
                text: qsTr("Exponential coefficients")
            }

            EaComponents.TableView {
                id: tableViewExponential

                width: EaStyle.Sizes.sideBarContentWidth

                model: XmlListModel {
                    // xml: ExGlobals.Constants.proxy.parameters.instrumentParametersAsXml
                    // query: `/data`

                    // XmlListModelRole { name: "alpha0"; query: "alpha0/value/number()" }
                    // XmlListModelRole { name: "alpha1"; query: "alpha1/value/number()" }
                    // XmlListModelRole { name: "beta0"; query: "beta0/value/number()" }
                    // XmlListModelRole { name: "beta1"; query: "beta1/value/number()" }

                    // XmlListModelRole { name: "alpha0Id"; query: "alpha0/__id/string()" }
                    // XmlListModelRole { name: "alpha1Id"; query: "alpha1/__id/string()" }
                    // XmlListModelRole { name: "beta0Id"; query: "beta0/__id/string()" }
                    // XmlListModelRole { name: "beta1Id"; query: "beta1/__id/string()" }
                }

                delegate: EaComponents.TableViewDelegate {

                    EaComponents.TableViewTextInput {
                        width: tableViewExponential.width / contentRowData.length
                        headerText: "α0"
                        text: EaLogic.Utils.toFixed(model.alpha0)
                        onEditingFinished: editParameterValue(model.alpha0Id, text)
                    }

                    EaComponents.TableViewTextInput {
                        width: tableViewExponential.width / contentRowData.length
                        headerText: "α1"
                        text: EaLogic.Utils.toFixed(model.alpha1)
                        onEditingFinished: editParameterValue(model.alpha1Id, text)
                    }

                    EaComponents.TableViewTextInput {
                        width: tableViewExponential.width / contentRowData.length
                        headerText: "β0"
                        text: EaLogic.Utils.toFixed(model.beta0)
                        onEditingFinished: editParameterValue(model.beta0Id, text)
                    }

                    EaComponents.TableViewTextInput {
                        width: tableViewExponential.width / contentRowData.length
                        headerText: "β1"
                        text: EaLogic.Utils.toFixed(model.beta1)
                        onEditingFinished: editParameterValue(model.beta1Id, text)
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

