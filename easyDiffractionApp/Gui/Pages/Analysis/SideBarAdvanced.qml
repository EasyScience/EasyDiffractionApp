import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Calculation")
        collapsed: false

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            // Minimizer
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: EaStyle.Sizes.fontPixelSize * 5.0
                text: qsTr("Engine:")
            }
            EaElements.ComboBox {
                id: calculatorSelector

                width: minimizerSelector.width
                model: ExGlobals.Constants.proxy.calculatorNames
                onActivated: ExGlobals.Constants.proxy.changeCurrentCalculator(currentIndex)

                //currentIndex: ExGlobals.Constants.proxy.calculatorIndex
                Component.onCompleted: {
                    ExGlobals.Variables.calculatorSelector = calculatorSelector
                    currentIndex = ExGlobals.Constants.proxy.currentCalculatorIndex
                }
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Minimization")
        enabled: ExGlobals.Constants.proxy.experimentLoaded
        //collapsed: false

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            // Minimizer
            EaComponents.TableViewLabel{
                id: minimizerLabel

                horizontalAlignment: Text.AlignRight
                width: EaStyle.Sizes.fontPixelSize * 5.0
                text: qsTr("Minimizer:")
            }
            EaElements.ComboBox {
                id: minimizerSelector

                width: (EaStyle.Sizes.sideBarContentWidth - minimizerLabel.width * 2 - EaStyle.Sizes.fontPixelSize * 4) / 2

                model: ExGlobals.Constants.proxy.minimizerNames

                onCurrentValueChanged: {
                    ExGlobals.Constants.proxy.changeCurrentMinimizer(currentIndex)

                    let idx = 0
                    if (currentValue === 'lmfit') {
                        idx = methodSelector.model.indexOf('leastsq')
                    } else if (currentValue === 'bumps') {
                        idx = methodSelector.model.indexOf('lm')
                    }
                    if (idx > -1) {
                        methodSelector.currentIndex = idx
                    }
                }

                Component.onCompleted: currentIndex = ExGlobals.Constants.proxy.currentMinimizerIndex
            }

            // Spacer
            Item {}

            // Method
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: minimizerLabel.width
                text: qsTr("Method:")
            }
            EaElements.ComboBox {
                id: methodSelector

                width: minimizerSelector.width
                model: ExGlobals.Constants.proxy.minimizerMethodNames
                onCurrentValueChanged: ExGlobals.Constants.proxy.changeCurrentMinimizerMethod(currentIndex)
                Component.onCompleted: currentIndex = ExGlobals.Constants.proxy.currentMinimizerMethodIndex
            }
        }

    }

    /*
    EaElements.GroupBox {
        title: qsTr("Plot settings")
        //collapsed: false

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.CheckBox {
                text: qsTr("Show legend")
                checked: ExGlobals.Variables.showLegend
                onCheckedChanged: ExGlobals.Variables.showLegend = checked //_matplotlibBridge.showLegend(checked, "figure")
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
        title: qsTr("Parameters settings")
        last: true
        //collapsed: false

        EaElements.CheckBox {
            topPadding: 0
            text: qsTr("Iconified names")
            checked: ExGlobals.Variables.iconifiedNames
            onCheckedChanged: ExGlobals.Variables.iconifiedNames = checked
        }
    }

}
