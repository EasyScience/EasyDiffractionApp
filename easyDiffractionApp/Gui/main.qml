import QtQuick 2.13

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

ExComponents.ApplicationWindow {
    id: window

    title: `${ExGlobals.Constants.appName} ${ExGlobals.Constants.appVersion}`
}
