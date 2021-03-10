import QtQuick 2.13

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

import easyAppGui.Style 1.0 as EaStyle


ExComponents.ApplicationWindow {
    id: window

    // Matplotlib

    Component.onCompleted: {
        ExGlobals.Constants.proxy.matplotlibBridge.setContext(window)

        ExGlobals.Constants.proxy.matplotlibBridge.setFont(EaStyle.Fonts.fontSource)
        ExGlobals.Constants.proxy.matplotlibBridge.updateStyle(EaStyle.Matplotlib.display)
        ExGlobals.Constants.proxy.matplotlibBridge.updateStyle(EaStyle.Matplotlib.sizes)
    }

    property var matplotlibColors: EaStyle.Matplotlib.colors
    onMatplotlibColorsChanged: ExGlobals.Constants.proxy.matplotlibBridge.updateStyle(EaStyle.Matplotlib.colors)
}
