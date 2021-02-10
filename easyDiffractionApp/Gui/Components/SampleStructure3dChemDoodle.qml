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

    property string structureChartLibVersion: '9.1.0'
    property string structureChartLibUrl: 'https://web.chemdoodle.com'

    property string structureChartWidth: container.width.toString()
    property string structureChartHeight: container.height.toString()

    property string structureChartBackgroundColor: EaStyle.Colors.chartPlotAreaBackground
    property string structureChartForegroundColor: EaStyle.Colors.themeForeground

    color: structureChartBackgroundColor

    WebEngineView {
        id: webView

        anchors.fill: parent
        backgroundColor: structureChartBackgroundColor
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
        s += '<script type="text/javascript" src="http://easyscience.apptimity.com/easyDiffraction/libs/ChemDoodleWeb-'+structureChartLibVersion+'.js"></script>'
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
        s += structureChart + '\n'
        s += '</script>' + '\n'
        s += '</body>' + '\n'
        s += '\n'
        s += '</html>'
        return s
    }

}
