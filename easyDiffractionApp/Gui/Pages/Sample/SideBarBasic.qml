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
        title: qsTr("Structural phases")
        collapsible: false

        ExComponents.PhasesView {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                enabled: ExGlobals.Constants.proxy.phaseList.length === 0

                fontIcon: "upload"
                text: qsTr("Set new sample from CIF")

                onClicked: {
                    loadPhaseFileDialog.open()
                }
            }

            EaElements.SideBarButton {
                enabled: ExGlobals.Constants.proxy.phaseList.length === 0

                fontIcon: "plus-circle"
                text: qsTr("Set new sample manually")

                onClicked: {
                    ExGlobals.Constants.proxy.addSampleManual()
                    ExGlobals.Variables.experimentPageEnabled = true
                    ExGlobals.Variables.sampleLoaded = true
                    ExGlobals.Variables.analysisPageEnabled = true
                }
            }
        }

    }

    EaElements.GroupBox {
        id: symmetryGroup

        title: qsTr("Symmetry and cell parameters")
        enabled: ExGlobals.Variables.sampleLoaded

        Column {
            ExComponents.SymmetryView {}
            ExComponents.CellView { titleText: "Cell parameters" }
        }

    }

    EaElements.GroupBox {
        title: qsTr("Atoms, atomic coordinates and occupations")
        enabled: ExGlobals.Variables.sampleLoaded

        ExComponents.AtomsView {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                fontIcon: "plus-circle"
                text: qsTr("Append new atom")

                onClicked: {
                    ExGlobals.Constants.proxy.addAtom()
                }
            }

            EaElements.SideBarButton {
                enabled: false
                fontIcon: "clone"
                text: qsTr("Duplicate selected atom")
            }

        }
    }

    EaElements.GroupBox {
        title: qsTr("Atomic displacement parameters")
        enabled: ExGlobals.Variables.sampleLoaded

        ExComponents.AdpsView {}
    }

    // Open phase CIF file dialog

    Dialogs1.FileDialog{
        id: loadPhaseFileDialog
        nameFilters: [ "CIF files (*.cif)"]
        //folder: settings.value("lastOpenedProjectFolder", examplesDirUrl)
        onAccepted: {
            //settings.setValue("lastOpenedProjectFolder", folder)
            ExGlobals.Constants.proxy.addSampleFromCif(fileUrl)
            ExGlobals.Variables.experimentPageEnabled = true
            ExGlobals.Variables.sampleLoaded = true
            ExGlobals.Variables.analysisPageEnabled = true
        }
    }

}
