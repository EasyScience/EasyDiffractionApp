import QtQuick 2.13
import QtQuick.Controls 2.13
import QtCharts 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    property bool showMeasured: false
    property bool showDifference: false

    property string xAxisTitle: qsTr("2theta (deg)")
    property string mainYAxisTitle: qsTr("Intensity")
    property string differenceYAxisTitle: qsTr("Difference")

    color: EaStyle.Colors.mainContentBackground

    // Main (top) chart

    EaCharts.ChartView {
        id: topChart

        anchors.top: parent.top
        anchors.bottom: bottomChart.top
        anchors.left: parent.left
        anchors.right: parent.right

        anchors.margins: -12 + EaStyle.Sizes.fontPixelSize * 2
        anchors.bottomMargin: bottomChart.visible ? 0 : anchors.topMargin

        //antialiasing: true

        EaCharts.ValueAxis {
            id: topAxisX

            title: xAxisTitle
            titleVisible: !bottomChart.visible

            labelsVisible: !bottomChart.visible
            labelFormat: xLabelFormat()

            min: ExGlobals.Constants.proxy.qtCharts.analysisXmin
            max: ExGlobals.Constants.proxy.qtCharts.analysisXmax
        }

        EaCharts.ValueAxis {
            id: topAxisY

            title: mainYAxisTitle

            labelFormat: yLabelFormat()

            min: ExGlobals.Constants.proxy.qtCharts.analysisYmin
            max: ExGlobals.Constants.proxy.qtCharts.analysisYmax
        }

        EaCharts.AreaSeries {
            visible: ExGlobals.Constants.proxy.showMeasuredSeries

            color: EaStyle.Colors.chartForegrounds[0]

            axisX: topAxisX
            axisY: topAxisY

            lowerSeries: LineSeries {
                id: measuredLower
                Component.onCompleted: {
                    setDefaultMeasuredLowerSeries()
                    ExGlobals.Constants.proxy.qtCharts.setAnalysisMeasuredLower(measuredLower)
                }
            }

            upperSeries: LineSeries {
                id: measuredUpper
                Component.onCompleted: {
                    setDefaultMeasuredUpperSeries()
                    ExGlobals.Constants.proxy.qtCharts.setAnalysisMeasuredUpper(measuredUpper)
                }
            }
        }

        EaCharts.LineSeries {
            id: calculated

            color: EaStyle.Colors.chartForegrounds[1]

            axisX: topAxisX
            axisY: topAxisY

            Component.onCompleted: {
                setDefaultCalculatedSeries()
                ExGlobals.Constants.proxy.qtCharts.setAnalysisCalculated(calculated)
            }
        }

        onPlotAreaChanged: adjustLeftAxesAnchor()
    }

    // Difference (bottom) chart

    EaCharts.ChartView {
        id: bottomChart

        visible: ExGlobals.Constants.proxy.showDifferenceChart && ExGlobals.Constants.proxy.experimentLoaded

        height: visible ? 0.3 * parent.height : 0

        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        anchors.margins: visible ? -12 + EaStyle.Sizes.fontPixelSize * 2 : 0
        anchors.topMargin: 0

        allowZoom: false
        animationDuration: topChart.animationDuration

        //antialiasing: true

        EaCharts.ValueAxis {
            id: bottomAxisX

            title: xAxisTitle

            labelFormat: xLabelFormat()

            min: topAxisX.min
            max: topAxisX.max

            onMinChanged: {
                if (zeroLine.count === 2)
                    zeroLine.removePoints(0, 1)
                zeroLine.insert(0, min, 0.)
            }
            onMaxChanged: {
                if (zeroLine.count === 2)
                    zeroLine.removePoints(1, 1)
                zeroLine.insert(0, max, 0.)
            }
        }

        EaCharts.ValueAxis {
            id: bottomAxisY

            title: differenceYAxisTitle

            tickType: ValueAxis.TicksFixed
            tickCount: 3

            labelFormat: yLabelFormat()

            min: differenceYRangeMiddle() - differenceYHalfRange() //ExGlobals.Constants.proxy.qtCharts.differenceYmin
            max: differenceYRangeMiddle() + differenceYHalfRange() //ExGlobals.Constants.proxy.qtCharts.differenceYmax
        }

        EaCharts.LineSeries {
            id: zeroLine

            color: EaStyle.Colors.appBorder//EaStyle.Colors.chartForegrounds[1]

            axisX: bottomAxisX
            axisY: bottomAxisY
        }

        EaCharts.AreaSeries {
            color: EaStyle.Colors.chartForegrounds[2]

            axisX: bottomAxisX
            axisY: bottomAxisY

            lowerSeries: LineSeries {
                id: differenceLower
                Component.onCompleted: {
                    setDefaultDifferenceLowerSeries()
                    ExGlobals.Constants.proxy.qtCharts.setAnalysisDifferenceLower(differenceLower)
                }
            }

            upperSeries: LineSeries {
                id: differenceUpper
                Component.onCompleted: {
                    setDefaultDifferenceUpperSeries()
                    ExGlobals.Constants.proxy.qtCharts.setAnalysisDifferenceUpper(differenceUpper)
                }
            }
        }

        onPlotAreaChanged: adjustLeftAxesAnchor()
    }

    // Helpers

    EaElements.Label {
        id: dummyText
        visible: false
    }

    // Logic

    function setDefaultCalculatedSeries() {
        const arrays = ExGlobals.Constants.proxy.qtCharts.arrays
        if (typeof arrays === 'undefined')
            return
        for (let i in arrays.x) {
            calculated.append(arrays.x[i], arrays.yCalc[i])
        }
    }

    function setDefaultMeasuredLowerSeries() {
        const arrays = ExGlobals.Constants.proxy.qtCharts.arrays
        if (typeof arrays === 'undefined')
            return
        for (let i in arrays.x) {
            measuredLower.append(arrays.x[i], arrays.yMeas[i] - arrays.syMeas[i])
        }
    }

    function setDefaultMeasuredUpperSeries() {
        const arrays = ExGlobals.Constants.proxy.qtCharts.arrays
        if (typeof arrays === 'undefined')
            return
        for (let i in arrays.x) {
            measuredUpper.append(arrays.x[i], arrays.yMeas[i] + arrays.syMeas[i])
        }
    }

    function setDefaultDifferenceLowerSeries() {
        const arrays = ExGlobals.Constants.proxy.qtCharts.arrays
        if (typeof arrays === 'undefined')
            return
        for (let i in arrays.x) {
            differenceLower.append(arrays.x[i], arrays.yMeas[i] - arrays.syMeas[i] - arrays.yCalc[i])
        }
    }

    function setDefaultDifferenceUpperSeries() {
        const arrays = ExGlobals.Constants.proxy.qtCharts.arrays
        if (typeof arrays === 'undefined')
            return
        for (let i in arrays.x) {
            differenceUpper.append(arrays.x[i], arrays.yMeas[i] + arrays.syMeas[i] - arrays.yCalc[i])
        }
    }

    function differenceYRangeMiddle() {
        return 0.
        //return (ExGlobals.Constants.proxy.qtCharts.differenceYmax + ExGlobals.Constants.proxy.qtCharts.differenceYmin) * 0.5
    }

    function differenceYHalfRange() {
        if (topChart.plotArea.height === 0 || bottomChart.plotArea.height === 0)
            return 1
        const hightRatio = topChart.plotArea.height / bottomChart.plotArea.height
        const topChartYRange = topAxisY.max - topAxisY.min
        const bottomChartYRange = topChartYRange / hightRatio
        return 0.5 * bottomChartYRange
    }

    function labelFormat(range) {
        if (range < 1)
            return "%.2f"
        else if (range < 10)
            return "%.1f"
        else
            return "%.0f"
    }

    function xLabelFormat() {
        const range = topAxisX.max - topAxisX.min
        return labelFormat(range)
    }

    function yLabelFormat() {
        const topAxisYRange = topAxisY.max - topAxisY.min
        const bottomAxisYRange = bottomAxisY.max - bottomAxisY.min
        const range = Math.min(topAxisYRange, bottomAxisYRange)
        return labelFormat(range)
    }

    function adjustLeftAxesAnchor() {
        let topChartTickMaxWidth = 0.0

        dummyText.text = topAxisY.max.toFixed(0)
        topChartTickMaxWidth = dummyText.width

        dummyText.text = topAxisY.min.toFixed(0)
        if (dummyText.width > topChartTickMaxWidth)
            topChartTickMaxWidth = dummyText.width

        let bottomChartTickMaxWidth = 0.0

        dummyText.text = bottomAxisY.max.toFixed(0)
        bottomChartTickMaxWidth = dummyText.width

        dummyText.text = bottomAxisY.min.toFixed(0)
        if (dummyText.width > bottomChartTickMaxWidth)
            bottomChartTickMaxWidth = dummyText.width

        const defaultLeftMargin = -12 + EaStyle.Sizes.fontPixelSize * 2
        const extraMargin = topChartTickMaxWidth - bottomChartTickMaxWidth

        if (extraMargin > 0) {
            bottomChart.anchors.leftMargin = defaultLeftMargin + extraMargin
        } else {
            topChart.anchors.leftMargin = defaultLeftMargin - extraMargin
        }
    }


}

