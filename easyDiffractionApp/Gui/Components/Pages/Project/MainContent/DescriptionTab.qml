// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


Rectangle {
    id: main

    readonly property int fullWidth: width
    readonly property int nameColumnWidth: 10 * EaStyle.Sizes.fontPixelSize
    readonly property int imageHeight: 7.0 * EaStyle.Sizes.fontPixelSize
    readonly property int innerSpacing: 0.85 * EaStyle.Sizes.fontPixelSize
    readonly property int outterSpacing: 1.5 * EaStyle.Sizes.fontPixelSize

    color: 'transparent'

    // Flickable
    Flickable {
        id: flickable

        anchors.fill: parent

        contentHeight: column.height + 2 * column.y
        contentWidth: column.width

        clip: true
        flickableDirection: Flickable.VerticalFlick

        ScrollBar.vertical: EaElements.ScrollBar {
            policy: ScrollBar.AsNeeded
            interactive: false
        }

        // Main column
        Column {
            id: column

            x: 1.5 * outterSpacing
            y: outterSpacing
            width: main.width - 2 * x

            spacing: innerSpacing

            // Title
            EaElements.TextInput {
                font.family: EaStyle.Fonts.secondFontFamily
                font.pixelSize: EaStyle.Sizes.fontPixelSize * 3
                font.weight: Font.ExtraLight
                onAccepted: focus = false
                validator: RegularExpressionValidator { regularExpression: /^[a-zA-Z][a-zA-Z0-9_\-\.]{1,30}$/ }
                placeholderText: qsTr("Enter project name here")
                text: Globals.Proxies.main.project.dataBlock.name.value
                onEditingFinished: Globals.Proxies.main.project.setName(text)
                onFocusChanged: {
                    if (!focus && !text) {
                        text = Globals.Proxies.main.project.dataBlock.name.value
                    }
                }

            }
            // Title

            // Extra spacer
            Item { height: 1; width: 1 }
            // Extra spacer

            // Description
            Row {
                property var parameter: Globals.Proxies.projectMainParam('_description')
                spacing: innerSpacing
                EaElements.Label {
                    width: nameColumnWidth
                    font.bold: true
                    text: parent.parameter.prettyName
                }
                EaElements.TextInput {
                    text: parent.parameter.value
                    placeholderText: qsTr("Enter project description here")
                    onAccepted: focus = false
                    onEditingFinished: {
                        if (text) {
                            Globals.Proxies.setProjectMainParam(parent.parameter, 'value', text)
                        } else {
                            text = parent.parameter.value
                        }
                    }
                }
            }
            // Description

            // Extra spacer
            Item {  visible: !Globals.Proxies.main.project.location.startsWith(':/'); height: 1; width: 1 }
            // Extra spacer

            // Date
            Column {
                visible: !Globals.Proxies.main.project.location.startsWith(':/')
                /*
                Row {
                    spacing: innerSpacing
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: qsTr('Created')
                    }
                    EaElements.Label {
                        text: Globals.Proxies.main.project.dateCreated
                    }
                }
                */
                Row {
                    spacing: innerSpacing
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: qsTr('Last modified')
                    }
                    EaElements.Label {
                        text: Globals.Proxies.main.project.dateLastModified
                    }
                }
            }
            // Date

            // Extra spacer
            Item {  visible: !Globals.Proxies.main.project.location.startsWith(':/'); height: 1; width: 1 }
            // Extra spacer

            // Location and dirs
            Column {
                visible: !Globals.Proxies.main.project.location.startsWith(':/')
                Row {
                    spacing: innerSpacing
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: qsTr('Location')
                    }
                    EaElements.Label {
                        width: column.width - nameColumnWidth
                        elide: Text.ElideMiddle
                        text: Globals.Proxies.main.project.location.startsWith(':/') ?
                                  Globals.Proxies.main.project.location.substring(2) :
                                  Globals.Proxies.main.project.location
                    }
                }
                Row {
                    spacing: innerSpacing
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: qsTr('Model directory')
                    }
                    EaElements.Label {
                        width: column.width - nameColumnWidth
                        elide: Text.ElideMiddle
                        text: Globals.Proxies.main.project.dirNames.models
                    }
                }
                Row {
                    spacing: innerSpacing
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: qsTr('Experiment directory')
                    }
                    EaElements.Label {
                        width: column.width - nameColumnWidth
                        elide: Text.ElideMiddle
                        text: Globals.Proxies.main.project.dirNames.experiments
                    }
                }
                Row {
                    spacing: innerSpacing
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: qsTr('Analysis directory')
                    }
                    EaElements.Label {
                        width: column.width - nameColumnWidth
                        elide: Text.ElideMiddle
                        text: Globals.Proxies.main.project.dirNames.analysis
                    }
                }
                Row {
                    spacing: innerSpacing
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: qsTr('Summary directory')
                    }
                    EaElements.Label {
                        width: column.width - nameColumnWidth
                        elide: Text.ElideMiddle
                        text: Globals.Proxies.main.project.dirNames.summary
                    }
                }
            }
            // Location and dirs

            // Extra spacer
            Item { height: 1; width: 1 }
            // Extra spacer

            // Models
            Row {
                //visible: !Globals.Proxies.main.project.location.startsWith(':/')
                spacing: innerSpacing
                EaElements.Label {
                    width: nameColumnWidth
                    font.bold: true
                    text: typeof Globals.Proxies.main.project.dataBlock.loops._model_cif_file === 'undefined' ?
                              '' :
                              Globals.Proxies.main.project.dataBlock.loops._model_cif_file[0]._name.prettyName
                }
                EaElements.Label {
                    text: typeof Globals.Proxies.main.project.dataBlock.loops._model_cif_file === 'undefined' ?
                              '' :
                              Globals.Proxies.main.project.dataBlock.loops._model_cif_file.map(item => item._name.value).join(',  ')

                }
            }
            // Models

            // Model images
            Row {
                spacing: innerSpacing
                visible: childrenRect.height > 2
                Item { height: 1; width: nameColumnWidth }
                Repeater {
                    id: modelImageRepeater
                    model: Globals.Proxies.main.project.dataBlock.loops._model_cif_file
                    Rectangle {
                        visible: childrenRect.height
                        height: childrenRect.height + 2 * border.width
                        width: childrenRect.width + 2 * border.width
                        color: EaStyle.Colors.chartBackground
                        border.color: EaStyle.Colors.chartAxis
                        border.width: 1
                        Image {
                            x: parent.border.width
                            y: parent.border.width
                            height: status === Image.Ready ? imageHeight : 0
                            fillMode: Image.PreserveAspectFit
                            asynchronous: true
                            mipmap: true
                            source: {
                                const cifFileName = modelImageRepeater.model[index]._name.value
                                let split = cifFileName.split('.')
                                split.pop()
                                const baseFileName = split.join(".")
                                const suffix = EaStyle.Colors.isDarkPalette ? '_dark' : '_light'
                                const imgFileName = baseFileName + suffix + '.png'
                                const fpathParts = [Globals.Proxies.main.project.location,
                                                    Globals.Proxies.main.project.dirNames.models,
                                                    imgFileName]
                                const uri = Globals.Proxies.main.backendHelpers.listToUri(fpathParts)
                                return uri
                            }
                        }
                    }
                }
            }
            // Model images

            // Experiments
            Row {
                //visible: !Globals.Proxies.main.project.location.startsWith(':/')
                spacing: innerSpacing
                EaElements.Label {
                    width: nameColumnWidth
                    font.bold: true
                    text: typeof Globals.Proxies.main.project.dataBlock.loops._experiment_cif_file === 'undefined' ?
                              '' :
                              Globals.Proxies.main.project.dataBlock.loops._experiment_cif_file[0]._name.prettyName
                }
                EaElements.Label {
                    text: typeof Globals.Proxies.main.project.dataBlock.loops._experiment_cif_file === 'undefined' ?
                              '' :
                              Globals.Proxies.main.project.dataBlock.loops._experiment_cif_file.map(item => item._name.value).join(',  ')

                }
            }
            // Experiments

            // Experiment images
            Row {
                spacing: innerSpacing
                visible: childrenRect.height > 2
                Item { height: 1; width: nameColumnWidth }
                Repeater {
                    id: experimentImageRepeater
                    model: Globals.Proxies.main.project.dataBlock.loops._experiment_cif_file
                    Rectangle {
                        visible: childrenRect.height
                        height: childrenRect.height + 2 * border.width
                        width: childrenRect.width + 2 * border.width
                        border.color: EaStyle.Colors.chartAxis
                        border.width: 1
                        Image {
                            x: parent.border.width
                            y: parent.border.width
                            height: status === Image.Ready ? imageHeight : 0
                            asynchronous: true
                            mipmap: true
                            fillMode: Image.PreserveAspectFit
                            source: {
                                const cifFileName = experimentImageRepeater.model[index]._name.value
                                let split = cifFileName.split('.')
                                split.pop()
                                const baseFileName = split.join(".")
                                const suffix = EaStyle.Colors.isDarkPalette ? '_dark' : '_light'
                                const imgFileName = baseFileName + suffix + '.png'
                                const fpathParts = [Globals.Proxies.main.project.location,
                                                    Globals.Proxies.main.project.dirNames.experiments,
                                                    imgFileName]
                                const uri = Globals.Proxies.main.backendHelpers.listToUri(fpathParts)
                                return uri
                            }
                        }
                    }
                }
            }
            // Experiment images
        }
        // Main column
    }
    // Flickable
}
