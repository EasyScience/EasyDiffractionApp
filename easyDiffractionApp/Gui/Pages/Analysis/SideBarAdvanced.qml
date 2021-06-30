// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Calculation")

        Row {
            spacing: minimizerRow.spacing

            // Minimizer
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: minimizerLabel.width
                text: qsTr("Engine:")
            }
            EaElements.ComboBox {
                width: minimizerSelector.width
                model: ExGlobals.Constants.proxy.fitting.calculatorNames
                currentIndex: ExGlobals.Constants.proxy.fitting.currentCalculatorIndex
                onCurrentIndexChanged: ExGlobals.Constants.proxy.fitting.currentCalculatorIndex = currentIndex
                Component.onCompleted: ExGlobals.Variables.calculatorSelector = this
            }
        }

        Component.onCompleted: ExGlobals.Variables.calculatorsGroup = this
    }

    EaElements.GroupBox {
        title: qsTr("Minimization")
        enabled: ExGlobals.Constants.proxy.experiment.experimentLoaded

        Row {
            id: minimizerRow

            spacing: EaStyle.Sizes.fontPixelSize

            // Minimizer
            EaComponents.TableViewLabel{
                id: minimizerLabel

                horizontalAlignment: Text.AlignRight
                width: EaStyle.Sizes.fontPixelSize * 4.5
                text: qsTr("Minimizer:")
            }
            EaElements.ComboBox {
                id: minimizerSelector

                width: (EaStyle.Sizes.sideBarContentWidth - minimizerLabel.width * 2 - minimizerRow.spacing * 3) / 2

                model: ExGlobals.Constants.proxy.fitting.minimizerNames
                currentIndex: ExGlobals.Constants.proxy.fitting.currentMinimizerIndex

                onCurrentIndexChanged: {
                    ExGlobals.Constants.proxy.fitting.currentMinimizerIndex = currentIndex
                }
            }

            // Method
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: minimizerLabel.width
                text: qsTr("Method:")
            }
            EaElements.ComboBox {
                id: methodSelector

                width: minimizerSelector.width
                model: ExGlobals.Constants.proxy.fitting.minimizerMethodNames
                currentIndex: ExGlobals.Constants.proxy.fitting.currentMinimizerMethodIndex
                onCurrentIndexChanged: {
                    ExGlobals.Constants.proxy.fitting.currentMinimizerMethodIndex = currentIndex
                }
            }
        }

    }

    /*
    EaElements.GroupBox {
        title: qsTr("Plot settings")

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.CheckBox {
                text: qsTr("Show legend")
                checked: ExGlobals.Variables.showLegend
                onCheckedChanged: ExGlobals.Variables.showLegend = checked
            }

            EaElements.CheckBox {
                text: qsTr("Show measured")
                checked: ExGlobals.Constants.proxy.showMeasuredSeries
                onCheckedChanged: ExGlobals.Constants.proxy.showMeasuredSeries = checked
            }

            EaElements.CheckBox {
                text: qsTr("Show difference")
                checked: ExGlobals.Constants.proxy.showDifferenceChart
                onCheckedChanged: ExGlobals.Constants.proxy.showDifferenceChart = checked
            }
        }
    }
    */

    EaElements.GroupBox {
        title: qsTr("Parameters")
        last: true

        EaElements.CheckBox {
            topPadding: 0
            text: qsTr("Iconified names")
            checked: ExGlobals.Variables.iconifiedNames
            onCheckedChanged: ExGlobals.Variables.iconifiedNames = checked
        }
    }

}
