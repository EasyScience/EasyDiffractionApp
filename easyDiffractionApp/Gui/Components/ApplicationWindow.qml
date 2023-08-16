// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Animations as EaAnimations
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals
import Gui.Components as Components


EaComponents.ApplicationWindow {

    appName: Globals.Configs.appConfig.name
    appVersion: Globals.Configs.appConfig.version
    appDate: Globals.Configs.appConfig.date

    //opacity: Globals.Vars.splashScreenAnimoFinished ? 1 : 0
    //Behavior on opacity { EaAnimations.ThemeChange {} }

    onClosing: Qt.quit()

    Component.onCompleted: {
        console.debug(`Application window loaded: ${this}`)
        Globals.Vars.applicationWindowCreated = true
    }
    Component.onDestruction: console.debug(`Application window destroyed: ${this}`)

    ///////////////////
    // APPLICATION BAR
    ///////////////////

    // Left group of application bar tool buttons
    appBarLeftButtons: [

        EaElements.ToolButton {
            enabled: Globals.Proxies.main.project.created &&
                    Globals.Proxies.main.project.needSave
            highlighted: true
            fontIcon: 'save'
            ToolTip.text: qsTr('Save current state of the project')
            onClicked: Globals.Proxies.main.project.save()
        },

        EaElements.ToolButton {
            enabled: false
            fontIcon: 'undo'
        },

        EaElements.ToolButton {
            enabled: false
            fontIcon: 'redo'
        },

        EaElements.ToolButton {
            enabled: Globals.Vars.homePageEnabled
            fontIcon: 'backspace'
            ToolTip.text: qsTr('Reset to initial state without project, model and data')
            onClicked: {
                console.debug(`Clicking 'Reset' button: ${this}`)
                appBarCentralTabs.setCurrentIndex(0)
                Globals.Proxies.disableAllPages()
                Globals.Proxies.resetAll()
            }
            Component.onCompleted: Globals.Refs.app.appbar.resetStateButton = this
        }

    ]

    // Right group of application bar tool buttons
    appBarRightButtons: [

        EaElements.ToolButton {
            fontIcon: 'cog'
            ToolTip.text: qsTr('Application preferences')
            onClicked: EaGlobals.Vars.showAppPreferencesDialog = true
        },

        EaElements.ToolButton {
            fontIcon: 'question-circle'
            ToolTip.text: qsTr('Get online help')
            onClicked: Qt.openUrlExternally(Globals.Configs.appConfig.docsUrl)
        },

        EaElements.ToolButton {
            fontIcon: 'bug'
            ToolTip.text: qsTr('Report a bug or issue')
            onClicked: Qt.openUrlExternally(Globals.Configs.appConfig.issuesUrl)
        }

    ]

    // Central group of application bar tab buttons (workflow tabs)
    // Tab buttons for the pages described below
    appBarCentralTabs.contentData: [

        // Home tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.homePageEnabled
            fontIcon: 'home'
            text: qsTr('Home')
            ToolTip.text: qsTr('Home page')
            Component.onCompleted: {
                homePageLoader.source = 'Pages/Home/Page.qml'
                Globals.Refs.app.appbar.homeButton = this
            }
        },

        // Project tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.projectPageEnabled
            fontIcon: 'archive'
            text: qsTr('Project')
            ToolTip.text: qsTr('Project description page')
            onEnabledChanged: enabled ?
                                  projectPageLoader.source = 'Pages/Project/PageStructure.qml' :
                                  projectPageLoader.source = ''
            Component.onCompleted: Globals.Refs.app.appbar.projectButton = this
        },

        // Model tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.modelPageEnabled  // NEED FIX: rename to defined
            fontIcon: 'layer-group'  //'gem'
            text: qsTr('Model')
            ToolTip.text: qsTr('Model description page')
            onEnabledChanged: enabled ?
                                  modelPageLoader.source = 'Pages/Model/PageStructure.qml' :
                                  modelPageLoader.source = ''
            onClicked: Globals.Proxies.main.connections.updateModelPageOnly()
            Component.onCompleted: Globals.Refs.app.appbar.modelButton = this
        },

        // Experiment tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.experimentPageEnabled
            fontIcon: 'microscope'
            text: qsTr('Experiment')
            ToolTip.text: qsTr('Experimental settings and measured data page')
            onEnabledChanged: enabled ?
                                  experimentPageLoader.source = 'Pages/Experiment/PageStructure.qml' :
                                  experimentPageLoader.source = ''
            onClicked: Globals.Proxies.main.connections.updateExperimentPageOnly()
            Component.onCompleted: Globals.Refs.app.appbar.experimentButton = this
        },

        // Analysis tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.analysisPageEnabled
            fontIcon: 'calculator'
            text: qsTr('Analysis')
            ToolTip.text: qsTr('Simulation and fitting page')
            onEnabledChanged: enabled ?
                                  analysisPageLoader.source = 'Pages/Analysis/PageStructure.qml' :
                                  analysisPageLoader.source = ''
            Component.onCompleted: Globals.Refs.app.appbar.analysisButton = this
        },

        // Summary tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.summaryPageEnabled
            fontIcon: 'clipboard-list'
            text: qsTr('Summary')
            ToolTip.text: qsTr('Summary of the work done')
            onEnabledChanged: enabled ?
                                  summaryPageLoader.source = 'Pages/Summary/PageStructure.qml' :
                                  summaryPageLoader.source = ''
            //onCheckedChanged: checked ?
            //                      Globals.Proxies.main.summary.isCreated = true :
            //                      Globals.Proxies.main.summary.isCreated = false
            Component.onCompleted: Globals.Refs.app.appbar.summaryButton = this
        }

    ]

    //////////////////////
    // MAIN VIEW + SIDEBAR
    //////////////////////

    // Pages for the tab buttons described above
    contentArea: [
        Loader { id: homePageLoader },
        Loader { id: projectPageLoader },
        Loader { id: modelPageLoader },
        Loader { id: experimentPageLoader },
        Loader { id: analysisPageLoader },
        Loader { id: summaryPageLoader }
    ]

    /////////////
    // STATUS BAR
    /////////////

    statusBar: Components.StatusBar {}

    ////////////
    // GUI TESTS
    ////////////

    Loader {
        source: Globals.Vars.isTestMode ? 'GuiTestsController.qml' : ''
    }

}
