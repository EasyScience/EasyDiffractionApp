// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents


EaElements.StatusBar {
    width: 1300
    height: 50
    //color: 'coral'
    //visible: EaGlobals.Vars.appBarCurrentIndex !== 0

    EaElements.StatusBarItem {
        keyIcon: 'archive'
        keyText: qsTr('Project')
        valueText: 'Undefined'
        ToolTip.text: qsTr('Current project name')
    }

    EaElements.StatusBarItem {
        keyIcon: 'layer-group'
        keyText: qsTr('Models')
        valueText: '1'
        ToolTip.text: qsTr('Number of models added')
    }

    EaElements.StatusBarItem {
        keyIcon: 'microscope'
        keyText: qsTr('Experiments')
        valueText: '2'
        ToolTip.text: qsTr('Number of experiments added')
    }

    EaElements.StatusBarItem {
        keyIcon: 'calculator'
        keyText: qsTr('Calculate')
        valueText: 'CrysPy'
        ToolTip.text: qsTr('Current calculation engine')
    }

    EaElements.StatusBarItem {
        keyIcon: 'level-down-alt'
        keyText: qsTr('Minimize')
        valueText: 'Lmfit (BFGO)'
        ToolTip.text: qsTr('Current minimization engine and method')
    }

    EaElements.StatusBarItem {
        keyIcon: 'th-list'
        keyText: qsTr('Params')
        valueText: '50'
        ToolTip.text: qsTr('Number of parameters: total, free and fixed')
    }

    EaElements.StatusBarItem {
        keyIcon: 'spinner'
        keyText: qsTr('Fit iteration')
        valueText: '127'
        ToolTip.text: qsTr('Number of fit iterations after the last refinement step')
    }

    EaElements.StatusBarItem {
        keyIcon: 'thumbs-up'
        keyText: qsTr('Goodness-of-fit')
        valueText: '4.47'
        //ToolTip.text: qsTr('Goodness-of-fit for comparison of the observed data with the data expected under the model')
        ToolTip.text: qsTr('Goodness-of-fit (χ²): previous and last comparisons')
    }

    EaElements.StatusBarItem {
        keyIcon: 'clipboard'
        keyText: qsTr('Fit status')
        valueText: 'Success'
        ToolTip.text: qsTr('Status of the last refinement step')
    }

}
