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
        xml: ExGlobals.Constants.proxy.instrumentParametersAsXml
        query: `/root/item`

        XmlRole { name: "u"; query: "u_resolution/value/number()" }
        XmlRole { name: "v"; query: "v_resolution/value/number()" }
        XmlRole { name: "w"; query: "w_resolution/value/number()" }
        XmlRole { name: "x"; query: "x_resolution/value/number()" }
        XmlRole { name: "y"; query: "y_resolution/value/number()" }

        XmlRole { name: "uId"; query: "u_resolution/key[4]/string()" }
        XmlRole { name: "vId"; query: "v_resolution/key[4]/string()" }
        XmlRole { name: "wId"; query: "w_resolution/key[4]/string()" }
        XmlRole { name: "xId"; query: "x_resolution/key[4]/string()" }
        XmlRole { name: "yId"; query: "y_resolution/key[4]/string()" }
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
