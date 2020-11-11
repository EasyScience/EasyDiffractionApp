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
        xml: ExGlobals.Constants.proxy.instrumentResolutionAsXml
        query: `/root/item`

        XmlRole { name: "u"; query: "U/number()" }
        XmlRole { name: "v"; query: "V/number()" }
        XmlRole { name: "w"; query: "W/number()" }
        XmlRole { name: "x"; query: "X/number()" }
        XmlRole { name: "y"; query: "Y/number()" }

        XmlRole { name: "uId"; query: "U/key[4]/string()" }
        XmlRole { name: "vId"; query: "V/key[4]/string()" }
        XmlRole { name: "wId"; query: "W/key[4]/string()" }
        XmlRole { name: "xId"; query: "X/key[4]/string()" }
        XmlRole { name: "yId"; query: "Y/key[4]/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewTextInput {
            id: uLabel
            width: EaStyle.Sizes.fontPixelSize * 7.1
            headerText: "U"
            text: model.u
            onEditingFinished: editParameterValue(model.uId, text)
        }

        EaComponents.TableViewTextInput {
            width: uLabel.width
            headerText: "V"
            text: model.v
            onEditingFinished: editParameterValue(model.vId, text)
        }

        EaComponents.TableViewTextInput {
            width: uLabel.width
            headerText: "W"
            text: model.w
            onEditingFinished: editParameterValue(model.wId, text)
        }

        EaComponents.TableViewTextInput {
            width: uLabel.width
            headerText: "X"
            text: model.x
            onEditingFinished: editParameterValue(model.xId, text)
        }

        EaComponents.TableViewTextInput {
            width: uLabel.width
            headerText: "Y"
            text: model.y
            onEditingFinished: editParameterValue(model.yId, text)
        }

    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameterValue(id, parseFloat(value))
    }

}
