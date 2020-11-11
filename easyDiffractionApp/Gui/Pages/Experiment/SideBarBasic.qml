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

                onClicked: {
                    ExGlobals.Variables.experimentLoaded = true
                    ExGlobals.Constants.proxy.updateExperimentalData()
                }
            }

            EaElements.SideBarButton {
                enabled: false

                fontIcon: "cloud-download-alt"
                text: qsTr("Import data from SciCat")
            }
        }

    }

}

