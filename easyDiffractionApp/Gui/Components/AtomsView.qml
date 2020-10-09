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
        property int phaseIndex: ExGlobals.Variables.phasesCurrentIndex + 1

        xml: ExGlobals.Constants.proxy.phasesXml
        query: `/root/item[${phaseIndex}]/atoms/item`

        XmlRole { name: "label"; query: "label/string()" }
        XmlRole { name: "type"; query: "type/string()" }
        XmlRole { name: "color"; query: "color/string()" }
        XmlRole { name: "x"; query: "x/number()" }
        XmlRole { name: "y"; query: "y/number()" }
        XmlRole { name: "z"; query: "z/number()" }
        XmlRole { name: "occupancy"; query: "occupancy/number()" }
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
        }

        EaComponents.TableViewComboBox {
            width: atomLabel.width
            currentIndex: model.indexOf(modelType)
            headerText: "Atom"
            model: ["Mn", "Fe", "Co", "Ni", "Cu", "Si", "O"]
        }

        EaComponents.TableViewLabel {
            headerText: "Color"
            backgroundColor: model.color
        }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "x"
            text: model.x
        }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "y"
            text: model.y
        }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "z"
            text: model.z
        }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "Occupancy"
            text: model.occupancy
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this atom")
            onClicked: ExGlobals.Constants.proxy.removeConstraintByIndex(model.index)
        }

    }

}
