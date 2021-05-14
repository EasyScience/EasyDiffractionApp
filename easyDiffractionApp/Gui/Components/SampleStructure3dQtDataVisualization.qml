import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Style 1.0 as EaStyle
import easyApp.Animations 1.0 as EaAnimations
import easyApp.Elements 1.0 as EaElements

Rectangle {
    color: EaStyle.Colors.contentBackground
    Behavior on color { EaAnimations.ThemeChange {} }

    EaElements.Label {
        enabled: false
        anchors.centerIn: parent
        font.family: EaStyle.Fonts.secondFontFamily
        font.pixelSize: EaStyle.Sizes.fontPixelSize * 3
        font.weight: Font.ExtraLight
        text: 'Not implemented'
    }
}
