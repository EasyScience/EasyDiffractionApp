// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    // Non-standard modes
    property bool isDebugMode: false
    property bool isTestMode: typeof pyIsTestMode !== 'undefined' ?
                                  pyIsTestMode:
                                  false

    // Initial application pages accessibility
    property bool homePageEnabled: isDebugMode ? true : true
    property bool projectPageEnabled: isDebugMode ? true : false
    property bool modelPageEnabled: isDebugMode ? true : false
    property bool experimentPageEnabled: isDebugMode ? true : false
    property bool analysisPageEnabled: isDebugMode ? true : false
    property bool summaryPageEnabled: isDebugMode ? true : false

    // Misc
    property bool splashScreenAnimoFinished: isDebugMode ? true : false
    property bool applicationWindowCreated: false
    property bool homePageCreated: false

    // Charts
    property bool showCoordinateVectorsOnModelPage: true
    property bool showLegendOnExperimentPage: true
    property bool showLegendOnAnalysisPage: true

    // Paths
    function imagePath(fileName) {
        return Qt.resolvedUrl(`../Resources/Images/${fileName}`)
    }

}
