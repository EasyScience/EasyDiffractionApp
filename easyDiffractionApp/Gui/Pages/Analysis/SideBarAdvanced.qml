import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {
    property int independentParCurrentIndex: 0
    property int dependentParCurrentIndex: 0
    property int dependentParCurrentIndex2: 0

    EaElements.GroupBox {
        title: qsTr("Calculator")
        collapsed: false

        EaElements.ComboBox {
            width: 200
            currentIndex: ExGlobals.Constants.proxy.calculatorIndex
            model: ExGlobals.Constants.proxy.calculatorList
            onActivated: ExGlobals.Constants.proxy.calculatorIndex = currentIndex
        }
    }

    EaElements.GroupBox {
        title: qsTr("Minimizer")
        collapsed: false

        EaElements.ComboBox {
            width: 200
            ///currentIndex: ExGlobals.Constants.proxy.minimizerIndex
            model: ExGlobals.Constants.proxy.minimizerList
            onActivated: ExGlobals.Constants.proxy.minimizerIndex = currentIndex
        }
    }

    EaElements.GroupBox {
        title: qsTr("Fitting constraints")
        visible: ExGlobals.Variables.analysisPageEnabled
        collapsed: false

        /*
        EaComponents.ConstraintsView {
            defaultInfoText: qsTr("No Constraints Added")
            xmlModel: ExGlobals.Constants.proxy.constraintsListAsXml
        }
        */

        ExComponents.ConstraintsView {}


        Column {
            spacing: -4

            Grid {
                columns: 6
                columnSpacing: 10
                verticalItemAlignment: Grid.AlignVCenter

                EaElements.ComboBox {
                    id: dependentPar
                    width: 140
                    currentIndex: -1
                    displayText: currentIndex === -1 ? "Select parameter" : currentText
                    model: XmlListModel {
                        ///xml: ExGlobals.Constants.proxy.fitablesListAsXml
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
                    //model: ["=", ">", "<"]
                    font.family: EaStyle.Fonts.iconsFamily
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
                    //model: ["", "*", "/", "+", "-"]
                    font.family: EaStyle.Fonts.iconsFamily
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
                        ///xml: ExGlobals.Constants.proxy.fitablesListAsXml
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
                columns: 4
                columnSpacing: 10
                anchors.horizontalCenter: parent.horizontalCenter
                verticalItemAlignment: Grid.AlignVCenter

                EaElements.ComboBox {
                    id: dependentPar2
                    width: 140
                    currentIndex: -1
                    displayText: currentIndex === -1 ? "Select parameter" : currentText
                    model: XmlListModel {
                        ///xml: ExGlobals.Constants.proxy.fitablesListAsXml
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
            }


        }


    }

}
