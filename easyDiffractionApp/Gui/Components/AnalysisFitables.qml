// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls
import QtQml.XmlListModel

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    id: table

    maxRowCountShow: 8
    defaultInfoText: qsTr("No Parameters Found")

    // Table model

    model: XmlListModel {
        id: fitablesModel

        //xml: ExGlobals.Constants.proxy.fitablesListAsXml
        xml: ExGlobals.Constants.proxy.parameters.parametersAsXml

        query: "/root/item"

        XmlListModelRole { name: "id"; query: "id/string()" }
        XmlListModelRole { name: "number"; query: "number/number()" }
        XmlListModelRole { name: "label"; query: "label/string()" }
        XmlListModelRole { name: "iconified_label"; query: "iconified_label/string()" }
        XmlListModelRole { name: "value"; query: "value/number()" }
        XmlListModelRole { name: "unit"; query: "unit/string()" }
        XmlListModelRole { name: "error"; query: "error/number()" }
        XmlListModelRole { name: "fit"; query: "fit/number()" }

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
                   fitColumn.width
            headerText: "Label"
            text: (ExGlobals.Variables.iconifiedNames ?
                       model.iconified_label
                       .split('$TEXT_COLOR').join(EaStyle.Colors.themeForegroundMinor)
                       .split('$ICON_COLOR').join(EaStyle.Colors.isDarkTheme ? Qt.darker(EaStyle.Colors.themeForegroundMinor, 1.2) : Qt.lighter(EaStyle.Colors.themeForegroundMinor, 1.2))
                       .split('$ICONS_FAMILY').join(EaStyle.Fonts.iconsFamily) :
                       model.label)
            textFormat: ExGlobals.Variables.iconifiedNames ? Text.RichText : Text.PlainText
            elide: Text.ElideMiddle
        }

        EaComponents.TableViewTextInput {
            id: valueColumn
            enabled: ExGlobals.Constants.proxy.fitting.isFitFinished
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Value"
            text: model.value.toFixed(4)
            onEditingFinished: editParameterValue(model.id, text)

            Component.onCompleted: {
                if (model.label.endsWith('.resolution_u')) {
                    ExGlobals.Variables.fitResolutionUValue = this
                } else if (model.label.endsWith('.resolution_v')) {
                    ExGlobals.Variables.fitResolutionVValue = this
                } else if (model.label.endsWith('.resolution_w')) {
                    ExGlobals.Variables.fitResolutionWValue = this
                } else if (model.label.endsWith('.resolution_y')) {
                    ExGlobals.Variables.fitResolutionYValue = this
                }
            }
        }

        EaComponents.TableViewLabel {
            id: unitColumn
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 2
            text: model.unit
            color: EaStyle.Colors.themeForegroundMinor
        }

        EaComponents.TableViewLabel {
            id: errorColumn
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 4
            elide: Text.ElideNone
            headerText: "Error  "
            text: model.error === 0.0 || model.error > 999999 ? "" : model.error.toFixed(4)
        }

        EaComponents.TableViewCheckBox {
            id: fitColumn
            enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded && ExGlobals.Constants.proxy.fitting.isFitFinished
            headerText: "Fit"
            checked: model.fit
            onCheckedChanged: editParameterFit(model.id, checked)

            Component.onCompleted: {
                if (model.label.endsWith('.length_a'))
                    ExGlobals.Variables.fitCellACheckBox = this
                if (model.label.endsWith('.length_b'))
                    ExGlobals.Variables.fitCellBCheckBox = this
                if (model.label.endsWith('.length_c'))
                    ExGlobals.Variables.fitCellCCheckBox = this
                if (model.label.endsWith('.zero_shift'))
                    ExGlobals.Variables.fitZeroShiftCheckBox = this
                if (model.label.endsWith('.scale'))
                    ExGlobals.Variables.fitScaleCheckBox = this
                if (model.label.endsWith('.resolution_y'))
                    ExGlobals.Variables.fitResolutionYCheckBox = this
            }
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
        //ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }
    function editParameterFit(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, value)
    }

}

