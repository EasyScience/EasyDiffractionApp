import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    id: table

    // Table model

    model: XmlListModel {
        xml: ExGlobals.Constants.proxy.fitablesListAsXml

        query: "/root/item"

        XmlRole { name: "number"; query: "number/number()" }
        XmlRole { name: "label"; query: "label/string()" }
        XmlRole { name: "value"; query: "value/number()" }
        XmlRole { name: "unit"; query: "unit/string()" }
        XmlRole { name: "error"; query: "error/number()" }
        XmlRole { name: "fit"; query: "fit/number()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            id: numberColumn
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.number
        }

        EaComponents.TableViewLabel {
            id: labelColumn
            horizontalAlignment: Text.AlignLeft
            width: table.width -
                   (parent.children.length - 1) * EaStyle.Sizes.tableColumnSpacing -
                   numberColumn.width -
                   valueColumn.width -
                   unitColumn.width -
                   errorColumn.width -
                   fitColumn.width
            headerText: "Label"
            text: model.label
        }

        EaComponents.TableViewTextInput {
            id: valueColumn
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Value"
            text: model.value.toFixed(4)
            onEditingFinished: ExGlobals.Constants.proxy.editFitableByIndexAndName(model.index, "value", text)
            Component.onCompleted: {
                if (model.label === "Sin.x_shift")
                    ExGlobals.Variables.xShiftValueTextInput = valueColumn
            }
        }

        EaComponents.TableViewLabel {
            id: unitColumn
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize
            text: model.unit
        }

        EaComponents.TableViewLabel {
            id: errorColumn
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Error"
            text: !fitColumn.checked || model.error === 0.0 || model.error > 999999 ? "" : model.error.toFixed(4)
        }

        EaComponents.TableViewCheckBox {
            id: fitColumn
            width: EaStyle.Sizes.fontPixelSize * 3
            headerText: "Fit"
            checked: model.fit
            onToggled: ExGlobals.Constants.proxy.editFitableByIndexAndName(model.index, "fit", checked)
            Component.onCompleted: {
                if (model.label === "Sin.x_shift")
                    ExGlobals.Variables.xShiftFitCheckBox = fitColumn
            }
        }
    }

}
