import QtQuick 2.13
import QtQuick.Controls 2.13
import QtWebEngine 1.10

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Animations 1.0 as EaAnimations
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Logic 1.0 as ExLogic
import Gui.Globals 1.0 as ExGlobals

Item {
    id: container

    property bool isFitting: typeof ExGlobals.Constants.proxy.fitResults.redchi2 !== 'undefined'
    property bool hasPhases: Object.keys(ExGlobals.Constants.proxy.phasesAsObj).length !== 0
    property string htmlBackground: EaStyle.Colors.contentBackground
    property int chartWidth: 520

    // Structure chart

    property string structureChartLibVersion: EaLogic.Plotting.chemDoodleInfo().version
    property string structureChartLibUrl: EaLogic.Plotting.chemDoodleInfo().url

    property int structureChartWidth: chartWidth + EaStyle.Sizes.fontPixelSize * 1.5 * 2
    property int structureChartHeight: structureChartWidth

    property string structureChartBackgroundColor: EaStyle.Colors.chartPlotAreaBackground
    property string structureChartForegroundColor: EaStyle.Colors.themeForeground
    property string structureChartBorderColor: EaStyle.Colors.appBorder

    // Data chart

    property string dataChartLibVersion: EaLogic.Plotting.bokehInfo().version
    property string dataChartLibUrl: EaLogic.Plotting.bokehInfo().url

    property int dataChartWidth: chartWidth
    property int dataChartHeight: chartWidth * 0.87
    property int dataChartPadding: EaStyle.Sizes.fontPixelSize

    property string dataChartBackgroundColor: EaStyle.Colors.chartPlotAreaBackground
    property string dataChartBorderColor: EaStyle.Colors.appBorder

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

        anchors.fill: parent
        backgroundColor: htmlBackground

        onContextMenuRequested: {
            request.accepted = true
        }

        onNavigationRequested: {
            if (request.navigationType === WebEngineNavigationRequest.LinkClickedNavigation) {
                request.action = WebEngineNavigationRequest.IgnoreRequest
                Qt.openUrlExternally(request.url)
            }
        }

        onPdfPrintingFinished: {
            saveConfirmationDialog.success = success
            saveConfirmationDialog.filePath = filePath
            saveConfirmationDialog.open()
        }

        signal htmlExportingFinished(bool success, string filePath)
        onHtmlExportingFinished: {
            saveConfirmationDialog.success = success
            saveConfirmationDialog.filePath = filePath
            saveConfirmationDialog.open()
        }

        Component.onCompleted: {
            ExGlobals.Variables.reportWebView = this
            ExGlobals.Constants.proxy.htmlExportingFinished.connect(htmlExportingFinished)
        }
    }

    EaElements.Dialog {
        id: saveConfirmationDialog

        property bool success: false
        property string filePath: 'undefined'

        visible: false
        title: qsTr("Save confirmation")

        parent: Overlay.overlay

        x: (parent.width - width) * 0.5
        y: (parent.height - height) * 0.5

        modal: true
        standardButtons: Dialog.Ok

        Row {
            padding: EaStyle.Sizes.fontPixelSize
            spacing: EaStyle.Sizes.fontPixelSize * 0.75

            EaElements.Label {
                anchors.verticalCenter: parent.verticalCenter
                font.family: EaStyle.Fonts.iconsFamily
                font.pixelSize: EaStyle.Sizes.fontPixelSize * 1.25
                text: saveConfirmationDialog.success ? 'check-circle' : 'minus-circle'
            }

            EaElements.Label {
                anchors.verticalCenter: parent.verticalCenter
                text: saveConfirmationDialog.success
                      ? qsTr('File "<a href="%1">%1</a>" is successfully saved'.arg(saveConfirmationDialog.filePath))
                      : qsTr('Failed to save file "%1"'.arg(saveConfirmationDialog.filePath))
            }
        }
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

    property string headScripts: {
        const list = [
                  EaLogic.Plotting.bokehHeadScripts(),
                  EaLogic.Plotting.chemDoodleHeadScripts()
              ]
        return list.join('\n')
    }

    property string dataChartStyle: {
        const list = [
                  '.bk-logo {',
                  '    display: none !important;',
                  '}',
                  '.bk-toolbar.bk-above  {',
                  `    position: absolute;`,
                  `    z-index: 1;`,
                  `    top: ${0.5 * EaStyle.Sizes.fontPixelSize}px;`,
                  `    right: ${1.5 * EaStyle.Sizes.fontPixelSize}px;`,
                  '}',
                  '#analysisSection {',
                  `    height: ${dataChartHeight}px;`,
                  `    width: ${dataChartWidth}px;`,
                  `    padding: ${dataChartPadding}px;`,
                  `    background-color: ${dataChartBackgroundColor};`,
                  `    border: 1px solid ${dataChartBorderColor};`,
                  '}'
              ]
        return list.join('\n')
    }

    property string structureChartStyle: {
        const list = [
                  'canvas.ChemDoodleWebComponent {',
                  `    border: 1px solid ${structureChartBorderColor};`,
                  '}'
              ]
        return list.join('\n')
    }

    property string headMiscStyle: {
        const list = [
                  'html {',
                  `    background-color: ${htmlBackground};`,
                  '}',
                  'body {',
                  '    font-family: "PT Sans", sans-serif;',
                  `    font-size: ${EaStyle.Sizes.fontPixelSize}px;`,
                  `    padding: ${EaStyle.Sizes.fontPixelSize}px;`,
                  `    color: ${EaStyle.Colors.themeForeground};`,
                  '}',
                  'article {',
                  `    width: ${structureChartWidth}px;`,
                  '    margin: 0 auto;',
                  '}',
                  'h2 {',
                  `    margin-top: ${EaStyle.Sizes.fontPixelSize * 3}px;`,
                  '}',
                  'a {',
                  '    text-decoration: underline;',
                  '}',
                  'a, a:visited {',
                  `    color: ${EaStyle.Colors.link};`,
                  '}',
                  'a:hover {',
                  `    color: ${EaStyle.Colors.linkHovered};`,
                  '}',
                  '#parametersSection table {',
                  '    border-collapse: collapse;',
                  '}',
                  '#parametersSection td, th {',
                  `    border: 1px solid ${EaStyle.Colors.appBorder};`,
                  '    padding: 2px;',
                  '    padding-left: 12px;',
                  '    padding-right: 12px;',
                  '}',
                  '#parametersSection tr:nth-child(odd) {',
                  `    background-color: ${EaStyle.Colors.chartPlotAreaBackground};`,
                  '}',
                  '#parametersSection tr:nth-child(even) {',
                  `    background-color: ${htmlBackground};`,
                  '}'
              ]
        return list.join('\n')
    }

    property string headStyle: {
        const list = [
                  '<style type="text/css">',
                  dataChartStyle,
                  structureChartStyle,
                  headMiscStyle,
                  '</style>'
              ]
        return list.join('\n')
    }

    property string head: {
        const list = [
                  EaLogic.Plotting.headCommon(),
                  headScripts,
                  headStyle
              ]
        return list.join('\n')
    }

    property string structureChart:
        EaLogic.Plotting.chemDoodleChart(
            // cif
            JSON.stringify(ExGlobals.Constants.proxy.phasesAsExtendedCif),
            // specs
            {
                chartWidth: structureChartWidth,
                chartHeight: structureChartHeight,
                chartForegroundColor: structureChartForegroundColor,
                chartBackgroundColor: structureChartBackgroundColor
            }
            )

    property string dataChart:
        EaLogic.Plotting.bokehChart(
            // data
            {
                measured: ExGlobals.Constants.proxy.bokeh.measuredDataObj,
                calculated: ExGlobals.Constants.proxy.bokeh.calculatedDataObj,
                bragg: ExGlobals.Constants.proxy.bokeh.braggDataObj,
                difference: ExGlobals.Constants.proxy.bokeh.differenceDataObj,
                ranges: ExGlobals.Variables.analysisChart.plotRanges,

                hasMeasured: ExGlobals.Variables.analysisChart.hasMeasuredData,
                hasCalculated: ExGlobals.Variables.analysisChart.hasCalculatedData,
                hasBragg: ExGlobals.Variables.analysisChart.hasBraggData,
                hasDifference: ExGlobals.Variables.analysisChart.hasDifferenceData,
                hasPlotRanges: ExGlobals.Variables.analysisChart.hasPlotRangesData
            },
            // specs
            {
                chartWidth: dataChartWidth, //dataChartWidth,
                mainChartHeight: ExGlobals.Variables.analysisChart.mainChartHeight * 0.7,
                braggChartHeight: ExGlobals.Variables.analysisChart.braggChartHeight,
                differenceChartHeight: ExGlobals.Variables.analysisChart.differenceChartHeight * 0.7,
                xAxisChartHeight: ExGlobals.Variables.analysisChart.xAxisChartHeight,

                xAxisTitle: ExGlobals.Variables.analysisChart.xAxisTitle,
                yMainAxisTitle: ExGlobals.Variables.analysisChart.yMainAxisTitle,
                yDifferenceAxisTitle: ExGlobals.Variables.analysisChart.yDifferenceAxisTitle,

                chartBackgroundColor: ExGlobals.Variables.analysisChart.chartBackgroundColor,
                chartForegroundColor: ExGlobals.Variables.analysisChart.chartForegroundColor,
                chartGridLineColor: ExGlobals.Variables.analysisChart.chartGridLineColor,
                chartMinorGridLineColor: ExGlobals.Variables.analysisChart.chartMinorGridLineColor,

                measuredLineColor: ExGlobals.Variables.analysisChart.measuredLineColor,
                measuredAreaColor: ExGlobals.Variables.analysisChart.measuredAreaColor,
                calculatedLineColor: ExGlobals.Variables.analysisChart.calculatedLineColor,
                braggTicksColor: ExGlobals.Variables.analysisChart.braggTicksColor,
                differenceLineColor: ExGlobals.Variables.analysisChart.differenceLineColor,
                differenceAreaColor: ExGlobals.Variables.analysisChart.differenceAreaColor,

                measuredLineWidth: ExGlobals.Variables.analysisChart.measuredLineWidth,
                calculatedLineWidth: ExGlobals.Variables.analysisChart.calculatedLineWidth,
                differenceLineWidth: ExGlobals.Variables.analysisChart.differenceLineWidth,

                fontPixelSize: ExGlobals.Variables.analysisChart.fontPixelSize,

                containerId: "analysisSection"
            }
            )

    property string parametersTable: {
        let list = []
        // header
        const hlist = [
                        '<tr>',
                        '<th align="right">No.</th>',
                        '<th align="left">Parameter</th>',
                        '<th align="right">Value</th>',
                        '<th align="left">Units</th>'
                    ]
        if (isFitting) {
            hlist.push('<th align="right">Error</th>')
        }
        hlist.push('</tr>')
        list.push(hlist.join(' '))
        // data
        const params = ExGlobals.Constants.proxy.parametersAsObj
        for (let i = 0; i < params.length; i++) {
            const number = params[i].number
            const label = params[i].label.replace('.point_background', '')
            const value = EaLogic.Utils.toFixed(params[i].value)
            const unit = params[i].unit
            const error = params[i].error === 0. ? "" : EaLogic.Utils.toFixed(params[i].error)
            const dlist = [
                            '<tr>',
                            '<td align="right">' + number + '</td>',
                            '<td align="left">' + label + '</td>',
                            '<td align="right">' + value + '</td>',
                            '<td align="left">' + unit + '</td>'
                        ]
            if (isFitting) {
                dlist.push('<td align="right">' + error + '</td>')
            }
            dlist.push('</tr>')
            list.push(dlist.join(' '))
        }
        return list.join('\n')
    }

    property string projectSection: {
        if (!hasPhases)
            return ''
        const projectDescription = ExGlobals.Constants.proxy.projectInfoAsJson.short_description
        const phaseName = ExGlobals.Constants.proxy.phasesAsObj[0].name
        const datasetName = 'D1A@ILL'
        const modifiedDate = ExGlobals.Constants.proxy.projectInfoAsJson.modified
        const list = [
                `<h1>${ExGlobals.Constants.proxy.projectInfoAsJson.name}</h1>`,
                '<p>',
                `<b>Short description:</b> ${projectDescription}<br>`,
                `<b>Structural phases:</b> ${phaseName}<br>`,
                `<b>Experimental data:</b> ${datasetName}<br>`,
                `<b>Modified:</b> ${modifiedDate}<br>`,
                '</p>'
              ]
        return list.join('\n')
    }

    property string minimizationSoftware: {
        if (!isFitting)
            return ''
        const soft = ExGlobals.Constants.proxy.statusModelAsObj.minimization
        let list = [
                `<b>Minimization:</b> ${soft}<br>`
            ]
        return list.join('\n')
    }

    property string softwareSection: {
        const list = [
                  '<h2>Software</h2>',
                  '<div id="softwareSection">',
                  `<b>Analysis:</b> <a href="${ExGlobals.Constants.appUrl}">${ExGlobals.Constants.appName} v${ExGlobals.Constants.appVersion}</a><br>`,
                  `<b>Structure chart:</b> <a href="${structureChartLibUrl}"> ChemDoodle v${structureChartLibVersion}</a><br>`,
                  `<b>Data chart:</b> <a href="${dataChartLibUrl}"> Bokeh v${dataChartLibVersion}</a><br>`,
                  minimizationSoftware,
                  '</div>'
              ]
        return list.join('\n')
    }

    property string structureSection: {
        if (!hasPhases)
            return ''
        const phase = ExGlobals.Constants.proxy.phasesAsObj[0]
        const phaseName = phase.name
        const spaceGroup = phase.spacegroup._space_group_HM_name.value
        const list = [
                  `<h2>Structure: ${phaseName}</h2>`,
                  '<p>',
                  `<b>Space group:</b> ${spaceGroup}<br>`,
                  '</p>',
                  '<div id="structureSection">',
                  '<script>',
                  structureChart,
                  '</script>',
                  '</div>'
              ]
        return list.join('\n')
    }

    property string fittingInfo: {
        if (!isFitting)
            return ''
        const redchi2 = ExGlobals.Constants.proxy.fitResults.redchi2.toFixed(2)
        let list = [
                '<p>',
                `<b>Goodness-of-fit (reduced \u03c7\u00b2):</b> ${redchi2}<br>`,
                '</p>'
            ]
        return list.join('\n')
    }

    property string analysisSection: {
        let list = [
                '<h2>Simulation/Fitting</h2>',
                fittingInfo,
                '<div id="analysisSection">',
                '<script>',
                dataChart,
                '</script>',
                '</div>'
            ]
        return list.join('\n')
    }

    property string parametersSection: {
        const list = [
                  '<h2>Parameters</h2>',
                  '<div id="parametersSection">',
                  '<table>',
                  parametersTable,
                  '</table>',
                  '</div>'
              ]
        return list.join('\n')
    }

    property string article: {
        const list = [
                  projectSection + '\n',
                  softwareSection + '\n',
                  structureSection + '\n',
                  analysisSection + '\n',
                  parametersSection
              ]
              return list.join('\n')
    }

    property string html: {
        const list = [
                  '<!DOCTYPE html>',
                  '<html>\n',
                  '<head>\n',
                  head+'\n',
                  '</head>\n',
                  '<body>\n',
                  '<article>\n',
                  article+'\n',
                  '</article>\n',
                  '</body>\n',
                  '</html>'
              ]
        return list.join('\n')
    }

}


