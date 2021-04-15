import QtQuick 2.13
import QtQuick.Controls 2.13

import Gui.Globals 1.0 as ExGlobals

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Components 1.0 as EaComponents


Item {

    // Home page

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

    // Project page

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
            text: qsTr("Click here to go to the next page.")
        }
    }

    // Sample page

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
            text: qsTr("Click here to go to the next page.")
        }
    }

    // Experiment page

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
            parent: ExGlobals.Variables.associatedPhasesGroup
            text: qsTr("The sidebar groups contain details related to the experiment.\n\nClick on the group name to unfold the group.")
        }

        EaComponents.GuideWindow {
            container: experimentPageGuidesContainer
            parent: ExGlobals.Variables.analysisTabButton
            text: qsTr("Click here to go to the next page.")
        }
    }

    // Analysis page

    EaComponents.GuideWindowContainer {
        id: analysisPageGuidesContainer

        appBarCurrentIndex: EaGlobals.Variables.AnalysisPageIndex

        EaComponents.GuideWindow {
            container: analysisPageGuidesContainer
            parent: ExGlobals.Variables.parametersGroup
            text: qsTr("Here you can see all the refinable parameters.\n\nYou can change their starting values manually\nor using the slider below.")
        }

        EaComponents.GuideWindow {
            container: analysisPageGuidesContainer
            parent: ExGlobals.Variables.analysisPageMainContent
            text: qsTr("Measured data (Iobs, blue) and calculate data (Icalc, red) points\n are shown in the main area.\n\nTheir difference (Iobs-Icalc, green) is given\nin the bottom plot.\n\nVertical ticks between the plots indicate\nBragg peak positions.")
        }

        EaComponents.GuideWindow {
            container: analysisPageGuidesContainer
            parent: ExGlobals.Variables.calculationCifTab
            text: qsTr("This tab button allows to see the\ncalcualted data as plain text.")
        }

        EaComponents.GuideWindow {
            container: analysisPageGuidesContainer
            parent: ExGlobals.Variables.startFittingButton
            text: qsTr("Click here to start or stop fitting.")
        }

        EaComponents.GuideWindow {
            container: analysisPageGuidesContainer
            parent: ExGlobals.Variables.summaryTabButton
            text: qsTr("Click here to go to the next page.")
        }
    }

    // Summary page

    EaComponents.GuideWindowContainer {
        id: summaryPageGuidesContainer

        appBarCurrentIndex: EaGlobals.Variables.SummaryPageIndex

        EaComponents.GuideWindow {
            container: summaryPageGuidesContainer
            parent: ExGlobals.Variables.summaryPageMainContent
            text: qsTr("A report here includes brief project details,\nlist of fitable parameters, fitting plot and\nstructure view.")
        }

        EaComponents.GuideWindow {
            container: summaryPageGuidesContainer
            parent: ExGlobals.Variables.exportReportGroup
            text: qsTr("Here you can export the report.")
        }
    }

}
