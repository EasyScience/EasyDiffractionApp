import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {

    /*
    EaElements.GroupBox {
        title: qsTr("Plot settings")

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.CheckBox {
                text: qsTr("Show legend")
                checked: ExGlobals.Variables.showLegend
                onCheckedChanged: ExGlobals.Variables.showLegend = checked
            }

            EaElements.CheckBox {
                text: qsTr("Show measured")
                checked: ExGlobals.Constants.proxy.showMeasuredSeries
                onCheckedChanged: ExGlobals.Constants.proxy.showMeasuredSeries = checked
            }

            EaElements.CheckBox {
                text: qsTr("Show difference")
                checked: ExGlobals.Constants.proxy.showDifferenceChart
                onCheckedChanged: ExGlobals.Constants.proxy.showDifferenceChart = checked
            }
        }
    }
    */

    EaElements.GroupBox {
        title: qsTr("Parameters")

        EaElements.CheckBox {
            topPadding: 0
            text: qsTr("Iconified names")
            checked: ExGlobals.Variables.iconifiedNames
            onCheckedChanged: ExGlobals.Variables.iconifiedNames = checked
        }
    }

    EaElements.GroupBox {
        title: qsTr("Calculation")

        Row {
            spacing: minimizerRow.spacing

            // Minimizer
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: minimizerLabel.width
                text: qsTr("Engine:")
            }
            EaElements.ComboBox {
                width: minimizerSelector.width

                model: ExGlobals.Constants.proxy.calculatorNames
                currentIndex: ExGlobals.Constants.proxy.currentCalculatorIndex
                onCurrentIndexChanged: ExGlobals.Constants.proxy.currentCalculatorIndex = currentIndex

                Component.onCompleted: ExGlobals.Variables.calculatorSelector = this
            }
        }

        Component.onCompleted: ExGlobals.Variables.calculatorsGroup = this
    }

    EaElements.GroupBox {
        title: qsTr("Minimization")
        enabled: ExGlobals.Constants.proxy.experimentLoaded

        Row {
            id: minimizerRow

            spacing: EaStyle.Sizes.fontPixelSize

            // Minimizer
            EaComponents.TableViewLabel{
                id: minimizerLabel

                horizontalAlignment: Text.AlignRight
                width: EaStyle.Sizes.fontPixelSize * 4.5
                text: qsTr("Minimizer:")
            }
            EaElements.ComboBox {
                id: minimizerSelector

                width: (EaStyle.Sizes.sideBarContentWidth - minimizerLabel.width * 2 - minimizerRow.spacing * 3) / 2

                model: ExGlobals.Constants.proxy.minimizerNames
                currentIndex: ExGlobals.Constants.proxy.currentMinimizerIndex

                onCurrentIndexChanged: {
                    ExGlobals.Constants.proxy.currentMinimizerIndex = currentIndex
                }
            }

            // Method
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: minimizerLabel.width
                text: qsTr("Method:")
            }
            EaElements.ComboBox {
                id: methodSelector

                width: minimizerSelector.width
                model: ExGlobals.Constants.proxy.minimizerMethodNames
                currentIndex: ExGlobals.Constants.proxy.currentMinimizerMethodIndex
                onCurrentIndexChanged: {
                    ExGlobals.Constants.proxy.currentMinimizerMethodIndex = currentIndex
                }
            }
        }

    }

    EaElements.GroupBox {
        title: qsTr("Fitting constraints")
        enabled: ExGlobals.Constants.proxy.experimentLoaded
        last: true

        ExComponents.AnalysisConstraints {}

        Column {
            //spacing: -4

            Grid {
                columns: 6
                columnSpacing: EaStyle.Sizes.fontPixelSize * 0.5
                verticalItemAlignment: Grid.AlignVCenter

                EaElements.ComboBox {
                    id: dependentPar
                    width: 149
                    currentIndex: -1
                    displayText: currentIndex === -1 ? "Select parameter" : currentText
                    model: XmlListModel {
                        xml: ExGlobals.Constants.proxy.fitablesListAsXml
                        query: "/root/item"
                        XmlRole { name: "label"; query: "label/string()" }
                        onXmlChanged: dependentParCurrentIndex = dependentPar.currentIndex
                    }
                    onCurrentIndexChanged: {
                        if (dependentPar.currentIndex === -1 && model.count > 0)
                            dependentPar.currentIndex = dependentParCurrentIndex
                    }
                }

                EaElements.ComboBox {
                    id: relationalOperator
                    width: 47
                    currentIndex: 0
                    font.family: EaStyle.Fonts.iconsFamily
                    //model: ["=", ">", "<"]
                    model: XmlListModel {
                        xml: "<root><item><operator>=</operator><icon>\uf52c</icon></item><item><operator>&gt;</operator><icon>\uf531</icon></item><item><operator>&lt;</operator><icon>\uf536</icon></item></root>"
                        query: "/root/item"
                        XmlRole { name: "icon"; query: "icon/string()" }
                    }
                }

                EaElements.TextField {
                    id: value
                    width: 65
                    horizontalAlignment: Text.AlignRight
                    text: "1.0000"
                }

                EaElements.ComboBox {
                    id: arithmeticOperator
                    width: relationalOperator.width
                    currentIndex: 0
                    font.family: EaStyle.Fonts.iconsFamily
                    //model: ["", "*", "/", "+", "-"]
                    //model: ["\uf00d", "\uf529", "\uf067", "\uf068"]
                    model: XmlListModel {
                        xml: "<root><item><operator>*</operator><icon>\uf00d</icon></item><item><operator>/</operator><icon>\uf529</icon></item><item><operator>+</operator><icon>\uf067</icon></item><item><operator>-</operator><icon>\uf068</icon></item></root>"
                        query: "/root/item"
                        XmlRole { name: "icon"; query: "icon/string()" }
                    }
                }

                EaElements.ComboBox {
                    id: independentPar
                    width: dependentPar.width
                    currentIndex: -1
                    displayText: currentIndex === -1 ? "Select parameter" : currentText
                    model: XmlListModel {
                        xml: ExGlobals.Constants.proxy.fitablesListAsXml
                        query: "/root/item"
                        XmlRole { name: "label"; query: "label/string()" }
                        onXmlChanged: independentParCurrentIndex = independentPar.currentIndex
                    }
                    onCurrentIndexChanged: {
                        if (independentPar.currentIndex === -1 && model.count > 0)
                            independentPar.currentIndex = independentParCurrentIndex
                    }
                }

                EaElements.SideBarButton {
                    id: addConstraint
                    width: 35
                    fontIcon: "plus-circle"
                    ToolTip.text: qsTr("Add constraint between two parameters")
                    onClicked: {
                        ExGlobals.Constants.proxy.addConstraint(
                                   dependentPar.currentIndex,
                                   relationalOperator.currentText.replace("\uf52c", "=").replace("\uf531", ">").replace("\uf536", "<"),
                                   value.text,
                                   arithmeticOperator.currentText.replace("\uf00d", "*").replace("\uf529", "/").replace("\uf067", "+").replace("\uf068", "-"),
                                   independentPar.currentIndex
                                   )
                    }
                }
            }

            Grid {
                columns: 6
                columnSpacing: EaStyle.Sizes.fontPixelSize * 0.5
                anchors.horizontalCenter: parent.horizontalCenter
                verticalItemAlignment: Grid.AlignVCenter

                EaElements.ComboBox {
                    id: dependentPar2
                    width: 149
                    currentIndex: -1
                    displayText: currentIndex === -1 ? "Select parameter" : currentText
                    model: XmlListModel {
                        xml: ExGlobals.Constants.proxy.fitablesListAsXml
                        query: "/root/item"
                        XmlRole { name: "label"; query: "label/string()" }
                        onXmlChanged: dependentParCurrentIndex2 = dependentPar2.currentIndex
                    }
                    onCurrentIndexChanged: {
                        if (dependentPar2.currentIndex === -1 && model.count > 0)
                            dependentPar2.currentIndex = dependentParCurrentIndex2
                    }
                }

                EaElements.ComboBox {
                    id: relationalOperator2
                    width: 47
                    currentIndex: 0
                    //model: ["=", ">", "<"]
                    font.family: EaStyle.Fonts.iconsFamily
                    model: XmlListModel {
                        xml: "<root><item><operator>=</operator><icon>\uf52c</icon></item><item><operator>&gt;</operator><icon>\uf531</icon></item><item><operator>&lt;</operator><icon>\uf536</icon></item></root>"
                        query: "/root/item"
                        XmlRole { name: "icon"; query: "icon/string()" }
                    }
                }

                EaElements.TextField {
                    id: value2
                    width: 65
                    horizontalAlignment: Text.AlignRight
                    text: "1.0000"
                }

                EaElements.SideBarButton {
                    id: addConstraint2
                    width: 35
                    fontIcon: "plus-circle"
                    ToolTip.text: qsTr("Add numeric constraint for single parameter")
                    onClicked: {
                        ExGlobals.Constants.proxy.addConstraint(
                                   dependentPar2.currentIndex,
                                   relationalOperator2.currentText.replace("\uf52c", "=").replace("\uf531", ">").replace("\uf536", "<"),
                                   value2.text,
                                   "",
                                   -1
                                   )
                    }
                }

                Item { height: 1; width: 47 }
                Item { height: 1; width: 149 }
            }


        }


    }

}
