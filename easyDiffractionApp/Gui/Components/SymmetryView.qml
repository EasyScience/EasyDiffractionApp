import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Row {
    spacing: EaStyle.Sizes.fontPixelSize

    Column {
        spacing: EaStyle.Sizes.fontPixelSize * -0.5

        EaElements.Label {
            enabled: false
            text: qsTr("Crystal system")
        }

        EaElements.ComboBox {
            id: spaceGroupSystemSelect
            width: EaStyle.Sizes.sideBarContentWidth / 3 - EaStyle.Sizes.fontPixelSize * 2
            model: ExGlobals.Constants.proxy.spaceGroupsSystems
            currentIndex: indexOfValue(ExGlobals.Constants.proxy.spaceGroupSystem)
            onActivated: ExGlobals.Constants.proxy.spaceGroupSystem = currentText
        }
    }

    Column {
        spacing: EaStyle.Sizes.fontPixelSize * -0.5

        EaElements.Label {
            enabled: false
            text: qsTr("Space group")
        }

        EaElements.ComboBox {
            width: spaceGroupSystemSelect.width
            model: ExGlobals.Constants.proxy.spaceGroupsInts.display
            currentIndex: ExGlobals.Constants.proxy.spaceGroupInt
            onActivated: ExGlobals.Constants.proxy.spaceGroupInt = currentIndex
        }
    }

    Column {
        spacing: EaStyle.Sizes.fontPixelSize * -0.5

        EaElements.Label {
            enabled: false
            text: qsTr("Setting")
        }

        EaElements.ComboBox {
            width: spaceGroupSystemSelect.width + EaStyle.Sizes.fontPixelSize * 4.0
            model: ExGlobals.Constants.proxy.currentSpaceGroupSettingList
            currentIndex: ExGlobals.Constants.proxy.curentSpaceGroupSettingIndex
            onActivated: ExGlobals.Constants.proxy.curentSpaceGroupSettingIndex = currentIndex
            //onCurrentTextChanged: print("onCurrrentTextChanged", currentText, currentValue)
        }
    }
}
