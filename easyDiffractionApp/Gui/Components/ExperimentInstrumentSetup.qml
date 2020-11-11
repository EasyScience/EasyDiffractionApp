import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

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
        text: "-0.36"
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
        text: "2.41"
        units: "A"
    }

    // Logic

    function labelWidth() {
        return EaStyle.Sizes.fontPixelSize * 6.0
    }

    function textFieldWidth() {
        return EaStyle.Sizes.fontPixelSize * 10.5
    }
}
