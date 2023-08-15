// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    // Main
    readonly property var app: {
        'appbar': {
            'resetStateButton': null,
            'homeButton': null,
            'projectButton': null,
            'modelButton': null,
            'experimentButton': null,
            'analysisButton': null,
            'summaryButton': null
        },
        'homePage': {
            'startButton': null
        },
        'projectPage': {
            'continueButton': null
        },
        'experimentPage': {
            'continueButton': null,
            'importDataFromLocalDriveButton': null,
            'addDefaultExperimentDataButton': null,
            'plotView': null
        },
        'modelPage': {
            'continueButton': null,
            'loadNewModelFromFileButton': null,
            'addNewModelManuallyButton': null,
            'plotView': null,
            'shiftParameter': null,
            'widthParameter': null,
            'scaleParameter': null
        },
        'analysisPage': {
            'continueButton': null,
            'startFittingButton': null,
            'plotView': null,
            'fitStatusDialogOkButton': null,
        },
        'summaryPage': {
        }
    }

    // Misc
    property var summaryReportWebEngine
    property var remoteController

}
