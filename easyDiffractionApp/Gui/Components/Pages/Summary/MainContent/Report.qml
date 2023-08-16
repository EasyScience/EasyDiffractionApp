// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.BasicReport {

    xAxisTitle: "x"
    yAxisTitle: "y"

    measuredXYData: Globals.Proxies.main.summary.isCreated ?
                        {'x': Globals.Proxies.main.experiment.xData, 'y': Globals.Proxies.main.experiment.yData} :
                        {}
    calculatedXYData: Globals.Proxies.main.summary.isCreated ?
                          {'x': Globals.Proxies.main.experiment.xData, 'y': Globals.Proxies.main.model.yData} :
                          {}

    Component.onCompleted: Globals.Refs.summaryReportWebEngine = this

}

