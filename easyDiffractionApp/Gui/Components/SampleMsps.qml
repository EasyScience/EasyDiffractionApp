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

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Constants.proxy.phase.currentPhaseIndex + 1

        xml: ExGlobals.Constants.proxy.phase.phasesAsXml
        query: `/root/item[${phaseIndex}]/atoms/data/item`

        XmlRole { name: "label"; query: "label/value/string()" }
        XmlRole { name: "mspType"; query: "msp/msp_type/value/string()" }
        XmlRole { name: "mspIso"; query: `msp/msp_class/Uiso/value/number()` }
        XmlRole { name: "mspAni11"; query: "msp_ani_11/number()" }
        XmlRole { name: "mspAni22"; query: "msp_ani_22/number()" }
        XmlRole { name: "mspAni33"; query: "msp_ani_33/number()" }
        XmlRole { name: "mspAni12"; query: "msp_ani_12/number()" }
        XmlRole { name: "mspAni13"; query: "msp_ani_13/number()" }
        XmlRole { name: "mspAni23"; query: "msp_ani_23/number()" }

        XmlRole { name: "mspIsoId"; query: "msp/msp_class/Uiso/key[4]/string()" }
        XmlRole { name: "mspAni11Id"; query: "msp_ani_11/key[4]/string()" }
        XmlRole { name: "mspAni22Id"; query: "msp_ani_22/key[4]/string()" }
        XmlRole { name: "mspAni33Id"; query: "msp_ani_33/key[4]/string()" }
        XmlRole { name: "mspAni12Id"; query: "msp_ani_12/key[4]/string()" }
        XmlRole { name: "mspAni13Id"; query: "msp_ani_13/key[4]/string()" }
        XmlRole { name: "mspAni23Id"; query: "msp_ani_23/key[4]/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property string modelmspType: model.mspType

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewLabel {
            id: mspAtomLabel
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 3.8
            headerText: "Label"
            text: model.label
        }

        EaComponents.TableViewComboBox {
            enabled: false
            width: mspAtomLabel.width * 1.2
            headerText: "Type"
            model: ["Cani", "Ciso"]
            //currentIndex: model.indexOf(modelmspType)
            Component.onCompleted: currentIndex = model.indexOf(modelmspType)
        }

        EaComponents.TableViewTextInput {
            width: mspAtomLabel.width
            headerText: "\u03C7Iso"
            text: EaLogic.Utils.toFixed(model.mspIso)
            onEditingFinished: editParameterValue(model.mspIsoId, text)
        }

        EaComponents.TableViewTextInput {
            width: mspAtomLabel.width
            headerText: "\u03C711"
            text: EaLogic.Utils.toFixed(model.mspAni11)
            onEditingFinished: editParameterValue(model.mspAniId11, text)
        }

        EaComponents.TableViewTextInput {
            width: mspAtomLabel.width
            headerText: "\u03C722"
            text: EaLogic.Utils.toFixed(model.mspAni22)
            onEditingFinished: editParameterValue(model.mspAniId22, text)
        }

        EaComponents.TableViewTextInput {
            width: mspAtomLabel.width
            headerText: "\u03C733"
            text: EaLogic.Utils.toFixed(model.mspAni33)
            onEditingFinished: editParameterValue(model.mspAniId33, text)
        }

        EaComponents.TableViewTextInput {
            width: mspAtomLabel.width
            headerText: "\u03C712"
            text: EaLogic.Utils.toFixed(model.mspAni12)
            onEditingFinished: editParameterValue(model.mspAniId12, text)
        }

        EaComponents.TableViewTextInput {
            width: mspAtomLabel.width
            headerText: "\u03C713"
            text: EaLogic.Utils.toFixed(model.mspAni13)
            onEditingFinished: editParameterValue(model.mspAniId13, text)
        }

        EaComponents.TableViewTextInput {
            width: mspAtomLabel.width
            headerText: "\u03C723"
            text: EaLogic.Utils.toFixed(model.mspAni23)
            onEditingFinished: editParameterValue(model.mspAniId23, text)
        }

    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }

}

