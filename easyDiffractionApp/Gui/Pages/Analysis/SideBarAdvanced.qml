import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import easyAppGui.Globals 1.0 as EaGlobals

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Calculation engine")
        collapsed: false

        EaElements.ComboBox {
            id: calculatorSelector

            width: 200
            model: ExGlobals.Constants.proxy.calculatorList
            onActivated: ExGlobals.Constants.proxy.calculatorIndex = currentIndex

            //currentIndex: ExGlobals.Constants.proxy.calculatorIndex
            Component.onCompleted: {
                ExGlobals.Variables.calculatorSelector = calculatorSelector
                currentIndex = ExGlobals.Constants.proxy.calculatorIndex
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Minimizer")
        collapsed: false

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.ComboBox {
                id: minimizerSelector

                width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 2

                model: ExGlobals.Constants.proxy.minimizerList

                onCurrentValueChanged: {
                    //print("currentValue 1", currentValue)
                    ExGlobals.Constants.proxy.minimizerIndex = currentIndex
                }

                //currentIndex: ExGlobals.Constants.proxy.calculatorIndex
                Component.onCompleted: {
                    //ExGlobals.Variables.minimizerSelector = minimizerSelector
                    currentIndex = ExGlobals.Constants.proxy.minimizerIndex
                }
            }

            EaElements.ComboBox {
                id: methodSelector

                width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 2

                model: {
                    if (minimizerSelector.currentValue === 'lmfit') {
                        return ['leastsq', 'least_squares', 'powell', 'cg', 'cobyla', 'bfgs', 'tnc', 'shgo']
                    } else if (minimizerSelector.currentValue === 'bumps') {
                        return ['amoeba', 'lm', 'newton']
                    } else {
                        return ['']
                    }
                }

                onModelChanged: {
                    if (minimizerSelector.currentValue === 'lmfit') {
                        currentIndex = 0
                    } else if (minimizerSelector.currentValue === 'bumps') {
                        currentIndex = 1
                    }
                }

                onCurrentValueChanged: {
                    if (typeof currentValue !== 'undefined') {
                        ExGlobals.Constants.minimizerMethod = currentValue
                    }
                }
            }
        }

    }

    EaElements.GroupBox {
        title: qsTr("Plot settings")
        collapsed: false

        EaElements.CheckBox {
            topPadding: 0
            text: qsTr("Show legend")
            checked: ExGlobals.Variables.showLegend
            onCheckedChanged: _matplotlibBridge.showLegend(checked, "figure")
        }
    }

    EaElements.GroupBox {
        title: qsTr("Parameters settings")
        last: true
        collapsed: false

        EaElements.CheckBox {
            topPadding: 0
            text: qsTr("Iconified names")
            checked: ExGlobals.Variables.iconifiedNames
            onCheckedChanged: ExGlobals.Variables.iconifiedNames = checked
        }
    }

}
