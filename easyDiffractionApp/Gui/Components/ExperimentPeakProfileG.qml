import QtQuick
import QtQuick.Controls
import QtQml.XmlListModel

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    id: tableView

    width: EaStyle.Sizes.sideBarContentWidth * 3 / 5 - EaStyle.Sizes.fontPixelSize / 2

    // Table model

    model: XmlListModel {
        xml: ExGlobals.Constants.proxy.instrumentParametersAsXml
        query: `/root/item`

        XmlListModelRole { name: "u"; query: "resolution_u/value/number()" }
        XmlListModelRole { name: "v"; query: "resolution_v/value/number()" }
        XmlListModelRole { name: "w"; query: "resolution_w/value/number()" }

        XmlListModelRole { name: "uId"; query: "resolution_u/key[4]/string()" }
        XmlListModelRole { name: "vId"; query: "v_resolution/key[4]/string()" }
        XmlListModelRole { name: "wId"; query: "resolution_w/key[4]/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewTextInput {
            width: tableView.width / contentRowData.length
            headerText: "U"
            text: EaLogic.Utils.toFixed(model.u)
            onEditingFinished: editParameterValue(model.uId, text)
        }

        EaComponents.TableViewTextInput {
            width: tableView.width / contentRowData.length
            headerText: "V"
            text: EaLogic.Utils.toFixed(model.v)
            onEditingFinished: editParameterValue(model.vId, text)
        }

        EaComponents.TableViewTextInput {
            width: tableView.width / contentRowData.length
            headerText: "W"
            text: EaLogic.Utils.toFixed(model.w)
            onEditingFinished: editParameterValue(model.wId, text)
        }
    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameter(id, parseFloat(value))
    }

}
