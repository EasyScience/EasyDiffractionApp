import QtQuick 2.13

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

import easyAppGui.Style 1.0 as EaStyle


ExComponents.ApplicationWindow {
    id: window

    title: `${ExGlobals.Constants.appName} ${ExGlobals.Constants.appVersion}`

    // Matplotlib

    Component.onCompleted: {
        ExGlobals.Constants.proxy.setMatplotlibContext(window)

        ExGlobals.Constants.proxy.setMatplotlibFont(EaStyle.Fonts.fontSource)
        ExGlobals.Constants.proxy.updateMatplotlibStyle(EaStyle.Matplotlib.display)
        ExGlobals.Constants.proxy.updateMatplotlibStyle(EaStyle.Matplotlib.sizes)
    }

    property var matplotlibColors: EaStyle.Matplotlib.colors
    onMatplotlibColorsChanged: ExGlobals.Constants.proxy.updateMatplotlibStyle(EaStyle.Matplotlib.colors)
}
