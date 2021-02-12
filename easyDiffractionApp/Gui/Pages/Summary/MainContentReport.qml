import QtQuick 2.13
import QtQuick.Controls 2.13
import QtWebEngine 1.10

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Animations 1.0 as EaAnimations
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Item {
    id: container

    property bool isFitting: typeof ExGlobals.Constants.proxy.fitResults.redchi2 !== 'undefined'
    property string htmlBackground: EaStyle.Colors.contentBackground
    property int chartWidth: 520

    // Structure chart

    property string structureChartLibVersion: '9.1.0'
    property string structureChartLibUrl: 'https://web.chemdoodle.com'

    property string structureChartWidth: (chartWidth + EaStyle.Sizes.fontPixelSize * 1.5 * 2).toString()
    property string structureChartHeight: structureChartWidth

    property string structureChartBackgroundColor: EaStyle.Colors.chartPlotAreaBackground
    property string structureChartForegroundColor: EaStyle.Colors.themeForeground
    property string structureChartBorderColor: EaStyle.Colors.appBorder

    // Data chart

    property string dataChartLibVersion: '2.2.3'
    property string dataChartLibUrl: 'https://docs.bokeh.org/en/' + dataChartLibVersion

    property string dataChartWidth: chartWidth.toString()
    property string dataChartHeight: (chartWidth / 5 * 4).toString()

    property var calculatedData: ExGlobals.Constants.proxy.bokeh.calculatedDataObj
    property var measuredData: ExGlobals.Constants.proxy.bokeh.measuredDataObj
    property bool hasMeasuredData: Object.keys(measuredData).length

    property string xAxisTitle: qsTr("2theta (deg)")
    property string yAxisTitle: qsTr("Intensity")

    property string dataChartBackgroundColor: EaStyle.Colors.chartPlotAreaBackground
    property string dataChartBorderColor: EaStyle.Colors.appBorder
    property string dataChartPadding: (EaStyle.Sizes.fontPixelSize * 1.5).toString()

    property string experimentLineColor: EaStyle.Colors.chartForegrounds[0]
    property string experimentLineWidth: '2'
    property string calculatedLineColor: EaStyle.Colors.chartForegrounds[1]
    property string calculatedLineWidth: '2'

    /*
    ScrollView {
        anchors.fill: parent
        contentHeight: webView.contentsSize.height
        contentWidth: webView.contentsSize.width
        focus: true
        ScrollBar.vertical.policy: ScrollBar.AlwaysOn
    */

    WebEngineView {
        id: webView
        enabled: false

        anchors.fill: parent
        backgroundColor: htmlBackground

        Component.onCompleted: ExGlobals.Variables.reportWebView = webView
    }

    //}

    onHtmlChanged: {
        //print(html)
        ExGlobals.Constants.proxy.setReport(html)
        webView.loadHtml(html)
    }

    /////////////
    // HTML parts
    /////////////

    property string headMisc: {
        let s = ''
        s += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
        return s
    }

    property string dataChartLib: {
        let s = ''
        s += '<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-'+dataChartLibVersion+'.min.js"></script>' + '\n'
        s += '<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-widgets-'+dataChartLibVersion+'.min.js"></script>' + '\n'
        s += '<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-tables-'+dataChartLibVersion+'.min.js"></script>' + '\n'
        s += '<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-api-'+dataChartLibVersion+'.min.js"></script>'
        return s
    }

    property string structureChartLib: {
        let s = ''
        s += '<script type="text/javascript" src="http://easyscience.apptimity.com/easyDiffraction/libs/ChemDoodleWeb-'+structureChartLibVersion+'.js"></script>'
        return s
    }

    property string headScripts: {
        let s = ''
        s += dataChartLib + '\n'
        s += structureChartLib
        return s
    }

    property string dataChartStyle: {
        let s = ''
        s += '.bk-logo {' + '\n'
        s += '    display: none !important;' + '\n'
        s += '}' + '\n'
        s += '#analysisSection {' + '\n'
        s += '    height: '+dataChartHeight+'px;' + '\n'
        s += '    width: '+dataChartWidth+'px;' + '\n'
        s += '    padding: '+dataChartPadding+'px;' + '\n'
        s += '    background-color: '+dataChartBackgroundColor+';' + '\n'
        s += '    border: 1px solid '+dataChartBorderColor+';' + '\n'
        s += '}'
        return s
    }

    property string structureChartStyle: {
        let s = ''
        s += 'canvas.ChemDoodleWebComponent {' + '\n'
        s += '    border: 1px solid '+structureChartBorderColor+';' + '\n'
        s += '}'
        return s
    }

    property string headMiscStyle: {
        let s = ''
        s += 'html {' + '\n'
        s += '    background-color: '+htmlBackground+';' + '\n'
        s += '}' + '\n'
        s += 'body {' + '\n'
        s += '    padding: '+(EaStyle.Sizes.fontPixelSize).toString()+'px;' + '\n'
        s += '    color: '+EaStyle.Colors.themeForeground+';' + '\n'
        s += '}' + '\n'
        s += 'article {' + '\n'
        s += '    width: '+structureChartWidth+'px;' + '\n'
        s += '    margin: 0 auto;' + '\n'
        s += '}' + '\n'
        s += 'h2 {' + '\n'
        s += '    margin-top: '+(EaStyle.Sizes.fontPixelSize * 3).toString()+'px;' + '\n'
        s += '}' + '\n'
        s += 'a:link {' + '\n'
        s += '    color: '+EaStyle.Colors.themeAccent+';' + '\n'
        s += '}' + '\n'
        s += 'table {' + '\n'
        s += '    border-collapse: collapse;' + '\n'
        s += '}' + '\n'
        s += 'td, th {' + '\n'
        s += '    border: 1px solid '+EaStyle.Colors.appBorder+';' + '\n'
        s += '    padding: 2px;' + '\n'
        s += '    padding-left: 12px;' + '\n'
        s += '    padding-right: 12px;' + '\n'
        s += '}' + '\n'
        s += 'tr:nth-child(odd) {' + '\n'
        s += '    background-color:'+EaStyle.Colors.chartPlotAreaBackground+';' + '\n'
        s += '}'
        s += 'tr:nth-child(even) {' + '\n'
        s += '    background-color:'+htmlBackground+';' + '\n'
        s += '}'
        return s
    }

    property string headStyle: {
        let s = ''
        s += '<style type="text/css">' + '\n'
        s += dataChartStyle + '\n'
        s += structureChartStyle +'\n'
        s += headMiscStyle + '\n'
        s += '</style>'
        return s
    }

    property string head: {
        let s = ''
        s += '\n'
        s += headMisc + '\n'
        s += '\n'
        s += headScripts + '\n'
        s += '\n'
        s += headStyle
        return s
    }

    property string structureChart: {
        let s = ''
        s += 'const cifStr = '+JSON.stringify(ExGlobals.Constants.proxy.phasesAsExtendedCif)+'' + '\n'
        s += 'const xSuper = 1' + '\n'
        s += 'const ySuper = 1' + '\n'
        s += 'const zSuper = 1' + '\n'
        s += 'const phase = ChemDoodle.readCIF(cifStr, xSuper, ySuper, zSuper)' + '\n'
        s += 'const crystalTransformer = new ChemDoodle.TransformCanvas3D("crystalTransformer", '+structureChartWidth+', '+structureChartHeight+')' + '\n'
        s += 'crystalTransformer.styles.set3DRepresentation("Ball and Stick")' + '\n'
        s += 'crystalTransformer.styles.projectionPerspective_3D = true' + '\n'
        s += 'crystalTransformer.styles.projectionPerspectiveVerticalFieldOfView_3D = 20' + '\n'
        s += 'crystalTransformer.styles.bonds_display = true' + '\n'
        s += 'crystalTransformer.styles.bonds_splitColor = true' + '\n'
        s += 'crystalTransformer.styles.atoms_displayLabels_3D = true' + '\n'
        s += 'crystalTransformer.styles.compass_display = true' + '\n'
        s += 'crystalTransformer.styles.compass_type_3D = 0' + '\n'
        s += 'crystalTransformer.styles.compass_size_3D = 70' + '\n'
        s += 'crystalTransformer.styles.compass_displayText_3D = true' + '\n'
        s += 'crystalTransformer.styles.shapes_color = "'+structureChartForegroundColor+'"' + '\n'
        //s += 'crystalTransformer.styles.shapes_lineWidth = 5' + '\n'
        s += 'crystalTransformer.styles.text_font_size = 12' + '\n'
        s += 'crystalTransformer.styles.text_font_families = ["Helvetica", "Arial", "Dialog"]' + '\n'
        s += 'crystalTransformer.styles.backgroundColor = "'+structureChartBackgroundColor+'"' + '\n'
        s += 'crystalTransformer.loadContent([phase.molecule],[phase.unitCell])'
        return s
    }

    property string dataChart: {
        let s = ''
        s += 'const plot = Bokeh.Plotting.figure({' + '\n'
        s += '    tools: "pan,box_zoom,hover,reset",' + '\n'
        s += '    height: '+dataChartHeight+',' + '\n'
        s += '    width: '+dataChartWidth+',' + '\n'
        s += '    x_axis_label: "'+xAxisTitle+'",' + '\n'
        s += '    y_axis_label: "'+yAxisTitle+'",' + '\n'
        s += '    background: "'+dataChartBackgroundColor+'",' + '\n'
        s += '    background_fill_color: "'+dataChartBackgroundColor+'",' + '\n'
        s += '    border_fill_color: "'+dataChartBackgroundColor+'",' + '\n'
        s += '})' + '\n'
        s += 'plot.x_range.range_padding = 0' + '\n'
        if (hasMeasuredData) {
            s += 'const experimentSource = new Bokeh.ColumnDataSource({' + '\n'
            s += '    data: {' + '\n'
            s += '        x: '+measuredData.x+',' + '\n'
            s += '        y: '+measuredData.y+'' + '\n'
            s += '    }' + '\n'
            s += '})' + '\n'
            s += 'const experimentLine = new Bokeh.Line({' + '\n'
            s += '    x: { field: "x" },' + '\n'
            s += '    y: { field: "y" },' + '\n'
            s += '    line_color: "'+experimentLineColor+'",' + '\n'
            s += '    line_width: '+experimentLineWidth+',' + '\n'
            s += '})' + '\n'
            s += 'plot.add_glyph(experimentLine, experimentSource)' + '\n'
        }
        s += 'const calculatedSource = new Bokeh.ColumnDataSource({' + '\n'
        s += '    data: {' + '\n'
        s += '        x: '+calculatedData.x+',' + '\n'
        s += '        y: '+calculatedData.y+'' + '\n'
        s += '    }' + '\n'
        s += '})' + '\n'
        s += 'const calculatedLine = new Bokeh.Line({' + '\n'
        s += '    x: { field: "x" },' + '\n'
        s += '    y: { field: "y" },' + '\n'
        s += '    line_color: "'+calculatedLineColor+'",' + '\n'
        s += '    line_width: '+calculatedLineWidth+',' + '\n'
        s += '})' + '\n'
        s += 'plot.add_glyph(calculatedLine, calculatedSource)' + '\n'
        s += 'Bokeh.Plotting.show(plot, "#analysisSection")'
        return s
    }

    property string parametersTable: {
        let s = ''
        s += '<tr>'
        s += '<th align="right">No.</th>'
        s += '<th align="left">Parameter</th>'
        s += '<th align="right">Value</th>'
        s += '<th align="left">Units</th>'
        if (isFitting) {
            s += '<th align="right">Error</th>'
        //    s += '<th align="right">Fit</th>'
        }
        s += '</tr>'
        const params = ExGlobals.Constants.proxy.parametersAsObj
        for (let i = 0; i < params.length; i++) {
            const number = params[i].number
            const label = params[i].label.replace('.point_background', '')
            const value = EaLogic.Utils.toFixed(params[i].value)
            const unit = params[i].unit
            const error = params[i].error === 0. ? "" : EaLogic.Utils.toFixed(params[i].error)
            const fit = params[i].fit === 0 ? "" : "+"
            s += '\n'
            s += '<tr>'
            s += '<td align="right">' + number + '</td>'
            s += '<td align="left">' + label + '</td>'
            s += '<td align="right">' + value + '</td>'
            s += '<td align="left">' + unit + '</td>'
            if (isFitting) {
                s += '<td align="right">' + error + '</td>'
            //    s += '<td align="right">' + fit + '</td>'
            }
            s += '</tr>'
        }
        return s
    }

    property string projectSection: {
        let s = ''
        s += '<h1>'+ExGlobals.Constants.proxy.projectInfoAsJson.name+'</h1>' + '\n'
        s += '<p>' + '\n'
        s += '<b>Short description:</b> '+ExGlobals.Constants.proxy.projectInfoAsJson.short_description+'<br>' + '\n'
        if (Object.keys(ExGlobals.Constants.proxy.phasesAsObj).length)
            s += '<b>Structural phases:</b> '+ExGlobals.Constants.proxy.phasesAsObj[0].name+'<br>' + '\n'
        s += '<b>Experimental data:</b> '+'D1A@ILL'+'<br>' + '\n'
        s += '<b>Modified:</b> '+ExGlobals.Constants.proxy.projectInfoAsJson.modified+'<br>' + '\n'
        s += '</p>'
        return s
    }

    property string softwareSection: {
        let s = ''
        s += '<h2>Software</h2>' + '\n'
        s += '<div id="softwareSection">' + '\n'
        s += '<b>Analysis:</b> <a href="'+ExGlobals.Constants.appUrl+'">'+ExGlobals.Constants.appName+' v'+ExGlobals.Constants.appVersion+'</a><br>' + '\n'
        s += '<b>Structure chart:</b> <a href="'+structureChartLibUrl+'"> ChemDoodle v'+structureChartLibVersion+'</a><br>' + '\n'
        s += '<b>Data chart:</b> <a href="'+dataChartLibUrl+'"> Bokeh v'+dataChartLibVersion+'</a><br>' + '\n'
        if (isFitting) {
            s += '<b>Minimization:</b> '+ExGlobals.Constants.proxy.statusModelAsObj.minimization+'<br>' + '\n'
        }
        s += '</div>'
        return s
    }

    property string structureSection: {
        let s = ''
        if (Object.keys(ExGlobals.Constants.proxy.phasesAsObj).length) {
            s += '<h2>Structure: '+ExGlobals.Constants.proxy.phasesAsObj[0].name+'</h2>' + '\n'
            s += '<p>' + '\n'
            s += '<b>Space group:</b> '+ExGlobals.Constants.proxy.phasesAsObj[0].spacegroup._space_group_HM_name.value+'<br>' + '\n'
            s += '</p>'
        }
        s += '<div id="structureSection">' + '\n'
        s += '<script>' + '\n'
        s += structureChart + '\n'
        s += '</script>' + '\n'
        s += '</div>'
        return s
    }

    property string analysisSection: {
        let s = ''
        s += '<h2>Simulation/Fitting</h2>' + '\n'
        if (isFitting) {
            s += '<p>' + '\n'
            s += '<b>Goodness-of-fit (reduced \u03c7\u00b2):</b> '+ExGlobals.Constants.proxy.fitResults.redchi2.toFixed(2)+'<br>' + '\n'
            s += '</p>'
        }
        s += '<div id="analysisSection">' + '\n'
        s += '</div>' + '\n'
        s += '<script>' + '\n'
        s += dataChart + '\n'
        s += '</script>'
        return s
    }

    property string parametersSection: {
        let s = ''
        s += '<h2>Parameters</h2>' + '\n'
        s += '<div id="parametersSection">' + '\n'
        s += '<table>' + '\n'
        s += parametersTable + '\n'
        s += '</table>' + '\n'
        s += '</div>'
        return s
    }

    property string article: {
        let s = ''
        s += projectSection + '\n'
        s += '\n'
        s += softwareSection + '\n'
        s += '\n'
        s += structureSection + '\n'
        s += '\n'
        s += analysisSection + '\n'
        s += '\n'
        s += parametersSection
        return s
    }

    property string html: {
        let s = ''
        s += '<!DOCTYPE html>' + '\n'
        s += '<html>' + '\n'
        s += '\n'
        s += '<head>' + '\n'
        s += head + '\n'
        s += '\n'
        s += '</head>' + '\n'
        s += '\n'
        s += '<body>' + '\n'
        s += '<article>' + '\n'
        s += '\n'
        s += article + '\n'
        s += '\n'
        s += '</article>' + '\n'
        s += '</body>' + '\n'
        s += '\n'
        s += '</html>'
        return s
    }

}


