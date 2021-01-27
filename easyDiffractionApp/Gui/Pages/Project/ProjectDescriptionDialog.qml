import QtQuick 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.ProjectDescriptionDialog {
    visible: EaGlobals.Variables.showProjectDescriptionDialog
    onClosed: EaGlobals.Variables.showProjectDescriptionDialog = false

    onProjectNameChanged: ExGlobals.Constants.proxy.editProjectInfo("name", projectName)
    onProjectShortDescriptionChanged: ExGlobals.Constants.proxy.editProjectInfo("shortDescription", projectShortDescription)
    onProjectLocationChanged: ExGlobals.Constants.proxy.editProjectInfo("location", projectLocation)

    onAccepted: print(`Not implemented yet: Create project in '${projectLocation}'`)

    Component.onCompleted: {
        projectName = ExGlobals.Constants.proxy.projectInfoAsJson.name
        projectShortDescription = ExGlobals.Constants.proxy.projectInfoAsJson.shortDescription
        projectLocation = ExGlobals.Constants.proxy.projectInfoAsJson.location
    }
}
