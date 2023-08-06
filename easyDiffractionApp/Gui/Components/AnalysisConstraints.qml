// SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQml.XmlListModel

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView  {
    id: table

    enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded

    maxRowCountShow: 8
    defaultInfoText: qsTr("No Constraints Added")

    // Table model

    model: XmlListModel {
        id: constraintsModel

        //xml: ExGlobals.Constants.proxy.constraintsListAsXml
        //xml: ExGlobals.Constants.proxy.fitting.constraintsAsXml

        query: "/data/data"

        // XmlListModelRole { name: "number"; query: "number/number()" }
        // XmlListModelRole { name: "dependentName"; query: "dependentName/string()" }
        // XmlListModelRole { name: "relationalOperator"; query: "relationalOperator/string()" }
        // XmlListModelRole { name: "value"; query: "value/number()" }
        // XmlListModelRole { name: "arithmeticOperator"; query: "arithmeticOperator/string()" }
        // XmlListModelRole { name: "independentName"; query: "independentName/string()" }
        // XmlListModelRole { name: "enabled"; query: "enabled/number()" }
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
            id: dependentNameColumn
            horizontalAlignment: Text.AlignLeft
            width: (table.width -
                    (parent.children.length - 1) * EaStyle.Sizes.tableColumnSpacing -
                    numberColumn.width -
                    relationalOperatorColumn.width -
                    valueColumn.width -
                    arithmeticOperatorColumn.width -
                    useColumn.width -
                    deleteRowColumn.width) / 2
            headerText: "Constraint"
            text: model.dependentName
        }

        EaComponents.TableViewLabel {
            id: relationalOperatorColumn
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 2
            font.family: EaStyle.Fonts.iconsFamily
            text: model.relationalOperator
                .replace("=", "\uf52c")
                .replace(">", "\uf531")
                .replace("<", "\uf536")
        }

        EaComponents.TableViewLabel {
            id: valueColumn
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 4
            text: model.value.toFixed(4)
        }

        EaComponents.TableViewLabel {
            id: arithmeticOperatorColumn
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 2
            font.family: EaStyle.Fonts.iconsFamily
            text: model.arithmeticOperator
                .replace("*", "\uf00d")
                .replace("/", "\uf529")
                .replace("+", "\uf067")
                .replace("-", "\uf068")
        }

        EaComponents.TableViewLabel {
            id: independentNameColumn
            horizontalAlignment: Text.AlignLeft
            width: dependentNameColumn.width
            text: model.independentName
        }

        EaComponents.TableViewCheckBox {
            id: useColumn
            width: EaStyle.Sizes.fontPixelSize * 3
            headerText: "Use"
            checked: model.enabled
            onToggled: ExGlobals.Constants.proxy.fitting.toggleConstraintByIndex(model.index, checked)
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this constraint")
            onClicked: ExGlobals.Constants.proxy.fitting.removeConstraintByIndex(model.index)
        }
    }

}
