import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Measured data")
        collapsible: false

        EaElements.SideBarButton {
            id: generateMeasuredDataButton
            fontIcon: "plus-circle"
            text: qsTr("Generate measured data")
            onClicked: {
                ExGlobals.Variables.analysisPageEnabled = true
                ExGlobals.Variables.experimentLoaded = true
                ExGlobals.Constants.proxy.generateMeasuredData()
            }
            Component.onCompleted: ExGlobals.Variables.generateMeasuredDataButton = generateMeasuredDataButton
        }
    }

    EaElements.GroupBox {
        title: qsTr("Instrumental parameters")
        //visible: ExGlobals.Variables.analysisPageEnabled
        enabled: ExGlobals.Variables.experimentLoaded
        //collapsed: false

        Grid {
            columns: 4
            columnSpacing: 20
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.Label {
                text: "X-shift"
            }

            EaElements.TextField {
                width: 140
                text: parseFloat(ExGlobals.Constants.proxy.xShift).toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.xShift = text
            }

            EaElements.Label {
                text: "Y-shift"
            }

            EaElements.TextField {
                width: 140
                text: parseFloat(ExGlobals.Constants.proxy.yShift).toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.yShift = text
            }
        }

        Grid {
            columns: 4
            columnSpacing: 20
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.Label {
                text: "x_shift"
            }

            EaElements.TextField {
                width: 140
                text: ExGlobals.Constants.proxy.fitablesDict.x_shift.toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.editFitableValueByName("x_shift", text)
            }

            EaElements.Label {
                text: "y_shift"
            }

            EaElements.TextField {
                width: 140
                text: ExGlobals.Constants.proxy.fitablesDict.y_shift.toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.editFitableValueByName("y_shift", text)
            }
        }
    }

}

