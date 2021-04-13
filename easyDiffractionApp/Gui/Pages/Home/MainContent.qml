import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

Item {
    id: root

    Column {
        anchors.centerIn: parent
        spacing: EaStyle.Sizes.fontPixelSize * 2.5

        // Application logo, name and version
        Column {
            anchors.horizontalCenter: parent.horizontalCenter

            // Application logo
            Image {
                source: ExGlobals.Constants.appLogo
                anchors.horizontalCenter: parent.horizontalCenter
                width: EaStyle.Sizes.fontPixelSize * 6
                fillMode: Image.PreserveAspectFit
                antialiasing: true
            }

            // Application name
            Row {
                property var fontFamily: EaStyle.Fonts.secondCondensedFontFamily
                property var fontPixelSize: EaStyle.Sizes.fontPixelSize * 4

                anchors.horizontalCenter: parent.horizontalCenter

                EaElements.Label {
                    font.family: parent.fontFamily
                    font.pixelSize: parent.fontPixelSize
                    font.weight: Font.ExtraLight
                    text: ExGlobals.Constants.appPrefixName
                }
                EaElements.Label {
                    font.family: parent.fontFamily
                    font.pixelSize: parent.fontPixelSize
                    text: ExGlobals.Constants.appSuffixName
                }
            }

            // Application version
            EaElements.Label {
                anchors.horizontalCenter: parent.horizontalCenter
                text: ExGlobals.Constants.branch && ExGlobals.Constants.branch !== 'master'
                      ? qsTr(`Version <a href="${ExGlobals.Constants.commitUrl}">${ExGlobals.Constants.appVersion}-${ExGlobals.Constants.commit}</a> (${ExGlobals.Constants.appDate})`)
                      : qsTr(`Version ${ExGlobals.Constants.appVersion} (${ExGlobals.Constants.appDate})`)
            }

            // Github branch
            EaElements.Label {
                visible: ExGlobals.Constants.branch && ExGlobals.Constants.branch !== 'master'
                topPadding: EaStyle.Sizes.fontPixelSize * 0.5
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr(`Branch <a href="${ExGlobals.Constants.branchUrl}">${ExGlobals.Constants.branch}</a>`)
            }
        }

        // Start button
        EaElements.SideBarButton {
            width: EaStyle.Sizes.fontPixelSize * 15
            anchors.horizontalCenter: parent.horizontalCenter
            fontIcon: "rocket"
            text: qsTr("Start")
            onClicked: {
                ExGlobals.Variables.projectPageEnabled = true
                ExGlobals.Variables.projectTabButton.toggle()
                ExGlobals.Constants.proxy.resetUndoRedoStack()
            }
            Component.onCompleted: ExGlobals.Variables.startButton = this
        }

        // Links
        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: EaStyle.Sizes.fontPixelSize * 3

            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    text: qsTr("About %1".arg(ExGlobals.Constants.appName))
                    onClicked: EaGlobals.Variables.showAppAboutDialog = true
                    Component.onCompleted: ExGlobals.Variables.aboutButton = this
                }
                EaElements.Button {
                    text: qsTr("Online documentation")
                    onClicked: Qt.openUrlExternally(ExGlobals.Constants.appUrl)
                }
                EaElements.Button {
                    text: qsTr("Get in touch online")
                    onClicked: Qt.openUrlExternally(`${ExGlobals.Constants.appUrl}/issues`)
                    Component.onCompleted: ExGlobals.Variables.getInTouchButton = this
                }
            }

            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    enabled: false
                    text: qsTr("Tutorial") + " 1: " + qsTr("Data fitting")
                    onPressed: runTutorial1()
                }
                EaElements.Button {
                    text: qsTr("Tutorial") + " 2: " + qsTr("Data simulation")
                    onPressed: runTutorial2()
                }
                EaElements.Button {
                    text: qsTr("Tutorial") + " 3: " + qsTr("App settings")
                    onPressed: runTutorial3()
                }
            }
        }

    }

    // Remote controller for tutorials

    EaElements.RemoteController {
        id: rc
        visible: false
        audioDir: Qt.resolvedUrl("../../Resources/Audio")
        audioEnabled: false
    }

    Timer {
        id: quitTimer
        interval: 1000
        onTriggered: {
            print("* closing app")
            Qt.quit()
        }
    }

    Timer {
        id: runTutorialTimer
        interval: 1000
        onTriggered: runTutorial2()
    }

    Component.onCompleted: {
        if (EaGlobals.Variables.isTestMode) {
            print('TEST MODE')
            runTutorialTimer.start()
        }
    }

    // Tutorials related logic

    function startSavingScreenshots() {
        if (EaGlobals.Variables.isTestMode) {
            //EaGlobals.Variables.saveScreenshotsRunning = true
            const frame_rect = {
                left: window.x,
                top: window.y,
                width: window.width,
                height: window.height
            }
            const margin_rect = {
                left: 3 * EaStyle.Sizes.fontPixelSize,
                top: 3 * EaStyle.Sizes.fontPixelSize,
                right: 3 * EaStyle.Sizes.fontPixelSize,
                bottom: 3 * EaStyle.Sizes.fontPixelSize
            }
            ExGlobals.Constants.proxy.screenRecorder.startRecording(frame_rect, margin_rect)
        }
    }

    function endSavingScreenshots() {
        if (EaGlobals.Variables.isTestMode) {
            //EaGlobals.Variables.saveScreenshotsRunning = false
            ExGlobals.Constants.proxy.screenRecorder.stopRecording()
            quitTimer.start()
        }
    }

    function runTutorial1() {
        print("* run Tutorial 1")

        startSavingScreenshots()
        rc.wait(1000)
        rc.posToCenter()
        rc.showPointer()

        rc.mouseClick(ExGlobals.Variables.startButton)
        rc.mouseClick(ExGlobals.Variables.createProjectButton)
        rc.mouseClick(ExGlobals.Variables.sampleTabButton)
        rc.mouseClick(ExGlobals.Variables.addNewSampleButton)
        rc.mouseClick(ExGlobals.Variables.sampleParametersGroup)

        rc.mouseClick(ExGlobals.Variables.amplitudeTextInput)
        rc.hidePointer()
        rc.keyClick(Qt.Key_Right)
        rc.deleteCharacters(6)
        rc.typeText("2.1234")
        rc.keyClick(Qt.Key_Enter)
        rc.showPointer()

        rc.mouseClick(ExGlobals.Variables.periodTextInput)
        rc.hidePointer()
        rc.keyClick(Qt.Key_Right)
        rc.deleteCharacters(1)
        rc.typeText("6")
        rc.keyClick(Qt.Key_Enter)
        rc.showPointer()

        rc.wait(2000)

        rc.mouseClick(ExGlobals.Variables.experimentTabButton)
        rc.mouseClick(ExGlobals.Variables.generateMeasuredDataButton)

        rc.wait(1000)

        rc.mouseClick(ExGlobals.Variables.analysisTabButton)
        rc.mouseClick(ExGlobals.Variables.xShiftFitCheckBox)

        rc.mouseClick(ExGlobals.Variables.xShiftValueTextInput)
        rc.hidePointer()
        rc.keyClick(Qt.Key_Right)
        rc.keyClick(Qt.Key_Right)
        rc.keyClick(Qt.Key_Right)
        rc.keyClick(Qt.Key_Right)
        rc.deleteCharacters(6)
        rc.typeText("-0.3")
        rc.keyClick(Qt.Key_Enter)
        rc.showPointer()

        rc.mouseClick(ExGlobals.Variables.startFittingButton)
        rc.mouseClick(ExGlobals.Variables.xShiftFitCheckBox)
        rc.mouseClick(ExGlobals.Variables.startFittingButton)

        rc.wait(1000)

        rc.hidePointer()
        rc.wait(1000)
        endSavingScreenshots()
    }

    function runTutorial2() {
        print("* run Tutorial 2")

        rc.visible = true

        // Start

        let x_pos = undefined
        let y_pos = undefined

        startSavingScreenshots()
        rc.wait(1000)
        rc.posToCenter()
        rc.showPointer()

        // App preferences

        rc.say("Application preferences can be accessed quickly from the application toolbar.")
        rc.mouseClick(ExGlobals.Variables.preferencesButton)

        rc.mouseClick(ExGlobals.Variables.themeSelector)
        y_pos = !EaStyle.Colors.isDarkTheme ? EaStyle.Sizes.comboBoxHeight * 1.5 : undefined
        rc.mouseClick(ExGlobals.Variables.themeSelector, x_pos, y_pos)

        rc.mouseClick(ExGlobals.Variables.enableToolTipsCheckBox)
        rc.wait(500)
        //rc.keyClick(Qt.Key_Escape) // DOESN'T WORK ON CI XVFB
        rc.mouseClick(ExGlobals.Variables.preferencesOkButton)

        // Home Tab

        rc.say("To start working with easy diffraction, just click start button.")
        rc.mouseClick(ExGlobals.Variables.startButton)

        // Project Tab

        //rc.say("Here, you can create a new project.")
        //rc.mouseClick(ExGlobals.Variables.createProjectButton)

        rc.say("Now, you can continue without creating a project.")
        rc.mouseClick(ExGlobals.Variables.continueWithoutProjectButton)

        // Sample Tab

        rc.say("Use application toolbar to switch to the sample description page.")
        rc.mouseClick(ExGlobals.Variables.sampleTabButton)

        rc.say("You can set new phase from file or manually.")
        rc.mouseClick(ExGlobals.Variables.setNewSampleManuallyButton)

        rc.say("Now, you can change the symmetry and cell parameters.")
        rc.mouseClick(ExGlobals.Variables.symmetryGroup, 15)
        x_pos = typeof ExGlobals.Variables.cellLengthALabel !== 'undefined' ?
                    ExGlobals.Variables.cellLengthALabel.width :
                    0
        rc.mouseClick(ExGlobals.Variables.cellLengthALabel, x_pos)
        rc.hidePointer()
        //rc.keyClick(Qt.Key_Right)
        //rc.keyClick(Qt.Key_Right)
        rc.deleteCharacters(6)
        rc.typeText("7.00")
        //rc.keyClick(Qt.Key_Enter) // DOESN'T WORK ON CI XVFB ?
        rc.showPointer()

        rc.say("Append or remove new atoms.")
        rc.mouseClick(ExGlobals.Variables.atomsGroup, 15)
        rc.mouseClick(ExGlobals.Variables.appendNewAtomButton)

        rc.say("To change the structure view parameters use the toolbar buttons.")
        rc.mouseClick(ExGlobals.Variables.xProjectionButton)
        rc.mouseClick(ExGlobals.Variables.showBondsButton)
        rc.mouseClick(ExGlobals.Variables.showBondsButton)
        rc.mouseClick(ExGlobals.Variables.showLabelsButton)
        rc.mouseClick(ExGlobals.Variables.showLabelsButton)
        rc.mouseClick(ExGlobals.Variables.projectionTypeButton)
        rc.mouseClick(ExGlobals.Variables.projectionTypeButton)
        rc.mouseClick(ExGlobals.Variables.yProjectionButton)
        rc.mouseClick(ExGlobals.Variables.zProjectionButton)
        rc.mouseClick(ExGlobals.Variables.defaultViewButton)

        rc.wait(1000)

        // Experiment Tab

        rc.say("When the sample is fully described, use application toolbar to switch to the experiment description page.")
        rc.mouseClick(ExGlobals.Variables.experimentTabButton)

        rc.say("If you don't have experimental data, just click continue without experiment button to enable analysis page and some parameters needed for simulation.")
        rc.mouseClick(ExGlobals.Variables.continueWithoutExperimentDataButton)

        // Analysis Tab

        rc.say("Now, you can switch to the analysis page to see and control the simulated diffraction pattern.")
        rc.mouseClick(ExGlobals.Variables.analysisTabButton)
        rc.wait(1000)
        rc.say("In the advanced controls, you can choose between different calculation engines.")
        rc.mouseClick(ExGlobals.Variables.analysisAdvancedControlsTabButton)
        // CFML
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        x_pos = undefined
        y_pos = EaStyle.Sizes.comboBoxHeight * 1.5
        rc.mouseClick(ExGlobals.Variables.calculatorSelector, x_pos, y_pos)
        rc.wait(1000)
        // GSAS-II
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        x_pos = undefined
        y_pos = EaStyle.Sizes.comboBoxHeight * 2.5
        rc.mouseClick(ExGlobals.Variables.calculatorSelector, x_pos, y_pos)
        rc.wait(1000)
        // CrysPy
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        rc.mouseClick(ExGlobals.Variables.analysisBasicControlsTabButton)

        // Summary Tab

        rc.say("Now, you can see the interactive report generated on the summary page and export it in different formats.")
        rc.mouseClick(ExGlobals.Variables.summaryTabButton)
        rc.wait(1000)
        rc.pointerMove(ExGlobals.Variables.reportWebView)
        //rc.mouseMove(ExGlobals.Variables.reportWebView)
        //rc.mouseWheel(ExGlobals.Variables.reportWebView)
        rc.wait(1000)

        // End

        rc.hidePointer()
        rc.say("Thank you for using easy diffraction.")
        rc.wait(1000)
        endSavingScreenshots()

        rc.visible = false
    }

    function runTutorial3() {
        print("* run Tutorial 3")

        rc.visible = true

        startSavingScreenshots()
        rc.wait(1000)
        rc.posToCenter()
        rc.showPointer()

        rc.mouseClick(ExGlobals.Variables.preferencesButton)
        rc.mouseClick(ExGlobals.Variables.themeSelector)

        const x_pos = undefined
        let y_pos = !EaStyle.Colors.isDarkTheme ? EaStyle.Sizes.comboBoxHeight * 1.5 : undefined
        rc.mouseClick(ExGlobals.Variables.themeSelector, x_pos, y_pos)

        rc.wait(1000)

        rc.mouseClick(ExGlobals.Variables.themeSelector)
        y_pos = !EaStyle.Colors.isDarkTheme ? EaStyle.Sizes.comboBoxHeight * 1.5 : undefined
        rc.mouseClick(ExGlobals.Variables.themeSelector, x_pos, y_pos)

        rc.wait(1000)
        rc.mouseClick(ExGlobals.Variables.preferencesOkButton)

        rc.wait(1000)

        rc.hidePointer()
        rc.wait(1000)
        endSavingScreenshots()

        rc.visible = false
    }

    // TESTS

    /*
    TestCase {
        name: "GeometryTests"
        when: windowShown
        id: test1

        function test_width() {
            compare(root.width, 120)
        }
    }
    */

}
