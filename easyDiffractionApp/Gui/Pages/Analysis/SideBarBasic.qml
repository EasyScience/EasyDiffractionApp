import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.XmlListModel 2.14

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
        last: true
        collapsible: false

        // Filter parameters widget
        Row {
            spacing: EaStyle.Sizes.fontPixelSize * 0.5

            EaElements.TextField {
                id: filterCriteriaField

                width: (EaStyle.Sizes.sideBarContentWidth - parent.spacing) / 2

                placeholderText: "Filter parameters"

                onTextChanged: {
                    exampleFilterCriteria.currentIndex = exampleFilterCriteria.indexOfValue(text)
                    ExGlobals.Constants.proxy.setFilterCriteria(text)
                }
            }

            EaElements.ComboBox {
                id: exampleFilterCriteria

                topInset: 0
                bottomInset: 0

                width: (EaStyle.Sizes.sideBarContentWidth - parent.spacing) / 2

                textRole: "text"
                valueRole: "value"

                displayText: currentIndex === -1 ? "Custom filter criteria" : currentText

                model: [
                    { value: "", text: formatFilterText("infinity", "All parameters") },
                    { value: "phases.", text: formatFilterText("gem", "Phases") },
                    { value: "instrument.", text: formatFilterText("microscope", "Instrument") },
                    { value: "cell.", text: formatFilterText("cube", "Cell") },
                    { value: "atoms.", text: formatFilterText("atom", "Atoms") },
                    { value: "fract_", text: formatFilterText("map-marker-alt", "Coordinates") },
                    { value: "adp.", text: formatFilterText("arrows-alt", "ADPs") },
                    { value: "resolution_", text: formatFilterText("grip-lines-vertical", "Resolution") }, //"delicious"//"grip-lines"//"flipboard"
                    { value: "background.", text: formatFilterText("wave-square", "Background") } //"water"
                ]

                onActivated: filterCriteriaField.text = currentValue
            }
        }

        // Parameters table
        ExComponents.AnalysisFitables {}

        // Parameter change slider
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

        // Start fitting button
        EaElements.SideBarButton {
            enabled: ExGlobals.Variables.experimentLoaded
            fontIcon: "play-circle"
            text: qsTr("Start fitting")

            wide: true

            onClicked: {
                print("Start fitting button clicked")
                ExGlobals.Constants.proxy.fit()
            }
        }
    }

    // Logic

    function formatFilterText(icon, text) {
        return `<font face="${EaStyle.Fonts.iconsFamily}">${icon}</font>&nbsp;&nbsp;${text}</font>`
    }

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
