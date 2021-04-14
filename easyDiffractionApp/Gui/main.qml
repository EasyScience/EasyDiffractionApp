import QtQuick 2.13
import QtQuick.Controls 2.13

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Components 1.0 as EaComponents


ExComponents.ApplicationWindow {
    id: window

    EaComponents.GuideWindowContainer {
        id: homePageGuidesContainer

        appBarCurrentIndex: EaGlobals.Variables.HomePageIndex

        EaComponents.GuideWindow {
            container: homePageGuidesContainer
            parent: ExGlobals.Variables.aboutButton
            text: qsTr("Click here to show about window.")
        }

        EaComponents.GuideWindow {
            container: homePageGuidesContainer
            parent: ExGlobals.Variables.onlineDocumentationButton
            text: qsTr("Links to the online resources.")
        }

        EaComponents.GuideWindow {
            container: homePageGuidesContainer
            parent: ExGlobals.Variables.appBarCentralTabs
            text: qsTr("Here you can see the steps in the data analysis workflow.\n\nThese buttons also allows you to easily navigate between the application pages.\n\nThe next page becomes enabled when the previous page is fully completed.")
        }

        EaComponents.GuideWindow {
            container: homePageGuidesContainer
            parent: ExGlobals.Variables.startButton
            text: qsTr("Click here to start your journey to easyDiffraction!")
        }
    }

    EaComponents.GuideWindowContainer {
        id: projectPageGuidesContainer

        appBarCurrentIndex: EaGlobals.Variables.ProjectPageIndex

        EaComponents.GuideWindow {
            container: projectPageGuidesContainer
            parent: ExGlobals.Variables.openProjectButton
            text: qsTr("Click here to open existing project...")
        }

        EaComponents.GuideWindow {
            container: projectPageGuidesContainer
            parent: ExGlobals.Variables.createProjectButton
            text: qsTr("Or here to create a new one...")
        }

        EaComponents.GuideWindow {
            container: projectPageGuidesContainer
            parent: ExGlobals.Variables.loadExampleProjectButton
            text: qsTr("Or click open button here to load one of the examples.")
        }

        EaComponents.GuideWindow {
            container: projectPageGuidesContainer
            parent: ExGlobals.Variables.projectPageMainContent
            text: qsTr("Brief project details will be shown in the main area.")
        }

        EaComponents.GuideWindow {
            container: projectPageGuidesContainer
            parent: ExGlobals.Variables.sampleTabButton
            text: qsTr("Click here to go to the next page: Sample.")
        }
    }

    EaComponents.GuideWindowContainer {
        id: samplePageGuidesContainer

        appBarCurrentIndex: EaGlobals.Variables.SamplePageIndex

        EaComponents.GuideWindow {
            container: samplePageGuidesContainer
            parent: ExGlobals.Variables.structuralPhasesGroup
            text: qsTr("Here you can see labels of the structural phases.")
        }

        EaComponents.GuideWindow {
            container: samplePageGuidesContainer
            parent: ExGlobals.Variables.samplePageMainContent
            text: qsTr("Crystal structure is shown in the main area.")
        }

        EaComponents.GuideWindow {
            container: samplePageGuidesContainer
            parent: ExGlobals.Variables.phaseCifTab
            text: qsTr("This tab button allows to see the sample\ndetails as plain text (CIF).")
        }

        EaComponents.GuideWindow {
            container: samplePageGuidesContainer
            parent: ExGlobals.Variables.symmetryGroup
            text: qsTr("The sidebar groups contain details related to the sample model.\n\nClick on the group name to unfold the group.")
        }

        EaComponents.GuideWindow {
            container: samplePageGuidesContainer
            parent: ExGlobals.Variables.experimentTabButton
            text: qsTr("Click here to go to the next page: Experiment.")
        }
    }

    EaComponents.GuideWindowContainer {
        id: experimentPageGuidesContainer

        appBarCurrentIndex: EaGlobals.Variables.ExperimentPageIndex

        EaComponents.GuideWindow {
            container: experimentPageGuidesContainer
            parent: ExGlobals.Variables.experimentalDataGroup
            text: qsTr("Here you can see labels of the experimental data.")
        }

        EaComponents.GuideWindow {
            container: experimentPageGuidesContainer
            parent: ExGlobals.Variables.experimentPageMainContent
            text: qsTr("Measured data points are plotted in the main area.")
        }

        EaComponents.GuideWindow {
            container: experimentPageGuidesContainer
            parent: ExGlobals.Variables.experimentTableTab
            text: qsTr("This tab button switches to the table\nview of the measured data.")
        }

        EaComponents.GuideWindow {
            container: experimentPageGuidesContainer
            parent: ExGlobals.Variables.experimentCifTab
            text: qsTr("This tab button allows to see the\nmeasured data as plain text.")
        }

        EaComponents.GuideWindow {
            container: experimentPageGuidesContainer
            parent: ExGlobals.Variables.associatedPhases
            text: qsTr("The sidebar groups contain details related to the experiment.\n\nClick on the group name to unfold the group.")
        }

        EaComponents.GuideWindow {
            container: experimentPageGuidesContainer
            parent: ExGlobals.Variables.analysisTabButton
            text: qsTr("Click here to go to the next page: Analysis.")
        }

    }

}
