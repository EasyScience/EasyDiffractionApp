import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

ExComponents.Structure3dView {
    visible: ExGlobals.Variables.experimentPageEnabled
}

/*
Rectangle {
    visible: ExGlobals.Variables.experimentPageEnabled

    color: EaStyle.Colors.mainContentBackground

    EaElements.Label {
        anchors.centerIn: parent
        text: "Structure view: Phase " + ExGlobals.Constants.proxy.phases2Dict[ExGlobals.Variables.phasesCurrentIndex].name
    }
}
*/

/*
Rectangle {
    property double amplitude: ExGlobals.Constants.proxy.phasesDict[ExGlobals.Variables.phasesCurrentIndex].parameters[ExGlobals.Variables.parametersCurrentIndex].amplitude
    property double period: ExGlobals.Constants.proxy.phasesDict[ExGlobals.Variables.phasesCurrentIndex].parameters[ExGlobals.Variables.parametersCurrentIndex].period

    visible: ExGlobals.Variables.experimentPageEnabled

    color: EaStyle.Colors.mainContentBackground

    Rectangle {
        anchors.centerIn: parent

        height: amplitude * ExGlobals.Constants.sampleScale
        width: period * ExGlobals.Constants.sampleScale

        opacity: 0.8

        color: ExGlobals.Constants.proxy.phasesDict[ExGlobals.Variables.phasesCurrentIndex].color
        Behavior on color {
            PropertyAnimation { duration: 500; easing.type: Easing.InOutQuad }
        }

        border.width: 1
        border.color: Qt.darker(color, 1.5)
        Behavior on border.color {
            PropertyAnimation { duration: 500; easing.type: Easing.InOutQuad }
        }

        Behavior on height {
            NumberAnimation { duration: 500; easing.type: Easing.InOutQuad }
        }
        Behavior on width {
            NumberAnimation { duration: 500; easing.type: Easing.InOutQuad }
        }

        EaElements.Label {
            x: -height
            y: (parent.height + width) / 2
            transform: Rotation { origin.x: 0; origin.y: 0; angle: -90}
            text: "amplitude = " + (parent.height / ExGlobals.Constants.sampleScale).toFixed(4)
        }
        EaElements.Label {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.bottom
            text: "period = " + (parent.width / ExGlobals.Constants.sampleScale).toFixed(4)
        }
    }

}
*/
