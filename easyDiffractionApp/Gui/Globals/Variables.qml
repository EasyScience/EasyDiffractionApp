pragma Singleton

import QtQuick 2.13

QtObject {
    // Debug mode
    property bool isDebugMode: typeof _pyQmlProxyObj === "undefined"

    // Initial application components accessibility
    property bool homePageEnabled: isDebugMode ? true : true
    property bool projectPageEnabled: isDebugMode ? true : false
    property bool samplePageEnabled: isDebugMode ? true : false
//    property bool experimentPageEnabled: isDebugMode ? true : false
    property bool analysisPageEnabled: isDebugMode ? true : false
    property bool summaryPageEnabled: isDebugMode ? true : false

    // Workflow states
    property bool projectCreated: false
    property bool sampleLoaded: false
    property bool experimentSkipped: false
    property bool needsSave: true // while waiting for a proper undo/redo flag

    // //////////
    // HTML parts
    // //////////
    property string analysisChartHeadScript: ""
    property string analysisChartHeadStyle: ""
    property string analysisChartHtml: ""
    property string reportHtml: ""

    //property string reportFilePath: ""

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

    // Main application window
    property var showSaveDialog : false

    // Application bar tool buttons
    property var preferencesButton
    property var preferencesOkButton

    // Main content and sidebar buttons
    property var startButton
    property var createProjectButton
    property var continueWithoutProjectButton
    property var setNewSampleManuallyButton
    property var appendNewAtomButton
    property var continueWithoutExperimentDataButton

    // Sidebar group boxes
    property var symmetryGroup
    property var atomsGroup
    property var adpsGroup

    // Sidebar text inputs
    property var cellLengthALabel

    // Checkboxes
    property var enableToolTipsCheckBox

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

    // Analysis tab settings
    property bool showLegend: false
    property bool iconifiedNames: true

    // Plotting
    property var bokehStructureChart
    property var analysisChart
    property var analysisImageSource
    property var structureImageSource
    property var showBondsButton
    property var showLabelsButton
    property var projectionTypeButton
    property var xProjectionButton
    property var yProjectionButton
    property var zProjectionButton
    property var defaultViewButton

    // Summary
    property var reportWebView

}
