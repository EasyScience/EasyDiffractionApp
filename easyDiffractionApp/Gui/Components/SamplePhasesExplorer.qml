// SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    defaultInfoText: qsTr("No Samples Added/Loaded")

    // Table model

    model: XmlListModel {
        xml: ExGlobals.Constants.proxy.phase.phasesAsXml
        query: "/data/item"

        XmlRole { name: "label"; query: "name/string()" }
        //XmlRole { name: "color"; query: "color/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        //property string modelColor: model.color ? model.color : "transparent"

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 27.9
            headerText: "Label"
            text: model.label
            onEditingFinished: ExGlobals.Constants.proxy.phase.setCurrentPhaseName(text)
        }

        EaComponents.TableViewLabel {
            headerText: "Color"
            //backgroundColor: model.color ? model.color : "transparent"
            backgroundColor: EaStyle.Colors.chartForegroundsExtra[model.index] ? EaStyle.Colors.chartForegroundsExtra[model.index] : "transparent"
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this phase")
            onClicked: ExGlobals.Constants.proxy.phase.removePhase(model.label)
        }

    }

    onCurrentIndexChanged: {
        ExGlobals.Constants.proxy.phase.currentPhaseIndex = currentIndex
    }
}
