// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Dialogs 1.3 as Dialogs1

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Logic 1.0 as ExLogic
import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Experimental data")
        collapsible: false
        enabled: ExGlobals.Constants.proxy.fitting.isFitFinished

        ExComponents.ExperimentDataExplorer {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded

                fontIcon: "upload"
                text: qsTr("Import data from local drive")

                onClicked: loadExperimentDataFileDialog.open()
            }

            EaElements.SideBarButton {
                enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded &&
                         !ExGlobals.Constants.proxy.experiment.experimentSkipped

                fontIcon: "arrow-circle-right"
                text: qsTr("Continue without experiment data")

                onClicked: ExGlobals.Constants.proxy.experiment.experimentSkipped = true

                Component.onCompleted: ExGlobals.Variables.continueWithoutExperimentDataButton = this
            }
        }

        Component.onCompleted: ExGlobals.Variables.experimentalDataGroup = this
    }

    EaElements.GroupBox {
        title: qsTr("Instrument and experiment type")
        enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded ||
                 ExGlobals.Constants.proxy.experiment.experimentSkipped

        Column {
            spacing: EaStyle.Sizes.fontPixelSize * 0.5

            Row {
                visible: false
                spacing: EaStyle.Sizes.fontPixelSize

                Column {
                    EaElements.Label {
                        enabled: false
                        text: qsTr("Facility")
                    }

                    EaElements.ComboBox {
                        enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Unknown"]
                    }
                }

                Column {
                    EaElements.Label {
                        enabled: false
                        text: qsTr("Instrument")
                    }

                    EaElements.ComboBox {
                        enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Unknown"]
                    }
                }

                Column {
                    EaElements.Label {
                        enabled: false
                        text: qsTr("Configuration")
                    }

                    EaElements.ComboBox {
                        enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Unknown"]
                    }
                }
            }

            Row {
                spacing: EaStyle.Sizes.fontPixelSize

                Column {
                    EaElements.Label {
                        enabled: false
                        text: qsTr("Radiation")
                    }

                    EaElements.ComboBox {
                        enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Neutron"]
                    }
                }

                Column {
                    EaElements.Label {
                        enabled: false
                        text: qsTr("Mode")
                    }

                    EaElements.ComboBox {
                        property string experimentType: ExGlobals.Constants.proxy.sample.experimentType

                        enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3

                        textRole: "text"
                        valueRole: "value"

                        model: [
                            { value: "powder1DCW", text: qsTr("Constant wavelength") },
                            { value: "powder1DTOF", text: qsTr("Time-of-Flight") }
                        ]

                        onExperimentTypeChanged: {
                            if (experimentType === "powder1DCW") {
                                currentIndex = 0
                            } else if (experimentType === "powder1DTOF") {
                                currentIndex = 1
                            }
                        }

                        onActivated: {
                            ExGlobals.Constants.proxy.sample.experimentType = currentValue
                        }
                    }
                }

                Column {
                    EaElements.Label {
                        enabled: false
                        text: qsTr("Method")
                    }

                    EaElements.ComboBox {
                        enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Powder"]
                    }
                }
            }
            Row {
                visible: true
                spacing: EaStyle.Sizes.fontPixelSize

                Column {
                    EaElements.Label {
                        enabled: false
                        text: qsTr("Polarization")
                    }

                    EaElements.ComboBox {
                        property bool experimentType: ExGlobals.Constants.proxy.experiment.isSpinPolarized
                        enabled: !ExGlobals.Constants.proxy.experiment.experimentLoaded
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3

                        textRole: "text"
                        valueRole: "value"

                        model: [
                            { value: false, text: qsTr("Unpolarized") },
                            { value: true, text: qsTr("Polarized") }
                        ]

                        onExperimentTypeChanged: {
                            if (experimentType === false) {
                                currentIndex = 0
                            } else if (experimentType === true) {
                                currentIndex = 1
                            }
                        }

                        onActivated: {
                            ExGlobals.Constants.proxy.experiment.setSpinPolarization(currentValue)
                        }
                    }
                }
            }
        }
    }


    EaElements.GroupBox {
        title: ExGlobals.Constants.proxy.experiment.experimentLoaded ?
                   qsTr("Measured range") :
                   qsTr("Simulation range")
        enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded ||
                 ExGlobals.Constants.proxy.experiment.experimentSkipped

        Loader {
            source: {
                if ((ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCW') || (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCWpol')) {
                    return 'SideBarGroups/RangesPdCw1d.qml'
                } else if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DTOF') {
                    return 'SideBarGroups/RangesPdTof1d.qml'
                }
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Instrument setup")
        enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded ||
                 ExGlobals.Constants.proxy.experiment.experimentSkipped

        Loader {
            source: {
                if ((ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCW') || (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCWpol')) {
                    return 'SideBarGroups/InstrumentSetupPdCw1d.qml'
                } else if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DTOF') {
                    return 'SideBarGroups/InstrumentSetupPdTof1d.qml'
                }
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Diffraction radiation")
        visible: ExGlobals.Constants.proxy.experiment.isSpinPolarized
        enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded ||
                 ExGlobals.Constants.proxy.experiment.experimentSkipped

        Loader {
            source: {
                    return 'SideBarGroups/DiffractionRadiation.qml'
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Peak profile")
        enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded ||
                 ExGlobals.Constants.proxy.experiment.experimentSkipped

        Loader {
            source: {
                if ((ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCW') || (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCWpol')) {
                    return 'SideBarGroups/PeakProfilePdCw1d.qml'
                } else if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DTOF') {
                    return 'SideBarGroups/PeakProfilePdTof1d.qml'
                }
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Background")
        enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded ||
                 ExGlobals.Constants.proxy.experiment.experimentSkipped

        Loader {
            source: {
                if ((ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCW') || (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCWpol')) {
                    return 'SideBarGroups/BackgroundPdCw1d.qml'
                } else if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DTOF') {
                    return 'SideBarGroups/BackgroundPdTof1d.qml'
                }
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Associated phases")
        enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded ||
                 ExGlobals.Constants.proxy.experiment.experimentSkipped

        ExComponents.ExperimentAssociatedPhases {}

        Component.onCompleted: ExGlobals.Variables.associatedPhasesGroup = this
    }

    EaElements.GroupBox {
        title: qsTr("Refinement")
        last: true
        visible: false
        // visible: ExGlobals.Constants.proxy.experiment.isSpinPolarized
        enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded ||
                 ExGlobals.Constants.proxy.experiment.experimentSkipped

        Loader {
            source: {
                    return 'SideBarGroups/Refinement.qml'
            }
        }

        Component.onCompleted: ExGlobals.Variables.associatedPhasesGroup = this
    }

    // Load experimental data file dialog

    Dialogs1.FileDialog {
        id: loadExperimentDataFileDialog

        nameFilters: [ qsTr("CIF files (*.cif)"), qsTr("Data files (*.xye *.xys *.xy)") ]

        onAccepted: ExGlobals.Constants.proxy.experiment.addExperimentData(fileUrl)
    }

    // Logic

    function indexOf(model, item) {
        for (let i in model) {
            if (model[i] === item) {
                return parseInt(i)
            }
        }
        return -1
    }
}

