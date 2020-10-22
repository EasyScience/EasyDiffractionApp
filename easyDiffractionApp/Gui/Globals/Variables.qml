pragma Singleton

import QtQuick 2.13

QtObject {
    // Debug mode
    property bool isDebugMode: false

    // Initial application components accessibility
    property bool homePageEnabled: isDebugMode ? true : true
    property bool projectPageEnabled: isDebugMode ? true : false
    property bool samplePageEnabled: isDebugMode ? true : false
    property bool experimentPageEnabled: isDebugMode ? true : false
    property bool analysisPageEnabled: isDebugMode ? true : false
    property bool summaryPageEnabled: isDebugMode ? true : false

    // Workflow states
    property bool projectCreated: false
    property bool sampleLoaded: false
    property bool experimentLoaded: false

    // //////////////////////////
    // References to GUI elements
    // //////////////////////////

    // Application bar tab buttons
    property var homeTabButton
    property var projectTabButton
    property var sampleTabButton
    property var experimentTabButton
    property var analysisTabButton
    property var summaryTabButton

    // Sidebar controls tab buttons
    property var analysisBasicControlsTabButton
    property var analysisAdvancedControlsTabButton

    // Application bar tool buttons
    property var preferencesButton

    // Main content and sidebar buttons
    property var startButton
    property var createProjectButton
    property var setNewSampleManuallyButton
    property var appendNewAtomButton

    // Sidebar group boxes
    property var symmetryGroup
    property var atomsGroup
    property var adpsGroup

    // Sidebar text inputs
    property var cellLengthALabel

    // Comboboxes
    property var themeSelector
    property var calculatorSelector

    // Tables
    property var phasesTable
    property var parametersTable
    property int currentPhaseIndex: -1
    property int currentAtomIndex: -1

    // Slider
    property string currentParameterId
    property real currentParameterValue
}
