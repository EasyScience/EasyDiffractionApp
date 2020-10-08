import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals


import QtQuick.Dialogs 1.0


import QtQuick.XmlListModel 2.13
import easyAppGui.Logic 1.0 as EaLogic


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Structural phases")
        collapsible: false

        EaComponents.TableView {
            id: phasesTable
            defaultLabelText: qsTr("No Samples Added/Loaded")

            model: XmlListModel {
                id: phasesModel

                xml: ExGlobals.Variables.sampleLoaded ? ExGlobals.Constants.proxy.phasesXml : ""
                query: "/root/item"

                XmlRole { name: "label"; query: "label/string()" }
                XmlRole { name: "color"; query: "color/string()" }

                //onXmlChanged: print(xml)
            }
            delegate: EaComponents.TableViewDelegate {
                property string modelColor: model.color

                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 2.5
                    headerText: "No."
                    text: model.index + 1
                }
                EaComponents.TableViewLabel {
                    horizontalAlignment: Text.AlignLeft
                    width: EaStyle.Sizes.fontPixelSize * 27.9
                    headerText: "Label"
                    text: model.label
                }
                /*
                EaComponents.TableViewComboBox {
                    width: 130
                    //displayText: ""
                    //backgroundColor: modelColor
                    foregroundColor: modelColor
                    currentIndex: model.indexOf(modelColor)
                    headerText: "Color"
                    model: ["coral", "darkolivegreen", "steelblue"]
                    onActivated: ExGlobals.Constants.proxy.editPhase(phasesTable.currentIndex,
                                                                     "color",
                                                                     currentText)
                }
                */
                EaComponents.TableViewLabel {
                    headerText: "Color"
                    backgroundColor: model.color
                }

                EaComponents.TableViewButton {
                    id: deleteRowColumn
                    headerText: "Del." //"\uf2ed"
                    fontIcon: "minus-circle"
                    ToolTip.text: qsTr("Remove this phase")
                }
            }
            onCurrentIndexChanged: ExGlobals.Variables.phasesCurrentIndex = currentIndex
            Component.onCompleted: ExGlobals.Variables.phasesTable = phasesTable
        }

        Row {
            spacing: 14

            EaElements.SideBarButton {
                width: 256

                id: importNewSampleButton
                //enabled: !ExGlobals.Variables.sampleLoaded
                fontIcon: "upload"
                text: qsTr("Import new sample from CIF")

                onClicked: {
                    ExGlobals.Variables.experimentPageEnabled = true
                    ExGlobals.Variables.sampleLoaded = true
                }
                Component.onCompleted: ExGlobals.Variables.addNewSampleButton = addNewSampleButton
            }

            EaElements.SideBarButton {
                width: 256

                id: addNewSampleButton
                //enabled: !ExGlobals.Variables.sampleLoaded
                fontIcon: "plus-circle"
                text: qsTr("Add new sample manually")

                onClicked: {
                    ExGlobals.Variables.experimentPageEnabled = true
                    ExGlobals.Variables.sampleLoaded = true
                }
                //Component.onCompleted: ExGlobals.Variables.addNewSampleButton = addNewSampleButton
            }
        }


    }


    EaElements.GroupBox {
        id: symmetryGroup

        property string crystalSystem: ExGlobals.Constants.proxy.phasesDict[ExGlobals.Variables.phasesCurrentIndex].crystal_system
        property string spaceGroupName: ExGlobals.Constants.proxy.phasesDict[ExGlobals.Variables.phasesCurrentIndex].space_group_name
        property string spaceGroupSetting: ExGlobals.Constants.proxy.phasesDict[ExGlobals.Variables.phasesCurrentIndex].space_group_setting

        title: qsTr("Symmetry and cell parameters")
        enabled: ExGlobals.Variables.sampleLoaded

        //onEnabledChanged: print(JSON.stringify(ExGlobals.Constants.proxy.phasesDict))

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
                        width: 166
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
                        width: 166
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
                        width: 166
                        model: [symmetryGroup.spaceGroupSetting]
                    }
                }

            }




            Column {

                EaElements.Label {
                    enabled: false
                    text: "Cell parameters"
                }

                EaComponents.TableView {
                    model: XmlListModel {

                        xml: ExGlobals.Constants.proxy.phasesXml
                        query: `/root/item[${phasesTable.currentIndex + 1}]`

                        XmlRole { name: "cell_length_a"; query: "cell_length_a/number()" }
                        XmlRole { name: "cell_length_b"; query: "cell_length_b/number()" }
                        XmlRole { name: "cell_length_c"; query: "cell_length_c/number()" }
                        XmlRole { name: "cell_angle_alpha"; query: "cell_angle_alpha/number()" }
                        XmlRole { name: "cell_angle_beta"; query: "cell_angle_beta/number()" }
                        XmlRole { name: "cell_angle_gamma"; query: "cell_angle_gamma/number()" }
                    }

                    delegate: EaComponents.TableViewDelegate {

                        EaComponents.TableViewTextInput {
                            id: cellLabel
                            width: EaStyle.Sizes.fontPixelSize * 5.8
                            headerText: "a (Å)"
                            text: model.cell_length_a
                        }

                        EaComponents.TableViewTextInput {
                            width: cellLabel.width
                            headerText: "b (Å)"
                            text: model.cell_length_b
                        }

                        EaComponents.TableViewTextInput {
                            width: cellLabel.width
                            headerText: "c (Å)"
                            text: model.cell_length_c
                        }

                        EaComponents.TableViewTextInput {
                            width: cellLabel.width
                            headerText: "alpha (°)"
                            text: model.cell_angle_alpha
                        }

                        EaComponents.TableViewTextInput {
                            width: cellLabel.width
                            headerText: "beta (°)"
                            text: model.cell_angle_beta
                        }

                        EaComponents.TableViewTextInput {
                            width: cellLabel.width
                            headerText: "gamma (°)"
                            text: model.cell_angle_gamma
                        }
                    }
                    onCurrentIndexChanged: ExGlobals.Variables.parametersCurrentIndex = currentIndex
                }


            }


        }







    }





    EaElements.GroupBox {
        id: sampleParametersGroup
        title: qsTr("Atoms, atomic coordinates and occupations")
        enabled: ExGlobals.Variables.sampleLoaded

        Component.onCompleted: ExGlobals.Variables.sampleParametersGroup = sampleParametersGroup

        EaComponents.TableView {
            id: parametersTable

            maxRowCountShow: 3

            model: XmlListModel {
                xml: ExGlobals.Constants.proxy.phasesXml
                query: `/root/item[${phasesTable.currentIndex + 1}]/atoms/item`

                XmlRole { name: "label"; query: "label/string()" }
                XmlRole { name: "type"; query: "type/string()" }
                XmlRole { name: "color"; query: "color/string()" }
                XmlRole { name: "x"; query: "x/number()" }
                XmlRole { name: "y"; query: "y/number()" }
                XmlRole { name: "z"; query: "z/number()" }
                XmlRole { name: "occupancy"; query: "occupancy/number()" }
            }
            delegate: EaComponents.TableViewDelegate {
                property string modelType: model.type

                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 2.5
                    headerText: "No."
                    text: model.index + 1
                }

                EaComponents.TableViewTextInput {
                    id: atomLabel
                    horizontalAlignment: Text.AlignLeft
                    width: EaStyle.Sizes.fontPixelSize * 4.22
                    headerText: "Label"
                    text: model.label
                }

                EaComponents.TableViewComboBox {
                    width: atomLabel.width
                    currentIndex: model.indexOf(modelType)
                    headerText: "Atom"
                    model: ["Mn", "Fe", "Co", "Ni", "Cu", "Si", "O"]
                }

                EaComponents.TableViewLabel {
                    headerText: "Color"
                    backgroundColor: model.color
                }

                EaComponents.TableViewTextInput {
                    width: atomLabel.width
                    headerText: "x"
                    text: model.x
                }

                EaComponents.TableViewTextInput {
                    width: atomLabel.width
                    headerText: "y"
                    text: model.y
                }

                EaComponents.TableViewTextInput {
                    width: atomLabel.width
                    headerText: "z"
                    text: model.z
                }

                EaComponents.TableViewTextInput {
                    width: atomLabel.width
                    headerText: "Occupancy"
                    text: model.occupancy
                }

                EaComponents.TableViewButton {
                    id: deleteRowColumn
                    headerText: "Del." //"\uf2ed"
                    fontIcon: "minus-circle"
                    ToolTip.text: qsTr("Remove this atom")
                    onClicked: ExGlobals.Constants.proxy.removeConstraintByIndex(model.index)
                }
            }
            onCurrentIndexChanged: ExGlobals.Variables.parametersCurrentIndex = currentIndex
            Component.onCompleted: ExGlobals.Variables.parametersTable = parametersTable
        }
    }

    EaElements.GroupBox {
        title: qsTr("Atomic displacement parameters")
        enabled: ExGlobals.Variables.sampleLoaded

        EaComponents.TableView {
            maxRowCountShow: 3

            model: XmlListModel {
                xml: ExGlobals.Constants.proxy.phasesXml
                query: `/root/item[${phasesTable.currentIndex + 1}]/atoms/item`
                XmlRole { name: "label"; query: "label/string()" }
                XmlRole { name: "adp_type"; query: "adp_type/string()" }
                XmlRole { name: "adp_iso"; query: "adp_iso/number()" }
                XmlRole { name: "adp_ani_11"; query: "adp_ani_11/number()" }
                XmlRole { name: "adp_ani_22"; query: "adp_ani_22/number()" }
                XmlRole { name: "adp_ani_33"; query: "adp_ani_33/number()" }
                XmlRole { name: "adp_ani_12"; query: "adp_ani_12/number()" }
                XmlRole { name: "adp_ani_13"; query: "adp_ani_13/number()" }
                XmlRole { name: "adp_ani_23"; query: "adp_ani_23/number()" }

                //onXmlChanged: print(xml)
            }
            delegate: EaComponents.TableViewDelegate {
                property string modelAdpType: model.adp_type

                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 2.5
                    headerText: "No."
                    text: model.index + 1
                }

                EaComponents.TableViewLabel {
                    id: adpAtomLabel
                    horizontalAlignment: Text.AlignLeft
                    width: EaStyle.Sizes.fontPixelSize * 3.8
                    headerText: "Label"
                    text: model.label
                }

                EaComponents.TableViewComboBox {
                    width: adpAtomLabel.width * 1.1
                    currentIndex: model.indexOf(modelAdpType)
                    headerText: "Type"
                    model: ["Uiso", "Uani", "Biso", "Bani"]
                }

                EaComponents.TableViewTextInput {
                    width: adpAtomLabel.width
                    headerText: "Uiso"
                    text: model.adp_iso
                }

                EaComponents.TableViewTextInput {
                    width: adpAtomLabel.width
                    headerText: "U11"
                }

                EaComponents.TableViewTextInput {
                    width: adpAtomLabel.width
                    headerText: "U22"
                }

                EaComponents.TableViewTextInput {
                    width: adpAtomLabel.width
                    headerText: "U33"
                }

                EaComponents.TableViewTextInput {
                    width: adpAtomLabel.width
                    headerText: "U12"
                }

                EaComponents.TableViewTextInput {
                    width: adpAtomLabel.width
                    headerText: "U13"
                }

                EaComponents.TableViewTextInput {
                    width: adpAtomLabel.width
                    headerText: "U23"
                }


            }
            onCurrentIndexChanged: ExGlobals.Variables.parametersCurrentIndex = currentIndex
        }
    }


}
