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
        last: true
        collapsible: false

        // Filter buttons
        Row {
            spacing: EaStyle.Sizes.fontPixelSize * 0.5

            EaElements.SideBarButton {
                smallIcon: true
                width: EaStyle.Sizes.fontPixelSize * 5.5
                fontIcon: "gem"
                text: "Phase"
                down: filterCriteriaField.text == "phases."
                onClicked: filterCriteriaField.text = "phases."
            }

            EaElements.SideBarButton {
                smallIcon: true
                width: EaStyle.Sizes.fontPixelSize * 7.5
                fontIcon: "microscope"
                text: "Instrument"
                down: filterCriteriaField.text == "instrument."
                onClicked: filterCriteriaField.text = "instrument."
            }

            EaElements.SideBarButton {
                smallIcon: true
                width: EaStyle.Sizes.fontPixelSize * 4.5
                fontIcon: "cube"
                text: "Cell"
                down: filterCriteriaField.text == "cell."
                onClicked: filterCriteriaField.text = "cell."
            }

            EaElements.SideBarButton {
                smallIcon: true
                width: EaStyle.Sizes.fontPixelSize * 5
                fontIcon: "atom"
                text: "Atom"
                down: filterCriteriaField.text == "atoms."
                onClicked: filterCriteriaField.text = "atoms."
            }

            EaElements.SideBarButton {
                smallIcon: true
                width: EaStyle.Sizes.fontPixelSize * 7.5
                fontIcon: "map-marker-alt"
                text: "Coordinate"
                down: filterCriteriaField.text == "fract_"
                onClicked: filterCriteriaField.text = "fract_"
            }

            EaElements.SideBarButton {
                smallIcon: true
                width: EaStyle.Sizes.fontPixelSize * 5
                fontIcon: "arrows-alt"
                text: "ADP"
                down: filterCriteriaField.text == "adp."
                onClicked: filterCriteriaField.text = "adp."
            }
        }

        // Filter text field
        Row {
            spacing: EaStyle.Sizes.fontPixelSize * 0.5


            EaElements.TextField {
                id: filterCriteriaField
                width: EaStyle.Sizes.sideBarContentWidth
                       - parent.spacing
                       - resetFilterButton.width
                placeholderText: "Specify your filter criteria"
                onTextChanged: ExGlobals.Constants.proxy.setFilterCriteria(text)
            }

            EaComponents.TableViewButton {
                id: resetFilterButton
                smallIcon: true
                inset: 0
                y: 0
                height: filterCriteriaField.height
                width: EaStyle.Sizes.fontPixelSize * 5
                text: "All"
                ToolTip.text: qsTr("Reset filtering")
                fontIcon: "infinity"
                down: filterCriteriaField.text == ""
                onClicked: filterCriteriaField.text = ""
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
