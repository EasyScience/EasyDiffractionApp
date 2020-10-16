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

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Variables.phasesCurrentIndex + 1

        xml: ExGlobals.Constants.proxy.phasesXml
        query: `/root/item[${phaseIndex}]/atoms/data/item`

/////        onXmlChanged: print(EaLogic.Utils.prettyXml(ExGlobals.Constants.proxy.phasesXml))
        //onXmlChanged: print(ExGlobals.Constants.proxy.phasesXml)

        XmlRole { name: "label"; query: "label/value/string()" }
        XmlRole { name: "type"; query: "specie/value/string()" }
        XmlRole { name: "color"; query: "color/string()" }
        XmlRole { name: "x"; query: "fract_x/value/number()" }
        XmlRole { name: "y"; query: "fract_y/value/number()" }
        XmlRole { name: "z"; query: "fract_z/value/number()" }
        XmlRole { name: "occupancy"; query: "occupancy/value/number()" }
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

    onCurrentIndexChanged: ExGlobals.Variables.atomsCurrentIndex = currentIndex

}
