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
        enabled: ExGlobals.Constants.proxy.isFitFinished

        ExComponents.SamplePhasesExplorer {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                enabled: ExGlobals.Constants.proxy.phasesAsObj.length === 0

                fontIcon: "upload"
                text: qsTr("Set new phase from CIF")

                onClicked: loadPhaseFileDialog.open()
            }

            EaElements.SideBarButton {
                id: setNewSampleManuallyButton

                enabled: ExGlobals.Constants.proxy.phasesAsObj.length === 0

                fontIcon: "plus-circle"
                text: qsTr("Set new phase manually")

                onClicked: {
                    ExGlobals.Constants.proxy.addDefaultPhase()
                    ExGlobals.Variables.experimentPageEnabled = true
                    ExGlobals.Variables.sampleLoaded = true
                }

                Component.onCompleted: ExGlobals.Variables.setNewSampleManuallyButton = setNewSampleManuallyButton
            }
        }

    }

    EaElements.GroupBox {
        id: symmetryGroup

        title: qsTr("Symmetry and cell parameters")
        enabled: ExGlobals.Variables.sampleLoaded

        Column {
            ExComponents.SampleSymmetry {}
            ExComponents.SampleCell { titleText: "Cell parameters" }
        }

        Component.onCompleted: ExGlobals.Variables.symmetryGroup = symmetryGroup
    }

    EaElements.GroupBox {
        id: atomsGroup

        title: qsTr("Atoms, atomic coordinates and occupations")
        enabled: ExGlobals.Variables.sampleLoaded

        ExComponents.SampleAtoms {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                id: appendNewAtomButton

                fontIcon: "plus-circle"
                text: qsTr("Append new atom")

                onClicked: ExGlobals.Constants.proxy.addDefaultAtom()

                Component.onCompleted: ExGlobals.Variables.appendNewAtomButton = appendNewAtomButton
            }

            EaElements.SideBarButton {
                enabled: false
                fontIcon: "clone"
                text: qsTr("Duplicate selected atom")
            }

        }

        Component.onCompleted: ExGlobals.Variables.atomsGroup = atomsGroup
    }

    EaElements.GroupBox {
        id: adpsGroup

        title: qsTr("Atomic displacement parameters")
        last: true
        enabled: ExGlobals.Variables.sampleLoaded

        ExComponents.SampleAdps {}

        Component.onCompleted: ExGlobals.Variables.adpsGroup = adpsGroup
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
        }
    }

}
