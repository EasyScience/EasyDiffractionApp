import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Constants.proxy.currentPhaseIndex + 1
        //property int atomIndex: ExGlobals.Variables.atomsCurrentIndex + 1
//        property string adpType: ""
//        onAdpTypeChanged: print("???", adpType)

        //xml: ExGlobals.Constants.proxy.phasesAsXml
        //query: `/root/item[${phaseIndex}]/atoms/item`

        xml: ExGlobals.Constants.proxy.phasesAsXml
        query: `/root/item[${phaseIndex}]/atoms/data/item`

 //       onXmlChanged: print("+++", model.adp_type)

        XmlRole { name: "label"; query: "label/value/string()" }
        XmlRole { name: "adp_type"; query: "adp/adp_type/value/string()" }
        XmlRole { name: "adp_iso"; query: `adp/adp_class/Uiso/value/number()` }
        XmlRole { name: "adp_ani_11"; query: "adp_ani_11/number()" }
        XmlRole { name: "adp_ani_22"; query: "adp_ani_22/number()" }
        XmlRole { name: "adp_ani_33"; query: "adp_ani_33/number()" }
        XmlRole { name: "adp_ani_12"; query: "adp_ani_12/number()" }
        XmlRole { name: "adp_ani_13"; query: "adp_ani_13/number()" }
        XmlRole { name: "adp_ani_23"; query: "adp_ani_23/number()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property string modelAdpType: model.adp_type

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewLabel {
            id: adpAtomLabel
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 3.8
            headerText: "Label"
            text: model.label
        }

        EaComponents.TableViewComboBox {
            width: adpAtomLabel.width * 1.1
            currentIndex: model.indexOf(modelAdpType)
            headerText: "Type"
            model: ["Uiso", "Uani", "Biso", "Bani"]
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "Uiso"
            text: model.adp_iso
            //onTextChanged: print("!!!!!", model.adp_iso)
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "U11"
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "U22"
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "U33"
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "U12"
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "U13"
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "U23"
        }

    }

}
