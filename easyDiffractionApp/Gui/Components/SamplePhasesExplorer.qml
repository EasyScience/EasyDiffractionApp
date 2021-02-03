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
    //id: phasesTable

    defaultInfoText: qsTr("No Samples Added/Loaded")

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Constants.proxy.currentPhaseIndex + 1

        xml: ExGlobals.Constants.proxy.phasesAsXml
        query: "/root/item"

        XmlRole { name: "label"; query: "name/string()" }
        XmlRole { name: "color"; query: "color/string()" }

        onXmlChanged: {
            if (ExGlobals.Constants.proxy.phasesAsObj.length === 0) {
                ExGlobals.Variables.experimentPageEnabled = false
                ExGlobals.Variables.sampleLoaded = false
                ExGlobals.Variables.analysisPageEnabled = false
                ExGlobals.Variables.summaryPageEnabled = false
            }
        }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        //property string modelColor: model.color ? model.color : "transparent"

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 27.9
            headerText: "Label"
            text: model.label
            //onEditingFinished: ExGlobals.Constants.proxy.changePhaseName(text) // use Id
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
            backgroundColor: model.color ? model.color : "transparent"
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this phase")
            onClicked: ExGlobals.Constants.proxy.removePhase(model.label)
        }

    }

    onCurrentIndexChanged: {
        ExGlobals.Constants.proxy.currentPhaseIndex = currentIndex //ExGlobals.Constants.proxy.currentPhaseIndex = currentIndex
    }

}
