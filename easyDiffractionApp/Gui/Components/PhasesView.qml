import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    //id: phasesTable

    defaultInfoText: qsTr("No Samples Added/Loaded")

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Variables.phasesCurrentIndex + 1

        //xml: ExGlobals.Variables.sampleLoaded ? ExGlobals.Constants.proxy.phasesXml : ""
        xml: ExGlobals.Constants.proxy.phasesXml
        query: "/root/item"

        XmlRole { name: "label"; query: "label/string()" }
        XmlRole { name: "color"; query: "color/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property string modelColor: model.color

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewLabel {
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 27.9
            headerText: "Label"
            text: model.label
        }

        /*
        EaComponents.TableViewComboBox {
            width: 130
            //displayText: ""
            //backgroundColor: modelColor
            foregroundColor: modelColor
            currentIndex: model.indexOf(modelColor)
            headerText: "Color"
            model: ["coral", "darkolivegreen", "steelblue"]
            onActivated: ExGlobals.Constants.proxy.editPhase(phasesTable.currentIndex,
                                                             "color",
                                                             currentText)
        }
        */

        EaComponents.TableViewLabel {
            headerText: "Color"
            backgroundColor: model.color
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this phase")
        }

    }

    onCurrentIndexChanged: ExGlobals.Variables.phasesCurrentIndex = currentIndex
}
