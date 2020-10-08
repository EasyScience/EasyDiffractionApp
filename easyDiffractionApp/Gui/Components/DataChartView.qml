import QtQuick 2.13
import QtQuick.Controls 2.13
import QtCharts 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    property bool showMeasured: false
    property bool showCalculated: false
    property bool showDifference: false

    color: EaStyle.Colors.mainContentBackground

    EaCharts.ChartView {
        anchors.fill: parent

        EaCharts.ValueAxis {
            id: axisX

            title: "Time (s)"

            tickCount: 4

            min: 0
            max: Math.PI * (tickCount - 1)
        }

        EaCharts.ValueAxis {
            id: axisY

            title: "Signal (arb. units)"

            min: -6
            max: 6
        }

        EaCharts.AreaSeries {
            visible: showMeasured

            axisX: axisX
            axisY: axisY

            lowerSeries: LineSeries {
                id: lowerMeasuredSeries

                // defult points
                XYPoint { x: 0; y: -3.8 }
                XYPoint { x: 1; y: -2.7 }
                XYPoint { x: 2; y:  0.2 }
                XYPoint { x: 3; y:  2.1 }
                XYPoint { x: 4; y:  3.2 }
                XYPoint { x: 5; y:  2.2 }
                XYPoint { x: 6; y:  0.1 }
                XYPoint { x: 7; y: -2.3 }
                XYPoint { x: 8; y: -3.6 }
                XYPoint { x: 9; y: -2.7 }
                XYPoint { x: 9.4; y: -2.2 }

                Component.onCompleted: ExGlobals.Constants.proxy.addLowerMeasuredSeriesRef(lowerMeasuredSeries)
            }

            upperSeries: LineSeries {
                id: upperMeasuredSeries

                // defult points
                XYPoint { x: 0; y: -3.2 }
                XYPoint { x: 1; y: -2.1 }
                XYPoint { x: 2; y:  0.6 }
                XYPoint { x: 3; y:  2.8 }
                XYPoint { x: 4; y:  3.7 }
                XYPoint { x: 5; y:  2.5 }
                XYPoint { x: 6; y:  0.7 }
                XYPoint { x: 7; y: -2.1 }
                XYPoint { x: 8; y: -3.1 }
                XYPoint { x: 9; y: -2.2 }
                XYPoint { x: 9.4; y: -2.0 }

                Component.onCompleted: ExGlobals.Constants.proxy.addUpperMeasuredSeriesRef(upperMeasuredSeries)
            }
        }

        EaCharts.LineSeries {
            id: calculatedSeries

            visible: showCalculated

            axisX: axisX
            axisY: axisY

            // defult points
            XYPoint { x: 0; y: -3 }
            XYPoint { x: 1; y: -2 }
            XYPoint { x: 2; y:  0 }
            XYPoint { x: 3; y:  2 }
            XYPoint { x: 4; y:  3 }
            XYPoint { x: 5; y:  2 }
            XYPoint { x: 6; y:  0 }
            XYPoint { x: 7; y: -2 }
            XYPoint { x: 8; y: -3 }
            XYPoint { x: 9; y: -2 }
            XYPoint { x: 9.4; y: -1 }

            Component.onCompleted: {
                if (visible) {
                    ExGlobals.Constants.proxy.setCalculatedSeriesRef(calculatedSeries)
                }
            }
        }
    }
}


