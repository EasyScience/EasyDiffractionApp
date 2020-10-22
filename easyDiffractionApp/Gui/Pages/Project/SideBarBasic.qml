import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Get started")
        collapsible: false

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                id: createProjectButton
                fontIcon: "plus-circle"
                text: qsTr("Create a new project")
                onClicked: {
                    ExGlobals.Variables.samplePageEnabled = true
                    ExGlobals.Variables.projectCreated = true
                }
                Component.onCompleted: ExGlobals.Variables.createProjectButton = createProjectButton
            }

            EaElements.SideBarButton {
                enabled: false
                fontIcon: "upload"
                text: qsTr("Open an existing project")
            }

        }
    }

    EaElements.GroupBox {
        title: qsTr("Test Group")
        visible: false
        //collapsed: false

        Grid {
            columns: 1
            columnSpacing: 20
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.Label { text: qsTr("First Parameter: 200") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Last Parameter: 300") }
        }
    }

}

