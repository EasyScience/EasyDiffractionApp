import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Globals 1.0 as EaGlobals
import easyApp.Style 1.0 as EaStyle
import easyApp.Elements 1.0 as EaElements
import easyApp.Components 1.0 as EaComponents
import easyApp.Logic 1.0 as EaLogic

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
            onEditingFinished: ExGlobals.Constants.proxy.setCurrentPhaseName(text)
        }

        EaComponents.TableViewLabel {
            headerText: "Color"
            //backgroundColor: model.color ? model.color : "transparent"
            backgroundColor: EaStyle.Colors.chartForegrounds[1]
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
        ExGlobals.Constants.proxy.currentPhaseIndex = currentIndex
    }

}
