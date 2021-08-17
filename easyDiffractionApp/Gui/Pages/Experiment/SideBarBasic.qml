// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

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
                spacing: EaStyle.Sizes.fontPixelSize

                Column {
                    EaElements.Label {
                        enabled: false
                        text: qsTr("Facility")
                    }

                    EaElements.ComboBox {
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
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3

                        textRole: "text"
                        valueRole: "value"

                        model: [
                            { value: "powder1DCW", text: qsTr("Constant wavelength") },
                            { value: "powder1DTOF", text: qsTr("Time-of-Flight") }
                        ]

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
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Powder"]
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
                if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCW') {
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
                if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCW') {
                    return 'SideBarGroups/InstrumentSetupPdCw1d.qml'
                } else if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DTOF') {
                    return 'SideBarGroups/InstrumentSetupPdTof1d.qml'
                }
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Peak profile")
        enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded ||
                 ExGlobals.Constants.proxy.experiment.experimentSkipped

        Loader {
            source: {
                if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCW') {
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
                if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DCW') {
                    return 'SideBarGroups/BackgroundPdCw1d.qml'
                } else if (ExGlobals.Constants.proxy.sample.experimentType === 'powder1DTOF') {
                    return 'SideBarGroups/BackgroundPdTof1d.qml'
                }
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Associated phases")
        last: true
        enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded

        ExComponents.ExperimentAssociatedPhases {}

        Component.onCompleted: ExGlobals.Variables.associatedPhasesGroup = this
    }

    // Load experimental data file dialog

    Dialogs1.FileDialog{
        id: loadExperimentDataFileDialog

        nameFilters: [ qsTr("Data files") + " (*.xye *.xys *.xy)" ]

        onAccepted: ExGlobals.Constants.proxy.experiment.addExperimentDataFromXye(fileUrl)
    }

}

