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
                model: ExGlobals.Constants.proxy.calculatorList
                onActivated: ExGlobals.Constants.proxy.calculatorIndex = currentIndex

                //currentIndex: ExGlobals.Constants.proxy.calculatorIndex
                Component.onCompleted: {
                    ExGlobals.Variables.calculatorSelector = calculatorSelector
                    currentIndex = ExGlobals.Constants.proxy.calculatorIndex
                }
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Minimization")
        enabled: ExGlobals.Variables.experimentLoaded
        collapsed: false

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
                model: ExGlobals.Constants.proxy.minimizerList
                onCurrentValueChanged: ExGlobals.Constants.proxy.minimizerIndex = currentIndex
                Component.onCompleted: currentIndex = ExGlobals.Constants.proxy.minimizerIndex
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
                model: ExGlobals.Constants.proxy.minimizerMethodList
                onCurrentValueChanged: ExGlobals.Constants.proxy.minimizerMethodIndex = currentIndex
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
            onCheckedChanged: ExGlobals.Variables.showLegend = checked //_matplotlibBridge.showLegend(checked, "figure")
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
