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

    property string structureChartLibVersion: '8.0.0'
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
        s += 'const crystalTransformer = new ChemDoodle.TransformCanvas3D("crystalTransformer", '+structureChartWidth+', '+structureChartHeight+')' + '\n'
        s += 'crystalTransformer.specs.set3DRepresentation("Ball and Stick")' + '\n'
        s += 'crystalTransformer.specs.projectionPerspective_3D = true' + '\n'
        s += 'crystalTransformer.specs.projectionPerspectiveVerticalFieldOfView_3D = 20' + '\n'
        s += 'crystalTransformer.specs.atoms_displayLabels_3D = true' + '\n'
        //s += 'crystalTransformer.specs.atoms_font_size_2D = 10' + '\n'
        //s += 'crystalTransformer.specs.bonds_display = false' + '\n'
        s += 'crystalTransformer.specs.crystals_unitCellLineWidth = 1.5' + '\n'
        s += 'crystalTransformer.specs.compass_display = true' + '\n'
        s += 'crystalTransformer.specs.compass_type_3D = 0' + '\n' // 0 or 1
        s += 'crystalTransformer.specs.compass_size_3D = 70' + '\n' // default: 50
        s += 'crystalTransformer.specs.compass_displayText_3D = true' + '\n'
        s += 'crystalTransformer.specs.backgroundColor = "'+structureChartBackgroundColor+'"' + '\n'
        s += 'crystalTransformer.specs.shapes_color = "'+structureChartForegroundColor+'"' + '\n'
        s += 'const phase = ChemDoodle.readCIF('+JSON.stringify(ExGlobals.Constants.proxy.phasesAsExtendedCif)+', 1, 1, 1)' + '\n' // (1,1,1)-cell
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
