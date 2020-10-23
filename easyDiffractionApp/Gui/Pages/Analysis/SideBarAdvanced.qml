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
        title: qsTr("Plotting")
        collapsed: false

        EaElements.CheckBox {
            text: qsTr("Show Legend")
            checked: ExGlobals.Variables.showLegend
            onCheckedChanged: displayBridge.showLegend(checked)
        }
    }

}
