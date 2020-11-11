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

    defaultInfoText: qsTr("No Associated Phases")

    // Table model

    model: XmlListModel {
        xml: ExGlobals.Constants.proxy.phasesAsXml
        query: "/root/item"

        XmlRole { name: "label"; query: "name/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            id: numColumn
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.sideBarContentWidth
                   - numColumn.width
                   - scaleColumn.width
                   - useColumn.width
                   - deleteRowColumn.width
                   - EaStyle.Sizes.tableColumnSpacing * 4
                   - EaStyle.Sizes.borderThickness * 2
            headerText: "Label"
            text: model.label
        }

        EaComponents.TableViewTextInput {
            id: scaleColumn
            horizontalAlignment: Text.AlignRight
            headerText: "Scale"
            text: "0.1620"
        }

        EaComponents.TableViewCheckBox {
            id: useColumn
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Use"
            checked: true
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del."
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this phase")
        }

    }


}
