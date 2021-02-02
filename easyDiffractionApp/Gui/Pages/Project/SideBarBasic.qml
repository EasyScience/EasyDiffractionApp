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
        last: true
        collapsible: false

        Grid {
            columns: 2
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                id: createProjectButton

                fontIcon: "plus-circle"
                text: qsTr("Create a new project")

                onClicked: EaGlobals.Variables.showProjectDescriptionDialog = true
                Component.onCompleted: ExGlobals.Variables.createProjectButton = createProjectButton
            }

            EaElements.SideBarButton {
                id: continueWithoutProjectButton

                fontIcon: "arrow-circle-right"
                text: qsTr("Continue without a project")

                onClicked: ExGlobals.Variables.samplePageEnabled = true
                Component.onCompleted: ExGlobals.Variables.continueWithoutProjectButton = continueWithoutProjectButton
            }

            EaElements.SideBarButton {
                enabled: false

                fontIcon: "upload"
                text: qsTr("Open an existing project")
            }

            EaElements.SideBarButton {
                enabled: false

                fontIcon: "download"
                text: qsTr("Save project as...")
            }
        }
    }

}

