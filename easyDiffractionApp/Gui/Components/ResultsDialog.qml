import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements

import Gui.Globals 1.0 as ExGlobals

EaElements.Dialog {
    property bool gotResults: typeof ExGlobals.Constants.proxy.fitResults.nvarys !== 'undefined' &&
                              ExGlobals.Constants.proxy.isFitFinished

    title: qsTr("Refinement Results")

    parent: Overlay.overlay

    x: (parent.width - width) * 0.5
    y: (parent.height - height) * 0.5

    modal: true
    standardButtons: Dialog.Ok

    Column {
        EaElements.Label {
            text: gotResults
                  ? `Success: ${ExGlobals.Constants.proxy.fitResults.success}`
                  : `Fitting cancelled`
        }

        EaElements.Label {
            enabled: gotResults
            text: gotResults
                  ? `Num. refined parameters: ${ExGlobals.Constants.proxy.fitResults.nvarys}`
                  : ""
        }

        EaElements.Label {
            enabled: gotResults
            text: gotResults
                  ? `Goodness-of-fit (reduced \u03c7\u00b2): ${ExGlobals.Constants.proxy.fitResults.redchi2.toFixed(2)}`
                  : ""
        }
    }
}

