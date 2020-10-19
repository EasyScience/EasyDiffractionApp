import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {
    property int independentParCurrentIndex: 0
    property int dependentParCurrentIndex: 0
    property int dependentParCurrentIndex2: 0

    EaElements.GroupBox {
        title: qsTr("Calculator")
        collapsed: false

        EaElements.ComboBox {
            width: 200
            currentIndex: ExGlobals.Constants.proxy.calculatorIndex
            model: ExGlobals.Constants.proxy.calculatorList
            onActivated: ExGlobals.Constants.proxy.calculatorIndex = currentIndex
        }
    }

}
