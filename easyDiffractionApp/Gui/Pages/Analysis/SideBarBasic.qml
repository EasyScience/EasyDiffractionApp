import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        id: groupBox

        title: qsTr("Parameters")
        collapsible: false

        ExComponents.AnalysisFitables {}

        // Slider
        Row {
            id: slideRow

            width: parent.width
            height: sliderFromLabel.height

            spacing: 10

            // Min edit area
            EaElements.TextField {
                id: sliderFromLabel
                readOnly: true
                width: EaStyle.Sizes.fontPixelSize * 6
                validator: DoubleValidator {}
                maximumLength: 8
                text: slider.from.toFixed(4)
                onEditingFinished: {}
            }

            // Slider
            EaElements.Slider {
                id: slider
                width: parent.width
                       - parent.spacing * 2
                       - sliderFromLabel.width
                       - sliderToLabel.width
                       - EaStyle.Sizes.fontPixelSize * 0.5
                height: parent.height
                from: min(ExGlobals.Variables.currentParameterValue)
                to: max(ExGlobals.Variables.currentParameterValue)
                value: ExGlobals.Variables.currentParameterValue
                onPressedChanged: {
                    if (!pressed) {
                        editParameterValue(ExGlobals.Variables.currentParameterId, value.toFixed(4))
                    }
                }
            }

            // Max edit area
            EaElements.TextField {
                id: sliderToLabel
                readOnly: sliderToLabel.readOnly
                width: sliderFromLabel.width
                validator: sliderFromLabel.validator
                maximumLength: sliderFromLabel.maximumLength
                text: slider.to.toFixed(4)
                onEditingFinished: {}
            }
        }
    }

    // Logic

    function min(value) {
        if (value !== 0)
            return value * 0.9
        return -0.1
    }

    function max(value) {
        if (value !== 0)
            return value * 1.1
        return 0.1
    }

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameterValue(id, parseFloat(value))
    }

}
