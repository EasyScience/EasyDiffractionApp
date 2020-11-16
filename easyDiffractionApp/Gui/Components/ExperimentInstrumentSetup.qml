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
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("Zero shift:")
    }
    EaElements.Parameter {
        width: textFieldWidth()
        units: typeof ExGlobals.Constants.proxy.instrumentParameters.zero_shift != "undefined" ? ExGlobals.Constants.proxy.instrumentParameters.zero_shift.units : ""
        text: typeof ExGlobals.Constants.proxy.instrumentParameters.zero_shift != "undefined" ? ExGlobals.Constants.proxy.instrumentParameters.zero_shift.value : ""
        onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.instrumentParameters.zero_shift["@id"], text)
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
        units: typeof ExGlobals.Constants.proxy.instrumentParameters.wavelength != "undefined" ? ExGlobals.Constants.proxy.instrumentParameters.wavelength.units : ""
        text: typeof ExGlobals.Constants.proxy.instrumentParameters.wavelength != "undefined" ? ExGlobals.Constants.proxy.instrumentParameters.wavelength.value : ""
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
