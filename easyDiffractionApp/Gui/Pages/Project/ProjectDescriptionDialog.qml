import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.ProjectDescriptionDialog {
    visible: EaGlobals.Variables.showProjectDescriptionDialog
    onClosed: EaGlobals.Variables.showProjectDescriptionDialog = false

    projectName: ExGlobals.Constants.proxy.projectInfoAsJson.name
    projectKeywords: ExGlobals.Constants.proxy.projectInfoAsJson.keywords

    onProjectNameChanged: ExGlobals.Constants.proxy.editProjectInfo("name", projectName)
    onProjectKeywordsChanged: ExGlobals.Constants.proxy.editProjectInfo("keywords", projectKeywords)
}
