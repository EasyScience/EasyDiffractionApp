import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Dialogs 1.2
import QtQuick.Window 2.12
import QtQuick.Controls.Material 2.12
import QtCharts 2.3
import QtVTK 1.0

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    id: chartContainer

    VtkFboItem {
        id: vtkFboItem
        objectName: "vtkFboItem"
        anchors.fill: parent
    }

    MouseArea {
        acceptedButtons: Qt.AllButtons
        anchors.fill: parent
        scrollGestureEnabled: false

        onPositionChanged: (mouse) => {
            //print('Mouse moved')
            _vtkHandler.mouseMoveEvent(pressedButtons, mouseX, mouseY)
            mouse.accepted = false
        }
        onPressed: (mouse) => {
            _vtkHandler.mousePressEvent(pressedButtons, mouseX, mouseY)
            mouse.accepted = false
            // if u want to propagate the pressed event
            // so the VtkFboItem instance can receive it
            // then uncomment the belowed line
            // mouse.ignore() // or mouse.accepted = false
        }
        onReleased: (mouse) => {
            _vtkHandler.mouseReleaseEvent(pressedButtons, mouseX, mouseY)
            //print(mouse)
            mouse.accepted = false
        }
        onWheel: (wheel) => {
            wheel.accepted = false
        }
    }

    EaElements.Label {
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: EaStyle.Sizes.fontPixelSize

        topPadding: 0.5*EaStyle.Sizes.fontPixelSize
        bottomPadding: 0.5*EaStyle.Sizes.fontPixelSize
        leftPadding: EaStyle.Sizes.fontPixelSize
        rightPadding: EaStyle.Sizes.fontPixelSize

        background: Rectangle {
            color: EaStyle.Colors.mainContentBackground
            opacity: 0.5
        }

        textFormat: Text.RichText

        text: `Axes colors: <font color=red>a</font>, <font color=#008000>b</font>, <font color=blue>c</font>`
    }

    // Save chart

    property int chartChangedTime: ExGlobals.Constants.proxy.structureChartChangedTime
    onChartChangedTimeChanged: saveChartTimer.restart()

    Timer {
        id: saveChartTimer
        interval: 1000
        onTriggered: saveChart()
    }

    function saveChart() {
        const imgWidth = chartContainer.width
        const imgHeight = chartContainer.height / chartContainer.width * imgWidth
        chartContainer.grabToImage(
                    function(result) {
                        ExGlobals.Variables.structureImageSource = ExGlobals.Constants.proxy.imageToSource(result.image)
                    },
                    Qt.size(imgWidth, imgHeight)
                    )
    }

}
