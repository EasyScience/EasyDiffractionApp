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

        XmlRole { name: "u"; query: "resolution_u/value/number()" }
        XmlRole { name: "v"; query: "resolution_v/value/number()" }
        XmlRole { name: "w"; query: "resolution_w/value/number()" }
        XmlRole { name: "x"; query: "resolution_x/value/number()" }
        XmlRole { name: "y"; query: "resolution_y/value/number()" }

        XmlRole { name: "uId"; query: "resolution_u/key[4]/string()" }
        XmlRole { name: "vId"; query: "v_resolution/key[4]/string()" }
        XmlRole { name: "wId"; query: "resolution_w/key[4]/string()" }
        XmlRole { name: "xId"; query: "resolution_x/key[4]/string()" }
        XmlRole { name: "yId"; query: "resolution_y/key[4]/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewTextInput {
            id: uLabel
            width: EaStyle.Sizes.fontPixelSize * 7.1
            headerText: "U"
            text: EaLogic.Utils.toFixed(model.u)
            onEditingFinished: editParameterValue(model.uId, text)
        }

        EaComponents.TableViewTextInput {
            width: uLabel.width
            headerText: "V"
            text: EaLogic.Utils.toFixed(model.v)
            onEditingFinished: editParameterValue(model.vId, text)
        }

        EaComponents.TableViewTextInput {
            width: uLabel.width
            headerText: "W"
            text: EaLogic.Utils.toFixed(model.w)
            onEditingFinished: editParameterValue(model.wId, text)
        }

        EaComponents.TableViewTextInput {
            width: uLabel.width
            headerText: "X"
            text: EaLogic.Utils.toFixed(model.x)
            onEditingFinished: editParameterValue(model.xId, text)
        }

        EaComponents.TableViewTextInput {
            width: uLabel.width
            headerText: "Y"
            text: EaLogic.Utils.toFixed(model.y)
            onEditingFinished: editParameterValue(model.yId, text)
        }

    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameter(id, parseFloat(value))
    }

}
