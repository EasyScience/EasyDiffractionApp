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
        enabled: ExGlobals.Constants.proxy.isFitFinished

        ExComponents.ExperimentDataExplorer {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                enabled: !ExGlobals.Constants.proxy.experimentLoaded

                fontIcon: "upload"
                text: qsTr("Import data from local drive")

                onClicked: loadExperimentDataFileDialog.open()
            }

            EaElements.SideBarButton {
                enabled: !ExGlobals.Constants.proxy.experimentLoaded && !ExGlobals.Constants.proxy.experimentSkipped

                fontIcon: "arrow-circle-right"
                text: qsTr("Continue without experiment data")

                onClicked: {
                    ExGlobals.Variables.analysisPageEnabled = true
                    ExGlobals.Variables.summaryPageEnabled = true
                    ExGlobals.Constants.proxy.experimentSkipped = true
                }

                Component.onCompleted: ExGlobals.Variables.continueWithoutExperimentDataButton = this
            }
        }

        Component.onCompleted: ExGlobals.Variables.experimentalDataGroup = this
    }

    EaElements.GroupBox {
        title: qsTr("Associated phases")
        enabled: ExGlobals.Constants.proxy.experimentLoaded

        ExComponents.ExperimentAssociatedPhases {}

        Component.onCompleted: ExGlobals.Variables.associatedPhasesGroup = this
    }

    EaElements.GroupBox {
        title: qsTr("Simulation range")
        enabled: ExGlobals.Constants.proxy.experimentLoaded || ExGlobals.Constants.proxy.experimentSkipped

        ExComponents.ExperimentSimulationSetup {}
    }

    EaElements.GroupBox {
        title: qsTr("Instrument setup")
        enabled: ExGlobals.Constants.proxy.experimentLoaded || ExGlobals.Constants.proxy.experimentSkipped

        ExComponents.ExperimentInstrumentSetup {}
    }

    EaElements.GroupBox {
        title: qsTr("Peak profile")
        enabled: ExGlobals.Constants.proxy.experimentLoaded || ExGlobals.Constants.proxy.experimentSkipped

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
        enabled: ExGlobals.Constants.proxy.experimentLoaded || ExGlobals.Constants.proxy.experimentSkipped

        ExComponents.ExperimentBackground {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                fontIcon: "plus-circle"
                text: qsTr("Append new point")
                onClicked: ExGlobals.Constants.proxy.backgroundProxy.addPoint()
            }

            EaElements.SideBarButton {
                fontIcon: "undo-alt"
                text: qsTr("Reset to default points")
                onClicked: ExGlobals.Constants.proxy.backgroundProxy.setDefaultPoints()
            }
        }
    }

    // Load experimental data file dialog

    Dialogs1.FileDialog{
        id: loadExperimentDataFileDialog

        nameFilters: [ qsTr("Data files") + " (*.xye *.xys *.xy)" ]

        onAccepted: {
            ExGlobals.Variables.analysisPageEnabled = true
            ExGlobals.Variables.summaryPageEnabled = true
//            ExGlobals.Constants.proxy.experimentSkipped = false
//            ExGlobals.Constants.proxy.experimentLoaded = true
            ExGlobals.Constants.proxy.addExperimentDataFromXye(fileUrl)
        }
    }

}

