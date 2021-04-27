import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Dialogs 1.3 as Dialogs1
import QtQuick.XmlListModel 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents
import Gui.Pages.Home 1.0 as ExHomePage
import Gui.Pages.Project 1.0 as ExProjectPage
import Gui.Pages.Sample 1.0 as ExSamplePage
import Gui.Pages.Experiment 1.0 as ExExperimentPage
import Gui.Pages.Analysis 1.0 as ExAnalysisPage
import Gui.Pages.Summary 1.0 as ExSummaryPage

EaComponents.ApplicationWindow {

    title: ' ' //`${ExGlobals.Constants.appName} ${ExGlobals.Constants.appVersion}`

    ///////////////////
    // APPLICATION BAR
    ///////////////////

    // Left group of application bar tool buttons
    appBarLeftButtons: [

        EaElements.ToolButton {
            enabled: ExGlobals.Constants.proxy.stateHasChanged
            highlighted: true
            fontIcon: "\uf0c7"
            ToolTip.text: qsTr("Save current state of the project")
            onClicked:  ExGlobals.Constants.proxy.saveProject()
        },

        EaElements.ToolButton {
            enabled: ExGlobals.Constants.proxy.canUndo
            fontIcon: "\uf2ea"
            ToolTip.text: qsTr("Undo: " + ExGlobals.Constants.proxy.undoText)
            onClicked: ExGlobals.Constants.proxy.undo()
        },

        EaElements.ToolButton {
            enabled: ExGlobals.Constants.proxy.canRedo
            fontIcon: "\uf2f9"
            ToolTip.text: qsTr("Redo: " + ExGlobals.Constants.proxy.redoText)
            onClicked: ExGlobals.Constants.proxy.redo()
        }

    ]

    // Right group of application bar tool buttons
    appBarRightButtons: [

        EaElements.ToolButton {
            fontIcon: "\uf013"
            ToolTip.text: qsTr("Application preferences")
            onClicked: EaGlobals.Variables.showAppPreferencesDialog = true
            Component.onCompleted: ExGlobals.Variables.preferencesButton = this
        },

        EaElements.ToolButton {
            fontIcon: "\uf059"
            ToolTip.text: qsTr("Get online help")
            onClicked: Qt.openUrlExternally(ExGlobals.Constants.appUrl)
        },

        EaElements.ToolButton {
            fontIcon: "\uf188"
            ToolTip.text: qsTr("Report a bug or issue")
            onClicked: Qt.openUrlExternally(`${ExGlobals.Constants.appUrl}/issues`)
        }

    ]

    // Central group of application bar tab buttons (workflow tabs)
    // Tab buttons for the pages described below
    appBarCentralTabs.contentData: [

        // Home tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.homePageEnabled
            fontIcon: "home"
            text: qsTr("Home")
            ToolTip.text: qsTr("Home page")
            Component.onCompleted: ExGlobals.Variables.homeTabButton = this
        },

        // Project tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.projectPageEnabled
            fontIcon: "archive"
            text: qsTr("Project")
            ToolTip.text: qsTr("Project description page")
            Component.onCompleted: ExGlobals.Variables.projectTabButton = this
        },

        // Sample tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.samplePageEnabled
            fontIcon: "gem"
            text: qsTr("Sample")
            ToolTip.text: qsTr("Sample model description page")
            Component.onCompleted: ExGlobals.Variables.sampleTabButton = this
        },

        // Experiment tab
        EaElements.AppBarTabButton {
            id: experimentTabButton
            enabled: ExGlobals.Constants.proxy.samplesPresent
            fontIcon: "microscope"
            text: qsTr("Experiment")
            ToolTip.text: qsTr("Experimental settings and data page")
            Component.onCompleted: ExGlobals.Variables.experimentTabButton = this
        },

        // Analysis tab
        EaElements.AppBarTabButton {
            id: analysisTabButton
            enabled: ExGlobals.Constants.proxy.samplesPresent &&
                     (ExGlobals.Constants.proxy.experimentSkipped || ExGlobals.Constants.proxy.experimentLoaded)
            fontIcon: "calculator"
            text: qsTr("Analysis")
            ToolTip.text: qsTr("Simulation and fitting page")
            Component.onCompleted: ExGlobals.Variables.analysisTabButton = analysisTabButton
        },

        // Summary tab
        EaElements.AppBarTabButton {
            id: summaryTabButton
            enabled: ExGlobals.Constants.proxy.samplesPresent &&
                     (ExGlobals.Constants.proxy.experimentSkipped || ExGlobals.Constants.proxy.experimentLoaded)
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
                    EaElements.TabButton { text: qsTr("Text View (CIF)") }
                ]

                items: [
                    ExProjectPage.MainContentDescription {},
                    ExProjectPage.MainContentTextView {}
                ]

                Component.onCompleted: ExGlobals.Variables.projectPageMainContent = this
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { enabled: false; text: qsTr("Advanced controls") }
                ]

                items: [
                    ExProjectPage.SideBarBasic {},
                    ExProjectPage.SideBarAdvanced {}
                ]
            }
        },

        // Sample page
        EaComponents.ContentPage {
            defaultInfo: ExGlobals.Constants.proxy.samplesPresent ? "" : qsTr("No Samples Added/Loaded")

            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton { text: qsTr("Structure view") },
                    EaElements.TabButton {
                        /*
                        text: typeof ExGlobals.Constants.proxy.phasesAsObj[ExGlobals.Constants.proxy.currentPhaseIndex] !== 'undefined' && ExGlobals.Constants.proxy.phasesAsObj.length > 0
                              ? ExGlobals.Constants.proxy.phasesAsObj[ExGlobals.Constants.proxy.currentPhaseIndex].name + '.cif'
                              : 'Unknown'
                              */
                        text: qsTr("Text view (CIF)")
                        Component.onCompleted: ExGlobals.Variables.phaseCifTab = this
                    }
                ]

                items: [
                    ExSamplePage.MainContentStructureView {},
                    ExSamplePage.MainContentTextView {}
                ]

                Component.onCompleted: ExGlobals.Variables.samplePageMainContent = this
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { enabled: false; text: qsTr("Advanced controls") }
                ]

                items: [
                    ExSamplePage.SideBarBasic {},
                    ExSamplePage.SideBarAdvanced {}
                ]
            }
        },

        // Experiment page
        EaComponents.ContentPage {
            defaultInfo: ExGlobals.Constants.proxy.experimentLoaded ? "" : qsTr("No Experiments Loaded")

            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton { text: qsTr("Plot view") },
                    EaElements.TabButton { enabled: false; text: qsTr("Table view"); Component.onCompleted: ExGlobals.Variables.experimentTableTab = this },
                    EaElements.TabButton { enabled: false; text: qsTr("Text view (CIF)"); Component.onCompleted: ExGlobals.Variables.experimentCifTab = this }
                ]

                items: [
                    ExExperimentPage.MainContentPlotView {},
                    ExExperimentPage.MainContentTableView {},
                    ExExperimentPage.MainContentTextView {}
                ]

                Component.onCompleted: ExGlobals.Variables.experimentPageMainContent = this
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { enabled: false; text: qsTr("Advanced controls") }
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
                        text: ExGlobals.Constants.proxy.experimentLoaded ? qsTr("Fitting") : qsTr("Simulation")
                    },
                    EaElements.TabButton {
                        visible: ExGlobals.Constants.proxy.experimentLoaded
                        enabled: false
                        text: 'calculations.cif' //ExGlobals.Constants.proxy.projectInfoAsJson.calculations
                        Component.onCompleted: ExGlobals.Variables.calculationCifTab = this
                    }
                ]

                items: [
                    ExAnalysisPage.MainContentFitting {},
                    ExAnalysisPage.MainContentTextView {}
                ]

                Component.onCompleted: ExGlobals.Variables.analysisPageMainContent = this
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton {
                        text: qsTr("Basic controls")
                        Component.onCompleted: ExGlobals.Variables.analysisBasicControlsTabButton = this
                    },
                    EaElements.TabButton {
                        text: qsTr("Advanced controls")
                        Component.onCompleted: ExGlobals.Variables.analysisAdvancedControlsTabButton = this
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

                Component.onCompleted: ExGlobals.Variables.summaryPageMainContent = this
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { enabled: false; text: qsTr("Advanced controls") }
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
        visible: EaGlobals.Variables.appBarCurrentIndex !== 0

        model: XmlListModel {
            xml: ExGlobals.Constants.proxy.statusModelAsXml
            query: "/root/item"

            XmlRole { name: "label"; query: "label/string()" }
            XmlRole { name: "value"; query: "value/string()" }
        }
    }

    ///////////////
    // Init dialogs
    ///////////////

    // Application dialogs (invisible at the beginning)
    ExProjectPage.ProjectDescriptionDialog {
        onAccepted: {
            ExGlobals.Variables.samplePageEnabled = true
            ExGlobals.Variables.projectCreated = true
        }
    }

    ExComponents.CloseDialog {
        id: closeDialog
    }

    ///////////////////
    // Init user guides
    ///////////////////

    ExComponents.UserGuides {}

    ////////
    // Misc
    ////////

    onClosing: {
       closeDialog.visible = ExGlobals.Constants.proxy.stateHasChanged
       close.accepted = !ExGlobals.Constants.proxy.stateHasChanged
    }

    Component.onCompleted: {
        ExGlobals.Variables.appBarCentralTabs = appBarCentralTabs
    }
}
