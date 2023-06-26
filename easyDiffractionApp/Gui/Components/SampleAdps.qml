// SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    property int numColumnWidth: EaStyle.Sizes.fontPixelSize * 2.5
    property int labelColumnWidth: EaStyle.Sizes.fontPixelSize * 2.5
    property int typeColumnWidth: EaStyle.Sizes.fontPixelSize * 4.0
    property int numFixedColumn: 3
    property int numFlexColumn: 7
    property bool adpIso: true
    property int flexColumnWidth: (width -
                                    numColumnWidth -
                                    labelColumnWidth -
                                    typeColumnWidth -
                                    EaStyle.Sizes.tableColumnSpacing * (numFixedColumn + numFlexColumn - 1)) /
                                    numFlexColumn

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Constants.proxy.phase.currentPhaseIndex + 1

        xml: ExGlobals.Constants.proxy.phase.phasesAsXml
        query: `/data/item/atoms/data`

        XmlRole { name: "label"; query: "label/value/string()" }
        XmlRole { name: "adpType"; query: "adp/adp_type/value/string()" }
        XmlRole { name: "adpIso"; query: "adp/adp_class/Uiso/value/number()" }
        XmlRole { name: "adpAni11"; query: "adp/adp_class/U_11/value/number()" }
        XmlRole { name: "adpAni22"; query: "adp/adp_class/U_22/value/number()" }
        XmlRole { name: "adpAni33"; query: "adp/adp_class/U_33/value/number()" }
        XmlRole { name: "adpAni12"; query: "adp/adp_class/U_12/value/number()" }
        XmlRole { name: "adpAni13"; query: "adp/adp_class/U_13/value/number()" }
        XmlRole { name: "adpAni23"; query: "adp/adp_class/U_23/value/number()" }

        XmlRole { name: "adpIsoId"; query: "adp/adp_class/Uiso/__id/string()" }
        XmlRole { name: "adpAniId11"; query: "adp/adp_class/U_11/__id/string()" }
        XmlRole { name: "adpAniId22"; query: "adp/adp_class/U_22/__id/string()" }
        XmlRole { name: "adpAniId33"; query: "adp/adp_class/U_33/__id/string()" }
        XmlRole { name: "adpAniId12"; query: "adp/adp_class/U_12/__id/string()" }
        XmlRole { name: "adpAniId13"; query: "adp/adp_class/U_13/__id/string()" }
        XmlRole { name: "adpAniId23"; query: "adp/adp_class/U_23/__id/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property string modelAdpType: model.adpType
        property int modelIndex: model.index
        property string adpIsoId: model.adpIsoId

        EaComponents.TableViewLabel {
            width: numColumnWidth
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewLabel {
            horizontalAlignment: Text.AlignLeft
            width: labelColumnWidth
            headerText: "Label"
            text: model.label
        }

        EaComponents.TableViewComboBox {
            id: adpTypeComboBox
            enabled: true
            width: typeColumnWidth
            headerText: "Type"
            // model: ["Uiso", "Uani", "Biso", "Bani"]
            model: ["Uiso", "Uani"]
            currentIndex: model.indexOf(modelAdpType)
            Component.onCompleted: {
                currentIndex = model.indexOf(modelAdpType)
                if (currentIndex === -1) {
                    currentIndex = 0
                }
            }
            onCurrentIndexChanged: {
                updateAdpType(adpIsoId, modelIndex, textAt(currentIndex))
            }
        }

        EaComponents.TableViewTextInput {
            enabled: adpTypeComboBox.currentText === "Uiso" || adpTypeComboBox.currentText === "Biso"
            width: flexColumnWidth
            headerText: "Iso"
            text: EaLogic.Utils.toFixed(model.adpIso)
            onEditingFinished: {
                // updateUiso(model.adpIsoId, modelIndex, text);
                // editParameterValue(model.adpIsoId, text)
                updateAniFromIso(model.adpIsoId, modelIndex, text)
            }
        }

        EaComponents.TableViewTextInput {
            enabled: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            visible: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            width: flexColumnWidth
            headerText: "Ani11"
            text: EaLogic.Utils.toFixed(model.adpAni11)
            onEditingFinished: updateIsoFromAni(model.adpAniId11, modelIndex, text)
        }

        EaComponents.TableViewTextInput {
            enabled: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            visible: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            width: flexColumnWidth
            headerText: "Ani22"
            text: EaLogic.Utils.toFixed(model.adpAni22)
            onEditingFinished: updateIsoFromAni(model.adpAniId22, modelIndex, text)
        }

        EaComponents.TableViewTextInput {
            enabled: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            visible: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            width: flexColumnWidth
            headerText: "Ani33"
            text: EaLogic.Utils.toFixed(model.adpAni33)
            onEditingFinished: updateIsoFromAni(model.adpAniId33, modelIndex, text)
        }

        EaComponents.TableViewTextInput {
            enabled: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            visible: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            width: flexColumnWidth
            headerText: "Ani12"
            text: EaLogic.Utils.toFixed(model.adpAni12)
            onEditingFinished: updateIsoFromAni(model.adpAniId12, modelIndex, text)
        }

        EaComponents.TableViewTextInput {
            enabled: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            visible: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            width: flexColumnWidth
            headerText: "Ani13"
            text: EaLogic.Utils.toFixed(model.adpAni13)
            onEditingFinished: updateIsoFromAni(model.adpAniId13, modelIndex, text)
        }

        EaComponents.TableViewTextInput {
            enabled: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            visible: adpTypeComboBox.currentText === "Uani" || adpTypeComboBox.currentText === "Bani"
            width: flexColumnWidth
            headerText: "Ani23"
            text: EaLogic.Utils.toFixed(model.adpAni23)
            onEditingFinished: updateIsoFromAni(model.adpAniId23, modelIndex, text)
        }

    }

    // Logic
    function updateAdpType(id, atom_id, value) {
        ExGlobals.Constants.proxy.parameters.updateAdpType(id, parseInt(atom_id), value)
    }
    function updateAniFromIso(id, atom_id, value){
        ExGlobals.Constants.proxy.parameters.updateAniFromIso(id, parseInt(atom_id), parseFloat(value))
    }
    function updateIsoFromAni(id, atom_id, value){
        ExGlobals.Constants.proxy.parameters.updateIsoFromAni(id, parseInt(atom_id), parseFloat(value))
    }
    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }

}
