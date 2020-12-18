import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Pages.Home 1.0 as ExHomePage
import Gui.Pages.Project 1.0 as ExProjectPage
import Gui.Pages.Sample 1.0 as ExSamplePage
import Gui.Pages.Experiment 1.0 as ExExperimentPage
import Gui.Pages.Analysis 1.0 as ExAnalysisPage
import Gui.Pages.Summary 1.0 as ExSummaryPage

EaComponents.ApplicationWindow {

    ///////////////////
    // APPLICATION BAR
    ///////////////////

    // Left group of application bar tool buttons
    appBarLeftButtons: [

        EaElements.ToolButton {
            enabled: false
            fontIcon: "\uf0c7"
            ToolTip.text: qsTr("Save current state of the project")
        },

        EaElements.ToolButton {
            enabled: false
            //enabled: ExGlobals.Constants.proxy.canUndo()
            fontIcon: "\uf2ea"
            ToolTip.text: qsTr("Undo")
            onClicked: ExGlobals.Constants.proxy.undo()
        },

        EaElements.ToolButton {
            enabled: false
            //enabled: ExGlobals.Constants.proxy.canRedo()
            fontIcon: "\uf2f9"
            ToolTip.text: qsTr("Redo")
            onClicked: ExGlobals.Constants.proxy.redo()
        }

    ]

    // Right group of application bar tool buttons
    appBarRightButtons: [

        EaElements.ToolButton {
            id: preferencesButton
            fontIcon: "\uf013"
            ToolTip.text: qsTr("Application preferences")
            onClicked: EaGlobals.Variables.showAppPreferencesDialog = true
            Component.onCompleted: ExGlobals.Variables.preferencesButton = preferencesButton
        },

        EaElements.ToolButton {
            enabled: false
            fontIcon: "\uf059"
            ToolTip.text: qsTr("Get online help")
        },

        EaElements.ToolButton {
            enabled: false
            fontIcon: "\uf188"
            ToolTip.text: qsTr("Report a bug or issue")
        }

    ]

    // Central group of application bar tab buttons (workflow tabs)
    // Tab buttons for the pages described below
    appBarCentralTabs: [

        // Home tab
        EaElements.AppBarTabButton {
            id: homeTabButton
            enabled: ExGlobals.Variables.homePageEnabled
            fontIcon: "home"
            text: qsTr("Home")
            ToolTip.text: qsTr("Home page")
            Component.onCompleted: ExGlobals.Variables.homeTabButton = homeTabButton
        },

        // Project tab
        EaElements.AppBarTabButton {
            id: projectTabButton
            enabled: ExGlobals.Variables.projectPageEnabled
            fontIcon: "archive"
            text: qsTr("Project")
            ToolTip.text: qsTr("Project description page")
            Component.onCompleted: ExGlobals.Variables.projectTabButton = projectTabButton
        },

        // Sample tab
        EaElements.AppBarTabButton {
            id: sampleTabButton
            enabled: ExGlobals.Variables.samplePageEnabled
            fontIcon: "gem"
            text: qsTr("Sample")
            ToolTip.text: qsTr("Sample model description page")
            Component.onCompleted: ExGlobals.Variables.sampleTabButton = sampleTabButton
        },

        // Experiment tab
        EaElements.AppBarTabButton {
            id: experimentTabButton
            enabled: ExGlobals.Variables.experimentPageEnabled
            fontIcon: "microscope"
            text: qsTr("Experiment")
            ToolTip.text: qsTr("Experimental settings and data page")
            Component.onCompleted: ExGlobals.Variables.experimentTabButton = experimentTabButton
        },

        // Analysis tab
        EaElements.AppBarTabButton {
            id: analysisTabButton
            enabled: ExGlobals.Variables.analysisPageEnabled
            fontIcon: "calculator"
            text: qsTr("Analysis")
            ToolTip.text: qsTr("Simulation and fitting page")
            Component.onCompleted: ExGlobals.Variables.analysisTabButton = analysisTabButton
        },

        // Summary tab
        EaElements.AppBarTabButton {
            id: summaryTabButton
            enabled: false // ExGlobals.Variables.summaryPageEnabled
            fontIcon: "clipboard-list"
            text: qsTr("Summary")
            ToolTip.text: qsTr("Summary of the work done")
            Component.onCompleted: ExGlobals.Variables.summaryTabButton = summaryTabButton
        }

    ]

    /////////////////////////
    // MAIN CONTENT + SIDEBAR
    /////////////////////////

    // Pages for the tab buttons described above
    contentArea: [

        // Home page
        ExHomePage.MainContent {},

        // Project page
        EaComponents.ContentPage {
            defaultInfo: ExGlobals.Variables.projectCreated ? "" : qsTr("No Project Created/Opened")

            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton { text: qsTr("Description") },
                    EaElements.TabButton { text: "project.json" }
                ]

                items: [
                    ExProjectPage.MainContentDescription {},
                    ExProjectPage.MainContentTextView {}
                ]
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { text: qsTr("Advanced controls"); enabled: false }
                ]

                items: [
                    ExProjectPage.SideBarBasic {},
                    ExProjectPage.SideBarAdvanced {}
                ]
            }
        },

        // Sample page
        EaComponents.ContentPage {
            defaultInfo: ExGlobals.Variables.sampleLoaded ? "" : qsTr("No Samples Added/Loaded")

            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton { text: qsTr("Structure view") },
                    EaElements.TabButton { text: ExGlobals.Constants.proxy.projectInfoAsJson.samples }
                ]

                items: [
                    ExSamplePage.MainContentStructureView {},
                    ExSamplePage.MainContentTextView {}
                ]
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { text: qsTr("Advanced controls") }
                ]

                items: [
                    ExSamplePage.SideBarBasic {},
                    ExSamplePage.SideBarAdvanced {}
                ]
            }
        },

        // Experiment page
        EaComponents.ContentPage {
            defaultInfo: ExGlobals.Variables.experimentLoaded ? "" : qsTr("No Experiments Loaded")

            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton { text: qsTr("Plot view") },
                    EaElements.TabButton { enabled: false; text: qsTr("Table view") },
                    EaElements.TabButton { enabled: false; text: ExGlobals.Constants.proxy.projectInfoAsJson.experiments }
                ]

                items: [
                    ExExperimentPage.MainContentPlotView {},
                    ExExperimentPage.MainContentTableView {},
                    ExExperimentPage.MainContentTextView {}
                ]
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { text: qsTr("Advanced controls") }
                ]

                items: [
                    ExExperimentPage.SideBarBasic {},
                    ExExperimentPage.SideBarAdvanced {}
                ]
            }
        },

        // Analysis page
        EaComponents.ContentPage {
            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton {
                        text: ExGlobals.Variables.experimentLoaded ? qsTr("Fitting") : qsTr("Simulation")
                    },
                    EaElements.TabButton {
                        visible: ExGlobals.Variables.experimentLoaded
                        enabled: false
                        text: ExGlobals.Constants.proxy.projectInfoAsJson.calculations
                    }
                ]

                items: [
                    ExAnalysisPage.MainContentFitting {},
                    ExAnalysisPage.MainContentTextView {}
                ]
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton {
                        id: analysisBasicControlsTabButton
                        text: qsTr("Basic controls")
                        Component.onCompleted: ExGlobals.Variables.analysisBasicControlsTabButton = analysisBasicControlsTabButton
                    },
                    EaElements.TabButton {
                        id: analysisAdvancedControlsTabButton
                        text: qsTr("Advanced controls")
                        Component.onCompleted: ExGlobals.Variables.analysisAdvancedControlsTabButton = analysisAdvancedControlsTabButton
                    }
                ]

                items: [
                    ExAnalysisPage.SideBarBasic {},
                    ExAnalysisPage.SideBarAdvanced {}
                ]
            }
        },

        // Summary page
        EaComponents.ContentPage {
            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton { text: qsTr("Report") }
                ]

                items: [
                    ExSummaryPage.MainContentReport {}
                ]
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { text: qsTr("Advanced controls"); enabled: false }
                ]

                items: [
                    ExSummaryPage.SideBarBasic {},
                    ExSummaryPage.SideBarAdvanced {}
                ]
            }
        }
    ]

    /////////////
    // STATUS BAR
    /////////////

    statusBar: EaElements.StatusBar {

        model: XmlListModel {
            xml: ExGlobals.Constants.proxy.statusModelAsXml
            query: "/root/item"

            XmlRole { name: "label"; query: "label/string()" }
            XmlRole { name: "value"; query: "value/string()" }
        }
    }

}
