import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

Row {
    spacing: EaStyle.Sizes.fontPixelSize

    // Min
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("2θ-min:")
    }
    EaElements.Parameter {
        id: xMin
        enabled: !ExGlobals.Variables.experimentLoaded
        width: textFieldWidth()
        units: "deg"
        //text: typeof ExGlobals.Constants.proxy.simulationParameters !== "undefined" ? ExGlobals.Constants.proxy.simulationParameters.x_min : ""
        text: ExGlobals.Constants.proxy.simulationParameters.x_min
        onEditingFinished: updateParameters()
    }

    // Spacer
    EaElements.Label {
        width: EaStyle.Sizes.fontPixelSize * 0.5
    }

    // Max
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("2θ-max:")
    }
    EaElements.Parameter {
        id: xMax
        enabled: !ExGlobals.Variables.experimentLoaded
        width: textFieldWidth()
        units: "deg"
        //text: typeof ExGlobals.Constants.proxy.simulationParameters !== "undefined" ? ExGlobals.Constants.proxy.simulationParameters.x_max : ""
        text: ExGlobals.Constants.proxy.simulationParameters.x_max
        onEditingFinished: updateParameters()
    }

    // Spacer
    EaElements.Label {
        width: EaStyle.Sizes.fontPixelSize * 0.5
    }

    // Step
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("2θ-step:")
    }
    EaElements.Parameter {
        id: xStep
        enabled: !ExGlobals.Variables.experimentLoaded
        width: textFieldWidth()
        units: "deg"
        //text: typeof ExGlobals.Constants.proxy.simulationParameters !== "undefined" ? ExGlobals.Constants.proxy.simulationParameters.x_step : ""
        text: ExGlobals.Constants.proxy.simulationParameters.x_step
        onEditingFinished: updateParameters()
    }

    // Logic

    function labelWidth() {
        return EaStyle.Sizes.fontPixelSize * 3.33
    }

    function textFieldWidth() {
        return EaStyle.Sizes.fontPixelSize * 6.5
    }

    function updateParameters() {
        const json = { "x_min": xMin.text, "x_max": xMax.text, "x_step": xStep.text }
        //print("json", JSON.stringify(json))
        ExGlobals.Constants.proxy.simulationParameters = JSON.stringify(json)
    }
}
