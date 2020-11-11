import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

Row {
    spacing: EaStyle.Sizes.fontPixelSize

    // Zero shift
    EaComponents.TableViewLabel{
        enabled: false
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("Zero shift:")
    }
    EaElements.Parameter {
        enabled: false
        width: textFieldWidth()
        text: "0.0"
        units: "deg"
    }

    // Spacer
    EaElements.Label {
        width: EaStyle.Sizes.fontPixelSize * 0.5
    }

    // Wavelength
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("Wavelength:")
    }
    EaElements.Parameter {
        width: textFieldWidth()
        units: ExGlobals.Constants.proxy.instrumentParameters.wavelength.units
        text: ExGlobals.Constants.proxy.instrumentParameters.wavelength.value
        onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.instrumentParameters.wavelength["@id"], text)
    }

    // Logic

    function labelWidth() {
        return EaStyle.Sizes.fontPixelSize * 6.0
    }

    function textFieldWidth() {
        return EaStyle.Sizes.fontPixelSize * 10.5
    }

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameterValue(id, parseFloat(value))
    }
}
