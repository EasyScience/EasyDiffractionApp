// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Charts as EaCharts

import Gui.Globals as Globals


EaCharts.QtCharts1dMeasVsCalc {
    id: chart

    useOpenGL: EaGlobals.Vars.useOpenGL //Globals.Proxies.main.plotting.useWebGL1d

    axisX.title: "2θ (degree)"
    axisX.min: parameterValue('xMin')
    axisX.max: parameterValue('xMax')

    axisY.title: "Icalc"
    axisY.min: parameterValue('yMin')
    axisY.max: parameterValue('yMax')

    calcSerie.color: EaStyle.Colors.models[Globals.Proxies.main.model.currentIndex]

    // Legend
    Rectangle {
        x: chart.plotArea.x + chart.plotArea.width - width - EaStyle.Sizes.fontPixelSize
        y: chart.plotArea.y + EaStyle.Sizes.fontPixelSize
        width: childrenRect.width
        height: childrenRect.height

        color: EaStyle.Colors.mainContentBackgroundHalfTransparent
        border.color: EaStyle.Colors.chartGridLine

        Column {
            leftPadding: EaStyle.Sizes.fontPixelSize
            rightPadding: EaStyle.Sizes.fontPixelSize
            topPadding: EaStyle.Sizes.fontPixelSize * 0.5
            bottomPadding: EaStyle.Sizes.fontPixelSize * 0.5

            EaElements.Label {
                text: '▬ Icalc (calculated)'
                color: calcSerie.color
            }
        }
    }

    // Data is set in python backend

    Component.onCompleted: {
        Globals.Refs.app.modelPage.plotView = this
        Globals.Proxies.main.plotting.setQtChartsSerieRef('modelPage',
                                                          'calcSerie',
                                                          this.calcSerie)
    }

    // Logic

    function parameterValue(name) {
        if (!Globals.Proxies.main.experiment.defined) {
            return ''
        }
        const currentExperimentIndex = Globals.Proxies.main.experiment.currentIndex
        const value = Globals.Proxies.main.experiment.chartRanges[currentExperimentIndex][name].value
        const formattedValue = value.toFixed(4)
        return formattedValue
    }

}
