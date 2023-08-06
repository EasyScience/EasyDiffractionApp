import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQml.XmlListModel

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {

    defaultInfoText: qsTr("No Background Points Added")

    // Table model

    model: XmlListModel {
        // xml: ExGlobals.Constants.proxy.backgroundProxy.asXml
        // query: "/data/data"

        // XmlListModelRole { name: "x"; query: "x/value/number()" }
        // XmlListModelRole { name: "y"; query: "y/value/number()" }

        // XmlListModelRole { name: "pointName"; query: "name/string()" }
        // XmlListModelRole { name: "xId"; query: "x/__id/string()" }
        // XmlListModelRole { name: "yId"; query: "y/__id/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewTextInput {
            id: xLabel
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 11.6
            headerText: "2θ"
            text: EaLogic.Utils.toFixed(model.x)
            onEditingFinished: editParameterValue(model.xId, text)
        }

        EaComponents.TableViewTextInput {
            id: yLabel
            horizontalAlignment: Text.AlignRight
            width: xLabel.width
            headerText: "Intensity"
            text: EaLogic.Utils.toFixed(model.y)
            onEditingFinished: editParameterValue(model.yId, text)
        }

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 7
        }

        EaComponents.TableViewButton {
            headerText: "Del."
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this point")
            onClicked: ExGlobals.Constants.proxy.backgroundProxy.removePoint(model.pointName)
        }

    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameter(id, parseFloat(value))
    }

}
