import QtQuick 2.13
import QtQuick.Controls 2.13
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
                fontIcon: "upload"
                text: qsTr("Import new sample from CIF")

                onClicked: {
                    loadPhaseFileDialog.open()
                }
            }

            EaElements.SideBarButton {
                fontIcon: "plus-circle"
                text: qsTr("Add new sample manually")
            }
        }

    }

    EaElements.GroupBox {
        id: symmetryGroup

        property string crystalSystem: ""//ExGlobals.Constants.proxy.phasesDict[ExGlobals.Variables.phasesCurrentIndex].crystal_system
        property string spaceGroupName: ExGlobals.Constants.proxy.phases2Dict[ExGlobals.Variables.phasesCurrentIndex].spacegroup._space_group_HM_name.value
        property string spaceGroupSetting: ""//ExGlobals.Constants.proxy.phasesDict[ExGlobals.Variables.phasesCurrentIndex].space_group_setting

        title: qsTr("Symmetry and cell parameters")
        enabled: ExGlobals.Variables.sampleLoaded

        Column {

            Row {
                spacing: EaStyle.Sizes.fontPixelSize

                Column {
                    spacing: EaStyle.Sizes.fontPixelSize * -0.5
                    EaElements.Label {
                        enabled: false
                        text: "Crystal system"
                    }
                    EaElements.ComboBox {
                        width: EaStyle.Sizes.sideBarContentWidth / 3 - EaStyle.Sizes.fontPixelSize / 3 * 2
                        model: [symmetryGroup.crystalSystem]
                    }
                }

                Column {
                    spacing: EaStyle.Sizes.fontPixelSize * -0.5
                    EaElements.Label {
                        enabled: false
                        text: "Space group"
                    }
                    EaElements.ComboBox {
                        width: EaStyle.Sizes.sideBarContentWidth / 3 - EaStyle.Sizes.fontPixelSize / 3 * 2
                        model: [symmetryGroup.spaceGroupName]
                    }
                }

                Column {
                    spacing: EaStyle.Sizes.fontPixelSize * -0.5
                    EaElements.Label {
                        enabled: false
                        text: "Setting"
                    }
                    EaElements.ComboBox {
                        width: EaStyle.Sizes.sideBarContentWidth / 3 - EaStyle.Sizes.fontPixelSize / 3 * 2
                        model: [symmetryGroup.spaceGroupSetting]
                    }
                }
            }

            ExComponents.CellView { titleText: "Cell parameters" }

        }

    }

    EaElements.GroupBox {
        title: qsTr("Atoms, atomic coordinates and occupations")
        enabled: ExGlobals.Variables.sampleLoaded

        ExComponents.AtomsView {}
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
            //print(EaLogic.Utils.prettyJson(ExGlobals.Constants.proxy.phases2Dict))
            //loadPhaseFileDialog.close()
        }
    }

}
