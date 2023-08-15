// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaElements.RemoteController {
    id: rc

    visible: false

    // Timers

    Timer {
        id: runTutorialTimer

        interval: 1000

        onTriggered: {
            console.debug('Application is lunched in test mode.')

            //print('Start saving screenshots.')
            //saveScreenshotTimer.start()

            console.debug("Run basic GUI test.")
            runBasicGuiTest()

            //print('Stop saving screenshots.')
            //saveScreenshotTimer.stop()
        }
    }

    Timer {
        id: runGuiTestTimer

        interval: 1000

        onTriggered: runBasicGuiTest()
    }

    Timer {
        id: saveScreenshotTimer

        property int imageNumber: 0

        interval: 200
        repeat: true

        onTriggered: {
            const digitsCount = 6
            const fileSuffix = (1e15 + ++imageNumber + '').slice(-digitsCount)
            const filePath = `tests/gui/screenshot_${fileSuffix}.jpg`
            saveScreenshot(parent, filePath)
        }
    }

    // Tutorials

    function setupRunTutorial() {
        rc.visible = true
        rc.posToCenter()
        rc.wait(1000)
        rc.showPointer()
    }

    function completeRunTutorial() {
        rc.hidePointer()
        rc.wait(1000)
        rc.visible = false
    }

    function runDataFittingTutorial() {
        setupRunTutorial()

        // Home Page
        rc.mouseClick(Globals.Refs.app.homePage.startButton)

        // Project Page
        rc.mouseClick(Globals.Refs.app.projectPage.continueButton)

        // Model Page
        rc.mouseClick(Globals.Refs.app.modelPage.loadNewModelFromFileButton)
        rc.mouseClick(Globals.Refs.app.modelPage.continueButton)

        // Experiment page
        rc.mouseClick(Globals.Refs.app.experimentPage.importDataFromLocalDriveButton)
        rc.mouseClick(Globals.Refs.app.experimentPage.continueButton)

        // Analysis page
        rc.mouseClick(Globals.Refs.app.analysisPage.startFittingButton)
        rc.mouseClick(Globals.Refs.app.analysisPage.continueButton)

        completeRunTutorial()
    }

}
