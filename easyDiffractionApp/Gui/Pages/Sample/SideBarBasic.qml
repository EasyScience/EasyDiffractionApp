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
                fontIcon: "upload"
                text: qsTr("Import new sample from CIF")

                onClicked: {
                    loadPhaseFileDialog.open()
                }
            }

            EaElements.SideBarButton {
                enabled: true
                fontIcon: "plus-circle"
                text: qsTr("Add new sample manually")

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

        property string crystalSystem: ""//ExGlobals.Constants.proxy.phasesObj[ExGlobals.Constants.proxy.currentPhaseIndex].crystal_system
        property string spaceGroupName: typeof ExGlobals.Constants.proxy.phasesObj[ExGlobals.Constants.proxy.currentPhaseIndex] !== 'undefined'
                                            ? ExGlobals.Constants.proxy.spaceGroupSetting
                                            : "P 1"
        property string spaceGroupSystem: typeof ExGlobals.Constants.proxy.phasesObj[ExGlobals.Constants.proxy.currentPhaseIndex] !== 'undefined'
                                            ? ExGlobals.Constants.proxy.spaceGroupSystem
                                            : "triclinic"
        property var spaceGroupInt: ExGlobals.Constants.proxy.spaceGroupInt
        property string spaceGroupSetting: ""//ExGlobals.Constants.proxy.phasesObj[ExGlobals.Constants.proxy.currentPhaseIndex].space_group_setting

        //property var spaceGroups: ExGlobals.Constants.proxy.spaceGroups
        //onSpaceGroupsChanged: print(JSON.stringify(spaceGroups))

        //onSpaceGroupNameChanged: print(EaLogic.Utils.prettyJson(ExGlobals.Constants.proxy.phasesObj[ExGlobals.Constants.proxy.currentPhaseIndex]))


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
                        id: spaceGroupSystemSelect
                        width: EaStyle.Sizes.sideBarContentWidth / 3 - EaStyle.Sizes.fontPixelSize / 3 * 2
                        model: ExGlobals.Constants.proxy.spaceGroupsSystems
                        currentIndex: indexOfValue(symmetryGroup.spaceGroupSystem)
                        onActivated: ExGlobals.Constants.proxy.spaceGroupSystem = currentText
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
                        model: ExGlobals.Constants.proxy.spaceGroupsInts.display
                        currentIndex: symmetryGroup.spaceGroupInt
                        onActivated: ExGlobals.Constants.proxy.spaceGroupInt = currentIndex
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
                        model: ExGlobals.Constants.proxy.spaceGroupSettings //[symmetryGroup.spaceGroupName]

                        currentIndex: indexOfValue(symmetryGroup.spaceGroupName)
                        onCurrentIndexChanged: {print("ExGlobals.Constants.proxy.spaceGroups", JSON.stringify(ExGlobals.Constants.proxy.spaceGroupSettings))
                                                print("SG SETTING: Current Index: ", "'", symmetryGroup.spaceGroupName, "' ", currentIndex)
                                                }
                        onActivated: ExGlobals.Constants.proxy.spaceGroupSetting = currentText

                        /*
                        onModelChanged: {
                            print("ExGlobals.Constants.proxy.spaceGroups", JSON.stringify(ExGlobals.Constants.proxy.spaceGroups))
                            print("spaceGroupName", symmetryGroup.spaceGroupName)
                            print("indexOfValue(spaceGroupName)", indexOfValue(symmetryGroup.spaceGroupName))
                            print("currentIndex", currentIndex)
                        }
                        */
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
            ExGlobals.Variables.analysisPageEnabled = true
            //print(EaLogic.Utils.prettyJson(ExGlobals.Constants.proxy.phasesObj))
            //loadPhaseFileDialog.close()
        }
    }

    // Logic



}
