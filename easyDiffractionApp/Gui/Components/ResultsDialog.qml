import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.XmlListModel 2.14

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

// Info dialog (after refinement)
EaElements.Dialog {
    id: refinementResultsDialog   
    parent: Overlay.overlay

    x: (parent.width - width) * 0.5
    y: (parent.height - height) * 0.5

    // modal: true
    standardButtons: Dialog.Ok

    title: qsTr("Refinement Results")

    Column {
        EaElements.Label { text: ExGlobals.Constants.proxy.isFitFinished ? `Success: ${ExGlobals.Constants.proxy.fitResults.success}` : "" }
        EaElements.Label { text: ExGlobals.Constants.proxy.isFitFinished ? `Num. refined parameters: ${ExGlobals.Constants.proxy.fitResults.nvarys}` : "Fitting in progress..." }
        EaElements.Label { text: ExGlobals.Constants.proxy.isFitFinished ? `Goodness-of-fit (reduced \u03c7\u00b2): ${ExGlobals.Constants.proxy.fitResults.redchi2.toFixed(2)}` : "" }       
    }
}