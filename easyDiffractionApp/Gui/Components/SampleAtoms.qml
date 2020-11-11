import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView { 
    property bool enableDelButton:
        typeof ExGlobals.Constants.proxy.phaseList[ExGlobals.Constants.proxy.currentPhaseIndex] !== 'undefined'
        && ExGlobals.Constants.proxy.phaseList[ExGlobals.Constants.proxy.currentPhaseIndex].atoms.data.length > 1
        ? true
        : false

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Constants.proxy.currentPhaseIndex + 1

        xml: ExGlobals.Constants.proxy.phasesAsXml
        query: `/root/item[${phaseIndex}]/atoms/data/item`

        XmlRole { name: "label"; query: "label/value/string()" }
        XmlRole { name: "type"; query: "specie/value/string()" }
        XmlRole { name: "color"; query: "color/string()" }
        XmlRole { name: "x"; query: "fract_x/value/number()" }
        XmlRole { name: "y"; query: "fract_y/value/number()" }
        XmlRole { name: "z"; query: "fract_z/value/number()" }
        XmlRole { name: "occupancy"; query: "occupancy/value/number()" }

        XmlRole { name: "labelId"; query: "label/key[4]/string()" }
        XmlRole { name: "typeId"; query: "specie/key[4]/string()" }
        XmlRole { name: "xId"; query: "fract_x/key[4]/string()" }
        XmlRole { name: "yId"; query: "fract_y/key[4]/string()" }
        XmlRole { name: "zId"; query: "fract_z/key[4]/string()" }
        XmlRole { name: "occupancyId"; query: "occupancy/key[4]/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property string modelType: model.type

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewTextInput {
            id: atomLabel
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 4.22
            headerText: "Label"
            text: model.label
            onEditingFinished: editDescriptorValue(model.labelId, text)
        }

        /*
        EaComponents.TableViewComboBox {
            width: atomLabel.width
            currentIndex: model.indexOf(modelType)
            headerText: "Atom"
            model: ["Mn", "Fe", "Co", "Ni", "Cu", "Si", "O"]
        }
        */
        EaComponents.TableViewTextInput {
            width: atomLabel.width
            horizontalAlignment: Text.AlignLeft
            headerText: "Atom"
            text: model.type
            onEditingFinished: editDescriptorValue(model.typeId, text)
        }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "x"
            text: model.x
            onEditingFinished: editParameterValue(model.xId, text)
        }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "y"
            text: model.y
            onEditingFinished: editParameterValue(model.yId, text)
       }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "z"
            text: model.z
            onEditingFinished: editParameterValue(model.zId, text)
        }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "Occ."
            text: model.occupancy
            onEditingFinished: editParameterValue(model.occupancyId, text)
        }

        EaComponents.TableViewLabel {
            headerText: "Color"
            backgroundColor: model.color ? model.color : "transparent"
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            enabled: enableDelButton
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this atom")
            onClicked: ExGlobals.Constants.proxy.removeAtom(model.label)
        }

    }

    onCurrentIndexChanged: ExGlobals.Variables.currentAtomIndex = currentIndex

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameterValue(id, parseFloat(value))
    }

    function editDescriptorValue(id, value) {
        ExGlobals.Constants.proxy.editDescriptorValue(id, value)
    }

}
