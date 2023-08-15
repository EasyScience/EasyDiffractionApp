// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import Gui.Globals as Globals


EaElements.StatusBar {
    visible: EaGlobals.Vars.appBarCurrentIndex !== 0

    EaElements.StatusBarItem {
        keyIcon: 'archive'
        keyText: qsTr('Project')
        valueText: Globals.Proxies.main.status.project ?? ''
        ToolTip.text: qsTr('Current project')
    }

    EaElements.StatusBarItem {
        keyIcon: 'layer-group'
        keyText: qsTr('Models')
        valueText: Globals.Proxies.main.status.phaseCount ?? ''
        ToolTip.text: qsTr('Number of models added')
    }

    EaElements.StatusBarItem {
        keyIcon: 'microscope'
        keyText: qsTr('Experiments')
        valueText: Globals.Proxies.main.status.experimentsCount ?? ''
        ToolTip.text: qsTr('Number of experiments added')
    }

    EaElements.StatusBarItem {
        keyIcon: 'calculator'
        keyText: qsTr('Calculator')
        valueText: Globals.Proxies.main.status.calculator ?? ''
        ToolTip.text: qsTr('Current calculation engine')
    }

    EaElements.StatusBarItem {
        keyIcon: 'level-down-alt'
        keyText: qsTr('Minimizer')
        valueText: Globals.Proxies.main.status.minimizer ?? ''
        ToolTip.text: qsTr('Current minimization engine and method')
    }

    EaElements.StatusBarItem {
        keyIcon: 'th-list'
        keyText: qsTr('Parameters')
        valueText: Globals.Proxies.main.status.variables ?? ''
        ToolTip.text: qsTr('Number of parameters: total, free and fixed')
    }

    EaElements.StatusBarItem {
        keyIcon: 'spinner'
        keyText: qsTr('Fit iterations')
        valueText: Globals.Proxies.main.status.fitIteration ?? ''
        ToolTip.text: qsTr('Number of fit iterations after the last refinement step')
    }

    EaElements.StatusBarItem {
        visible: valueText !== '' && Globals.Proxies.main.analysis.defined  // NEED FIX
        keyIcon: 'thumbs-up'
        keyText: qsTr('Goodness-of-fit')
        valueText: Globals.Proxies.main.status.goodnessOfFit ?? ''
        ToolTip.text: valueText.includes('→') ?
                          qsTr('Reduced χ² goodness-of-fit: previous → last') :
                          qsTr('Reduced χ² goodness-of-fit')  // 'Goodness-of-fit for comparison of the observed data with the data expected under the model'
    }

    EaElements.StatusBarItem {
        keyIcon: 'clipboard'
        keyText: qsTr('Fit status')
        valueText: Globals.Proxies.main.status.fitStatus ?? ''
        ToolTip.text: qsTr('Status of the last refinement step')
    }

}
