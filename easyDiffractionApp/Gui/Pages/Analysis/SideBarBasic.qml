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

            Column {
                EaElements.Label {
                    visible: false
                    enabled: false
                    text: qsTr("Filter by text")
                }

                EaElements.TextField {
                    id: filterCriteriaField

                    width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3

                    placeholderText: qsTr("Filter parameters")

                    onTextChanged: {
                        exampleFilterCriteria.currentIndex = exampleFilterCriteria.indexOfValue(text)
                        namesFilterCriteria.currentIndex = namesFilterCriteria.indexOfValue(text)
                        ExGlobals.Constants.proxy.setFilterCriteria(text)
                    }
                }
            }

            Column {
                EaElements.Label {
                    visible: false
                    enabled: false
                    text: qsTr("Filter by type")
                }

                EaElements.ComboBox {
                    id: exampleFilterCriteria

                    topInset: 0
                    bottomInset: 0

                    width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3

                    textRole: "text"
                    valueRole: "value"

                    displayText: currentIndex === -1 ? qsTr("Filter by type") : currentText

                    model: [
                        { value: "", text: qsTr("All types") },
                        { value: "phases.", text: formatFilterText("gem", "", "Phases") },
                        { value: "instrument.", text: formatFilterText("microscope", "", "Instrument") },
                        { value: ".lattice.", text: formatFilterText("gem", "cube", "Cell") },
                        { value: ".atoms.", text: formatFilterText("gem", "atom", "Atoms") },
                        { value: ".fract_", text: formatFilterText("gem", "map-marker-alt", "Coordinates") },
                        { value: ".adp.", text: formatFilterText("gem", "arrows-alt", "ADPs") },
                        { value: ".resolution_", text: formatFilterText("microscope", "grip-lines-vertical", "Resolution") }, //"delicious"//"grip-lines"//"flipboard"
                        { value: ".background.", text: formatFilterText("microscope", "wave-square", "Background") } //"water"
                    ]

                    onActivated: filterCriteriaField.text = currentValue
                }
            }

            Column {
                EaElements.Label {
                    visible: false
                    enabled: false
                    text: qsTr("Filter by name")
                }

                EaElements.ComboBox {
                    id: namesFilterCriteria

                    topInset: 0
                    bottomInset: 0

                    width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3

                    textRole: "text"
                    valueRole: "value"

                    displayText: currentIndex === -1 ? qsTr("Filter by name") : currentText

                    model: {
                        if (typeof ExGlobals.Constants.proxy.phaseList === 'undefined' || typeof ExGlobals.Constants.proxy.phaseList[0] === 'undefined' ) {
                            return []
                        }
                        const phase_name = ExGlobals.Constants.proxy.phaseList[0].name
                        let m = [
                                { value: "", text: qsTr("All names") },
                                { value: `.${phase_name}.`, text: formatFilterText("gem", "", phase_name) },
                                { value: ".D1A@ILL.", text: formatFilterText("microscope", "", "D1A@ILL") },
                                ]
                        for (let i in ExGlobals.Constants.proxy.phaseList[0].atoms.data) {
                            const atom_label = ExGlobals.Constants.proxy.phaseList[0].atoms.data[i].label.value
                            m.push({ value: `.${atom_label}.`, text: formatFilterText("gem", "atom", atom_label) })
                        }
                        return m
                    }

                    onActivated: filterCriteriaField.text = currentValue
                }
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
                //print("Start fitting button clicked")
                ExGlobals.Constants.proxy.fit()
                refinementResultsDialog.open()
            }
        }
    }

    // Info dialog (after refinement)

    EaElements.Dialog {
        id: refinementResultsDialog

        parent: Overlay.overlay

        x: (parent.width - width) * 0.5
        y: (parent.height - height) * 0.5

        modal: true
        standardButtons: Dialog.Ok

        title: "Refinement Results"

        Column {
            EaElements.Label { text: typeof ExGlobals.Constants.proxy.fitResults !== 'undefined' ? `Success: ${ExGlobals.Constants.proxy.fitResults.success}` : "" }
            EaElements.Label { text: typeof ExGlobals.Constants.proxy.fitResults !== 'undefined' && typeof ExGlobals.Constants.proxy.fitResults.redchi !== 'undefined' ? `Goodness-of-fit (\u03c7\u00b2): ${ExGlobals.Constants.proxy.fitResults.redchi.toFixed(2)}` : "" }
            EaElements.Label { text: typeof ExGlobals.Constants.proxy.fitResults !== 'undefined' ? `Num. refined parameters: ${ExGlobals.Constants.proxy.fitResults.nvarys}` : "" }
        }
    }

    // Logic

    function formatFilterText(group_icon, icon, text) {
        if (icon === "")
            return `<font face="${EaStyle.Fonts.iconsFamily}">${group_icon}</font>&nbsp;&nbsp;${text}</font>`
        return `<font face="${EaStyle.Fonts.iconsFamily}">${group_icon}</font>&nbsp;&nbsp;<font face="${EaStyle.Fonts.iconsFamily}">${icon}</font>&nbsp;&nbsp;${text}</font>`
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
