// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
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
        XmlRole { name: "adpIso"; query: `adp/adp_class/Uiso/value/number()` }
        XmlRole { name: "adpAni11"; query: "adp_ani_11/number()" }
        XmlRole { name: "adpAni22"; query: "adp_ani_22/number()" }
        XmlRole { name: "adpAni33"; query: "adp_ani_33/number()" }
        XmlRole { name: "adpAni12"; query: "adp_ani_12/number()" }
        XmlRole { name: "adpAni13"; query: "adp_ani_13/number()" }
        XmlRole { name: "adpAni23"; query: "adp_ani_23/number()" }

        XmlRole { name: "adpIsoId"; query: "adp/adp_class/Uiso/__id/string()" }
        XmlRole { name: "adpAni11Id"; query: "adp_ani_11/__id/string()" }
        XmlRole { name: "adpAni22Id"; query: "adp_ani_22/__id/string()" }
        XmlRole { name: "adpAni33Id"; query: "adp_ani_33/__id/string()" }
        XmlRole { name: "adpAni12Id"; query: "adp_ani_12/__id/string()" }
        XmlRole { name: "adpAni13Id"; query: "adp_ani_13/__id/string()" }
        XmlRole { name: "adpAni23Id"; query: "adp_ani_23/__id/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property string modelAdpType: model.adpType

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
            enabled: false
            width: typeColumnWidth
            headerText: "Type"
            model: ["Uiso", "Uani", "Biso", "Bani"]
            //currentIndex: model.indexOf(modelAdpType)
            Component.onCompleted: currentIndex = model.indexOf(modelAdpType)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "Iso"
            text: EaLogic.Utils.toFixed(model.adpIso)
            onEditingFinished: editParameterValue(model.adpIsoId, text)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "Ani11"
            text: EaLogic.Utils.toFixed(model.adpAni11)
            onEditingFinished: editParameterValue(model.adpAniId11, text)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "Ani22"
            text: EaLogic.Utils.toFixed(model.adpAni22)
            onEditingFinished: editParameterValue(model.adpAniId22, text)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "Ani33"
            text: EaLogic.Utils.toFixed(model.adpAni33)
            onEditingFinished: editParameterValue(model.adpAniId33, text)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "Ani12"
            text: EaLogic.Utils.toFixed(model.adpAni12)
            onEditingFinished: editParameterValue(model.adpAniId12, text)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "Ani13"
            text: EaLogic.Utils.toFixed(model.adpAni13)
            onEditingFinished: editParameterValue(model.adpAniId13, text)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "Ani23"
            text: EaLogic.Utils.toFixed(model.adpAni23)
            onEditingFinished: editParameterValue(model.adpAniId23, text)
        }

    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }

}
