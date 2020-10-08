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
        title: qsTr("Samples")
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
                    width: 100
                    headerText: "Label"
                    text: model.label
                }
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
            }
            onCurrentIndexChanged: ExGlobals.Variables.phasesCurrentIndex = currentIndex
            Component.onCompleted: ExGlobals.Variables.phasesTable = phasesTable
        }

        EaElements.SideBarButton {
            id: addNewSampleButton
            enabled: !ExGlobals.Variables.sampleLoaded
            fontIcon: "plus-circle"
            text: qsTr("Add new sample")
            onClicked: {
                ExGlobals.Variables.experimentPageEnabled = true
                ExGlobals.Variables.sampleLoaded = true
            }
            Component.onCompleted: ExGlobals.Variables.addNewSampleButton = addNewSampleButton
        }
    }

    EaElements.GroupBox {
        id: sampleParametersGroup
        title: qsTr("Sample parameters")
        enabled: ExGlobals.Variables.sampleLoaded

        Component.onCompleted: ExGlobals.Variables.sampleParametersGroup = sampleParametersGroup

        EaComponents.TableView {
            id: parametersTable

            model: XmlListModel {
                id: parametersModel

                xml: ExGlobals.Constants.proxy.phasesXml
                query: `/root/item[${phasesTable.currentIndex + 1}]/parameters/item`
                XmlRole { name: "amplitude"; query: "amplitude/number()" }
                XmlRole { name: "period"; query: "period/number()" }
            }
            delegate: EaComponents.TableViewDelegate {
                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 2.5
                    headerText: "No."
                    text: model.index + 1
                }
                EaComponents.TableViewTextInput {
                    id: amplitudeTextInput
                    width: 100
                    headerText: "Amplitude"
                    text: model.amplitude
                    onEditingFinished: {
                        ExGlobals.Constants.proxy.editPhaseParameter(phasesTable.currentIndex,
                                                                     parametersTable.currentIndex,
                                                                     "amplitude",
                                                                     text)
                    }
                    Component.onCompleted: ExGlobals.Variables.amplitudeTextInput = amplitudeTextInput
                }
                EaComponents.TableViewTextInput {
                    id: periodTextInput
                    width: 100
                    headerText: "Period"
                    text: model.period
                    onEditingFinished: {
                        //print(parametersModel.query, parametersTable.currentIndex, model.index, "value", text)
                        ExGlobals.Constants.proxy.editPhaseParameter(phasesTable.currentIndex,
                                                                     parametersTable.currentIndex,
                                                                     "period",
                                                                     text)
                    }
                    Component.onCompleted: ExGlobals.Variables.periodTextInput = periodTextInput
                }
            }
            onCurrentIndexChanged: ExGlobals.Variables.parametersCurrentIndex = currentIndex
            Component.onCompleted: ExGlobals.Variables.parametersTable = parametersTable
        }
    }

    EaElements.GroupBox {
        //id: sampleParametersGroup
        title: qsTr("Sample parameters (old)")
        //visible: ExGlobals.Variables.experimentPageEnabled
        enabled: ExGlobals.Variables.sampleLoaded
        //collapsed: false

        //Component.onCompleted: ExGlobals.Variables.sampleParametersGroup = sampleParametersGroup

        Grid {
            columns: 4
            columnSpacing: 20
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.Label {
                text: "Amplitude"
            }

            EaElements.TextField {
                //id: amplitudeTextInput
                width: 130
                text: parseFloat(ExGlobals.Constants.proxy.amplitude).toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.amplitude = text
                //Component.onCompleted: ExGlobals.Variables.amplitudeTextInput = amplitudeTextInput
            }

            EaElements.Label {
                text: "Period"
            }

            EaElements.TextField {
                //id: periodTextInput
                width: 130
                text: parseFloat(ExGlobals.Constants.proxy.period).toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.period = text
                //Component.onCompleted: ExGlobals.Variables.periodTextInput = periodTextInput
            }
        }

        Grid {
            columns: 4
            columnSpacing: 20
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.Label {
                text: "amplitude"
            }

            EaElements.TextField {
                width: 130
                text: ExGlobals.Constants.proxy.fitablesDict.amplitude.toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.editFitableValueByName("amplitude", text)
            }

            EaElements.Label {
                text: "period"
            }

            EaElements.TextField {
                width: 130
                text: ExGlobals.Constants.proxy.fitablesDict.period.toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.editFitableValueByName("period", text)
            }
        }
    }

}
