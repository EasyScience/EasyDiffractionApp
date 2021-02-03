import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Item {
    id: reportContainer

    ScrollView {
        anchors.fill: parent

        EaElements.TextArea {
            id: textArea

            readOnly: true
            textFormat: TextEdit.RichText
            text: writeHtml()
            onTextChanged: ExGlobals.Constants.proxy.setReport(text)
        }
    }

    /////////////
    // Write HTML
    /////////////

    function writeHtmlHead() {
        let s = ''
        s += '<head>'

        s += '<style>'
        s += 'table {'
        s += 'border-collapse: collapse;'
        s += '}'
        s += 'td, th {'
        s += 'border: 1px solid #ddd;'
        s += 'padding: 2px;'
        s += 'padding-left: 12px;'
        s += 'padding-right: 12px;'
        s += '}'
        s += 'tr:nth-child(even) {'
        s += 'background-color: #eee;'
        s += '}'
        s += `a:link { color: ${EaStyle.Colors.themeAccent.toString() }; }`
        s += '</style>'

        s += '</head>'
        return s
    }

    function writeHtmlTable() {
        let s = ''
        s += '<table>'

        s += '<tr>'
        s += '<th align="right">No.</th>'
        s += '<th align="left">Parameter</th>'
        s += '<th align="right">Value</th>'
        s += '<th align="left"></th>'
        if (typeof ExGlobals.Constants.proxy.fitResults !== 'undefined' && typeof ExGlobals.Constants.proxy.fitResults.redchi2 !== 'undefined') {
            s += '<th align="right">Error</th>'
            s += '<th align="right">Fit</th>'
        }
        s += '</tr>'

        const params = ExGlobals.Constants.proxy.parametersAsObj
        for (let i = 0; i < params.length; i++) {
            const number = params[i].number
            const label = params[i].label
            const value = EaLogic.Utils.toFixed(params[i].value)
            const unit = params[i].unit
            const error = params[i].error === 0. ? "" : EaLogic.Utils.toFixed(params[i].error)
            const fit = params[i].fit === 0 ? "" : "+"
            s += '<tr>'
            s += '<td align="right">' + number + '</td>'
            s += '<td align="left">' + label + '</td>'
            s += '<td align="right">' + value + '</td>'
            s += '<td align="left">' + unit + '</td>'
            if (typeof ExGlobals.Constants.proxy.fitResults !== 'undefined' && typeof ExGlobals.Constants.proxy.fitResults.redchi2 !== 'undefined') {
                s += '<td align="right">' + error + '</td>'
                s += '<td align="right">' + fit + '</td>'
            }
            s += '</tr>'
        }

        s += '</table>'
        return s
    }

    function writeHtmlBody() {
        let s = ''
        s += '<body>'

        s += `<h1>${ExGlobals.Constants.proxy.projectInfoAsJson.name}</h1>`
        s += '<p>'
        s += `<b>Short description:</b> ${ExGlobals.Constants.proxy.projectInfoAsJson.short_description}<br>`
        s += `<b>Structural phases:</b> ${ExGlobals.Constants.proxy.projectInfoAsJson.samples}<br>`
        s += `<b>Experimental data:</b> ${ExGlobals.Constants.proxy.projectInfoAsJson.experiments}<br>`
        s += `<b>Modified:</b> ${ExGlobals.Constants.proxy.projectInfoAsJson.modified}<br>`
        s += '</p>'

        s += '<h2>Software</h2>'
        s += '<p>'
        s += `<b>GUI:</b> <a href="${ExGlobals.Constants.appUrl}">${ExGlobals.Constants.appName} v${ExGlobals.Constants.appVersion}</a><br>`
        s += `<b>Calculation:</b> ${ExGlobals.Constants.proxy.statusModelAsObj.calculation}<br>`
        if (typeof ExGlobals.Constants.proxy.fitResults !== 'undefined' && typeof ExGlobals.Constants.proxy.fitResults.redchi2 !== 'undefined') {
            s += `<b>Minimization:</b> ${ExGlobals.Constants.proxy.statusModelAsObj.minimization}<br>`
            s += `<b>Goodness-of-fit (reduced \u03c7\u00b2):</b> ${ExGlobals.Constants.proxy.fitResults.redchi2.toFixed(2)} <br>`
        }
        s += '</p>'

        s += '<h2>Parameters</h2>'
        s += '<p>'
        s += writeHtmlTable()
        s += '<br>'
        s += '</p>'

        if (typeof ExGlobals.Constants.proxy.fitResults !== 'undefined' && typeof ExGlobals.Constants.proxy.fitResults.redchi2 !== 'undefined') {
            s += '<h2>Fitting</h2>'
        } else {
            s += '<h2>Simulation</h2>'
        }
        s += '<p>'
        s += `<img width="${reportContainer.width-2*textArea.padding}" src="${ExGlobals.Variables.analysisImageSource}">`
        s += '</p>'

        s += '<h2>Structure</h2>'
        s += '<p>'
        s += `<img width="${reportContainer.width-2*textArea.padding}" src="${ExGlobals.Variables.structureImageSource}">`
        s += '</p>'

        s += '</body>'
        return s
    }

    function writeHtml() {
        let s = ''
        s += '<!DOCTYPE html>'
        s += '<html>'
        s += writeHtmlHead()
        s += writeHtmlBody()
        s += '</html>'
        return s
    }

}
