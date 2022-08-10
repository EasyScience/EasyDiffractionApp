// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls
import QtQml.XmlListModel

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Constants.proxy.phase.currentPhaseIndex + 1

        xml: ExGlobals.Constants.proxy.phase.phasesAsXml
        query: `/root/item[${phaseIndex}]`

        XmlListModelRole { name: "a"; query: "cell/length_a/value/number()" }
        XmlListModelRole { name: "b"; query: "cell/length_b/value/number()" }
        XmlListModelRole { name: "c"; query: "cell/length_c/value/number()" }
        XmlListModelRole { name: "alpha"; query: "cell/angle_alpha/value/number()" }
        XmlListModelRole { name: "beta"; query: "cell/angle_beta/value/number()" }
        XmlListModelRole { name: "gamma"; query: "cell/angle_gamma/value/number()" }

        XmlListModelRole { name: "a_enabled"; query: "cell/length_a/enabled/string()"}
        XmlListModelRole { name: "b_enabled"; query: "cell/length_b/enabled/string()"}
        XmlListModelRole { name: "c_enabled"; query: "cell/length_c/enabled/string()"}
        XmlListModelRole { name: "alpha_enabled"; query: "cell/angle_alpha/enabled/string()" }
        XmlListModelRole { name: "beta_enabled"; query: "cell/angle_beta/enabled/string()"}
        XmlListModelRole { name: "gamma_enabled"; query: "cell/angle_gamma/enabled/string()"}

        XmlListModelRole { name: "aId"; query: "cell/length_a/key[4]/string()" }
        XmlListModelRole { name: "bId"; query: "cell/length_b/key[4]/string()" }
        XmlListModelRole { name: "cId"; query: "cell/length_c/key[4]/string()" }
        XmlListModelRole { name: "alphaId"; query: "cell/angle_alpha/key[4]/string()" }
        XmlListModelRole { name: "betaId"; query: "cell/angle_beta/key[4]/string()" }
        XmlListModelRole { name: "gammaId"; query: "cell/angle_gamma/key[4]/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewTextInput {
            id: cellLengthALabel
            enabled: model.a_enabled === 'True'
            width: EaStyle.Sizes.fontPixelSize * 5.8
            headerText: "a (Å)"
            text: EaLogic.Utils.toFixed(model.a)
            onEditingFinished: editParameterValue(model.aId, text)
            Component.onCompleted: ExGlobals.Variables.cellLengthALabel = this
        }

        EaComponents.TableViewTextInput {
            enabled: model.b_enabled === 'True'
            width: cellLengthALabel.width
            headerText: "b (Å)"
            text: EaLogic.Utils.toFixed(model.b)
            onEditingFinished: editParameterValue(model.bId, text)
        }

        EaComponents.TableViewTextInput {
            enabled: model.c_enabled === 'True'
            width: cellLengthALabel.width
            headerText: "c (Å)"
            text: EaLogic.Utils.toFixed(model.c)
            onEditingFinished: editParameterValue(model.cId, text)
        }

        EaComponents.TableViewTextInput {
            enabled: model.alpha_enabled === 'True'
            width: cellLengthALabel.width
            headerText: "alpha (°)"
            text: EaLogic.Utils.toFixed(model.alpha)
            onEditingFinished: editParameterValue(model.alphaId, text)
        }

        EaComponents.TableViewTextInput {
            enabled: model.beta_enabled === 'True'
            width: cellLengthALabel.width
            headerText: "beta (°)"
            text: EaLogic.Utils.toFixed(model.beta)
            onEditingFinished: editParameterValue(model.betaId, text)
        }

        EaComponents.TableViewTextInput {
            enabled: model.gamma_enabled === 'True'
            width: cellLengthALabel.width
            headerText: "gamma (°)"
            text: EaLogic.Utils.toFixed(model.gamma)
            onEditingFinished: editParameterValue(model.gammaId, text)
        }

    }

    // Logic

    function editParameterValue(id, value) {
        //ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }

}
