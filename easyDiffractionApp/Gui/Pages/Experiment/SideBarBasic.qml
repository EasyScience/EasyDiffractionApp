import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Dialogs 1.3 as Dialogs1

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Experimental data")
        collapsible: false

        ExComponents.ExperimentDataExplorer {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                enabled: !ExGlobals.Variables.experimentLoaded

                fontIcon: "upload"
                text: qsTr("Import data from local drive")

                onClicked: loadExperimentDataFileDialog.open()
            }

            EaElements.SideBarButton {
                id: continueWithoutExperimentDataButton

                enabled: !ExGlobals.Variables.experimentLoaded && !ExGlobals.Variables.experimentSkipped

                fontIcon: "chevron-circle-right"
                text: qsTr("Continue without experiment data")

                onClicked: {
                    ExGlobals.Variables.analysisPageEnabled = true

                    ExGlobals.Variables.experimentSkipped = true
                    ExGlobals.Constants.proxy.experimentSkipped = true
                }

                Component.onCompleted: ExGlobals.Variables.continueWithoutExperimentDataButton = continueWithoutExperimentDataButton
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Associated phases")
        enabled: ExGlobals.Variables.experimentLoaded

        ExComponents.ExperimentAssociatedPhases {}
    }

    EaElements.GroupBox {
        title: qsTr("Simulation range")
        enabled: ExGlobals.Variables.experimentLoaded || ExGlobals.Variables.experimentSkipped

        ExComponents.ExperimentSimulationSetup {}
    }

    EaElements.GroupBox {
        title: qsTr("Instrument setup")
        enabled: ExGlobals.Variables.experimentLoaded || ExGlobals.Variables.experimentSkipped

        ExComponents.ExperimentInstrumentSetup {}
    }

    EaElements.GroupBox {
        title: qsTr("Peak profile")
        enabled: ExGlobals.Variables.experimentLoaded || ExGlobals.Variables.experimentSkipped

        Column {

            Column {
                spacing: EaStyle.Sizes.fontPixelSize * -0.5

                EaElements.Label {
                    enabled: false
                    text: qsTr("Instrument resolution function")
                }

                EaElements.ComboBox {
                    width: EaStyle.Sizes.sideBarContentWidth
                    model: ["Pseudo-Voigt"]
                }
            }

            Column {
                EaElements.Label {
                    enabled: false
                    text: qsTr("Profile parameters")
                }

                ExComponents.ExperimentPeakProfile {}
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Background")
        last: true
        enabled: ExGlobals.Variables.experimentLoaded || ExGlobals.Variables.experimentSkipped

        ExComponents.ExperimentBackground {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                fontIcon: "plus-circle"
                text: qsTr("Append new point")
                onClicked: ExGlobals.Constants.proxy.addBackgroundPoint()
            }

            EaElements.SideBarButton {
                enabled: false
                fontIcon: "plus-square"
                text: qsTr("Insert point before selected")
            }
        }
    }

    // Load experimental data file dialog

    Dialogs1.FileDialog{
        id: loadExperimentDataFileDialog

        nameFilters: [ qsTr("Data files") + " (*.xye *.xys *.xy)" ]

        onAccepted: {
            ExGlobals.Variables.analysisPageEnabled = true

            ExGlobals.Variables.experimentSkipped = false
            ExGlobals.Constants.proxy.experimentSkipped = false

            ExGlobals.Variables.experimentLoaded = true
            ExGlobals.Constants.proxy.experimentLoaded = true

            ExGlobals.Constants.proxy.addExperimentDataFromXye(fileUrl)
        }
    }

}

