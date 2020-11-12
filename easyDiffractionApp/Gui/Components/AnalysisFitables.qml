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
        id: fitablesModel

        xml: ExGlobals.Constants.proxy.fitablesListAsXml

        query: "/root/item"

        XmlRole { name: "id"; query: "id/string()" }
        XmlRole { name: "number"; query: "number/number()" }
        XmlRole { name: "label"; query: "label/string()" }
        XmlRole { name: "value"; query: "value/number()" }
        XmlRole { name: "unit"; query: "unit/string()" }
        XmlRole { name: "error"; query: "error/number()" }
        XmlRole { name: "fit"; query: "fit/number()" }

        onStatusChanged: {
            if (status === XmlListModel.Ready) {
                storeCurrentParameter()
            }
        }
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
                   useColumn.width
            headerText: "Label"
            text: formatLabel(model.index, model.label)
            textFormat: Text.RichText
        }

        EaComponents.TableViewTextInput {
            id: valueColumn
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Value"
            text: model.value.toFixed(4)
            onEditingFinished: editParameterValue(model.id, text)
        }

        EaComponents.TableViewLabel {
            id: unitColumn
            enabled: false
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 2
            text: model.unit
        }

        EaComponents.TableViewLabel {
            id: errorColumn
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Error  "
            text: model.error === 0.0 || model.error > 999999 ? "" : model.error.toFixed(4) + "  "
        }

        EaComponents.TableViewCheckBox {
            enabled: ExGlobals.Variables.experimentLoaded
            id: useColumn
            headerText: "Fit"
            checked: model.fit
        }

    }

    onCurrentIndexChanged: storeCurrentParameter()

    // Logic

    function storeCurrentParameter() {
        if (typeof model.get(currentIndex) === "undefined")
            return
        ExGlobals.Variables.currentParameterId = model.get(currentIndex).id
        ExGlobals.Variables.currentParameterValue = model.get(currentIndex).value
    }

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameterValue(id, parseFloat(value))
    }

    function formatLabel(index, label) {
        // String label to list
        let list = label.split(".")
        const last = list.length - 1

        // Previous label to list
        let previousList = index > 0 ? fitablesModel.get(index - 1).label.split(".") : [""]

        // First element formatting
        if (list[0] === previousList[0]) {
            list[0] = `<font color=${EaStyle.Colors.themeForegroundDisabled} face="${EaStyle.Fonts.iconsFamily}">${list[0]}</font>`
        } else {
            list[0] = `<font color=${EaStyle.Colors.themeForeground} face="${EaStyle.Fonts.iconsFamily}">${list[0]}</font>`
        }
        list[0] = list[0].replace("Phases", "gem").replace("Instrument", "microscope")

        // Intermediate elements formatting (excluding first and last)
        for (let i = 1; i < last; ++i) {
            if (list[i] === previousList[i]) {
                list[i] = `<font color=${EaStyle.Colors.themeForegroundDisabled}>${list[i]}</font>`
            } else {
                list[i] = `<b>${list[i]}</b>`
            }
        }

        // Last element formatting
        list[last] = `<font color=${EaStyle.Colors.themeForegroundHovered}><b>${list[last]}</b></font>`

        // Back to string
        label = list.join("&nbsp;&nbsp;")

        return label
    }

}

