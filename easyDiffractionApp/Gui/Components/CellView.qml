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
        property int phaseIndex: ExGlobals.Constants.proxy.currentPhaseIndex + 1

        xml: ExGlobals.Constants.proxy.phasesAsXml
        query: `/root/item[${phaseIndex}]`

        XmlRole { name: "a"; query: "cell/length_a/value/number()" }
        XmlRole { name: "b"; query: "cell/length_b/value/number()" }
        XmlRole { name: "c"; query: "cell/length_c/value/number()" }
        XmlRole { name: "alpha"; query: "cell/angle_alpha/value/number()" }
        XmlRole { name: "beta"; query: "cell/angle_beta/value/number()" }
        XmlRole { name: "gamma"; query: "cell/angle_gamma/value/number()" }

        XmlRole { name: "aId"; query: "cell/length_a/key[4]/string()" }
        XmlRole { name: "bId"; query: "cell/length_b/key[4]/string()" }
        XmlRole { name: "cId"; query: "cell/length_c/key[4]/string()" }
        XmlRole { name: "alphaId"; query: "cell/angle_alpha/key[4]/string()" }
        XmlRole { name: "betaId"; query: "cell/angle_beta/key[4]/string()" }
        XmlRole { name: "gammaId"; query: "cell/angle_gamma/key[4]/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewTextInput {
            id: cellLabel
            width: EaStyle.Sizes.fontPixelSize * 5.8
            headerText: "a (Å)"
            text: model.a
            onEditingFinished: editParameterValue(model.aId, text)
        }

        EaComponents.TableViewTextInput {
            width: cellLabel.width
            headerText: "b (Å)"
            text: model.b
            onEditingFinished: editParameterValue(model.bId, text)
        }

        EaComponents.TableViewTextInput {
            width: cellLabel.width
            headerText: "c (Å)"
            text: model.c
            onEditingFinished: editParameterValue(model.cId, text)
        }

        EaComponents.TableViewTextInput {
            width: cellLabel.width
            headerText: "alpha (°)"
            text: model.alpha
            onEditingFinished: editParameterValue(model.alphaId, text)
        }

        EaComponents.TableViewTextInput {
            width: cellLabel.width
            headerText: "beta (°)"
            text: model.beta
            onEditingFinished: editParameterValue(model.betaId, text)
        }

        EaComponents.TableViewTextInput {
            width: cellLabel.width
            headerText: "gamma (°)"
            text: model.gamma
            onEditingFinished: editParameterValue(model.gammaId, text)
        }

    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameterValue(id, parseFloat(value))
    }

}
