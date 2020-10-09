import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Variables.phasesCurrentIndex + 1

        xml: ExGlobals.Constants.proxy.phasesXml
        query: `/root/item[${phaseIndex}]`

        XmlRole { name: "cell_length_a"; query: "cell_length_a/number()" }
        XmlRole { name: "cell_length_b"; query: "cell_length_b/number()" }
        XmlRole { name: "cell_length_c"; query: "cell_length_c/number()" }
        XmlRole { name: "cell_angle_alpha"; query: "cell_angle_alpha/number()" }
        XmlRole { name: "cell_angle_beta"; query: "cell_angle_beta/number()" }
        XmlRole { name: "cell_angle_gamma"; query: "cell_angle_gamma/number()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewTextInput {
            id: cellLabel
            width: EaStyle.Sizes.fontPixelSize * 5.8
            headerText: "a (Å)"
            text: model.cell_length_a
        }

        EaComponents.TableViewTextInput {
            width: cellLabel.width
            headerText: "b (Å)"
            text: model.cell_length_b
        }

        EaComponents.TableViewTextInput {
            width: cellLabel.width
            headerText: "c (Å)"
            text: model.cell_length_c
        }

        EaComponents.TableViewTextInput {
            width: cellLabel.width
            headerText: "alpha (°)"
            text: model.cell_angle_alpha
        }

        EaComponents.TableViewTextInput {
            width: cellLabel.width
            headerText: "beta (°)"
            text: model.cell_angle_beta
        }

        EaComponents.TableViewTextInput {
            width: cellLabel.width
            headerText: "gamma (°)"
            text: model.cell_angle_gamma
        }

    }

}
