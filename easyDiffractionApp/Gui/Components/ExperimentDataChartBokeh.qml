import QtQuick 2.13
import QtQuick.Controls 2.13
import QtWebEngine 1.10

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Animations 1.0 as EaAnimations
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    id: container

    property string dataChartLibVersion: '2.2.3'
    property string dataChartLibUrl: 'https://docs.bokeh.org/en/' + dataChartLibVersion

    property string dataChartWidth: (container.width - webView.anchors.margins * 2).toString()
    property string dataChartHeight: (container.height - webView.anchors.margins * 2).toString()

    property var calculatedData: ExGlobals.Constants.proxy.bokeh.calculatedDataObj
    property var measuredData: ExGlobals.Constants.proxy.bokeh.measuredDataObj

    property string xAxisTitle: qsTr("2theta (deg)")
    property string yAxisTitle: qsTr("Intensity")

    property string dataChartBackgroundColor: EaStyle.Colors.chartPlotAreaBackground
    property string dataChartBorderColor: EaStyle.Colors.appBorder
    property string dataChartPadding: (EaStyle.Sizes.fontPixelSize * 1.5).toString()

    property string experimentLineColor: EaStyle.Colors.chartForegrounds[0]
    property string calculatedLineColor: EaStyle.Colors.chartForegrounds[1]

    property string experimentLineWidth: '2'
    property string calculatedLineWidth: '2'

    color: dataChartBackgroundColor

    WebEngineView {
        id: webView

        anchors.fill: parent
        anchors.margins: EaStyle.Sizes.fontPixelSize * 1.5
        backgroundColor: dataChartBackgroundColor
    }

    onHtmlChanged: webView.loadHtml(html)

    // HTML parts

    property string headMisc: {
        let s = ''
        s += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
        return s
    }

    property string headScripts: {
        let s = ''
        s += '<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-'+dataChartLibVersion+'.min.js"></script>' + '\n'
        s += '<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-widgets-'+dataChartLibVersion+'.min.js"></script>' + '\n'
        s += '<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-tables-'+dataChartLibVersion+'.min.js"></script>' + '\n'
        s += '<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-api-'+dataChartLibVersion+'.min.js"></script>'
        return s
    }

    property string headStyle: {
        let s = ''
        s += '<style type="text/css">' + '\n'
        s += '* { ' + '\n'
        s += '    margin: 0;' + '\n'
        s += '    padding: 0;' + '\n'
        s += '    box-sizing: border-box;' + '\n'
        s += '}' + '\n'
        s += 'body {' + '\n'
        s += '    overflow: hidden;' + '\n'
        s += '}' + '\n'
        s += '.bk-logo {' + '\n'
        s += '    display: none !important;' + '\n'
        s += '}' + '\n'
        s += '</style>'
        return s
    }

    property string head: {
        let s = ''
        s += headMisc + '\n'
        s += headScripts + '\n'
        s += headStyle
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
        s += 'Bokeh.Plotting.show(plot)'
        return s
    }

    property string html: {
        let s = ''
        s += '<!DOCTYPE html>' + '\n'
        s += '<html>' + '\n'
        s += '\n'
        s += '<head>' + '\n'
        s += head + '\n'
        s += '</head>' + '\n'
        s += '\n'
        s += '<body>' + '\n'
        s += '<script>' + '\n'
        s += dataChart + '\n'
        s += '</script>' + '\n'
        s += '</body>' + '\n'
        s += '\n'
        s += '</html>'
        return s
    }

}


