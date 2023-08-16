// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import QtQuick
import QtQuick.Controls
import QtQuick3D
import QtQuick3D.Helpers

import EasyApp.Gui.Animations as EaAnimations
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


Rectangle {
    id: container

    property real cellLengthA: typeof Globals.Proxies.main.model.dataBlocks[Globals.Proxies.main.model.currentIndex] !== 'undefined' ?
        Globals.Proxies.main.model.dataBlocks[Globals.Proxies.main.model.currentIndex].params['_cell_length_a']['value'] :
        10.0  // NEED FIX
    property real cellLengthB: typeof Globals.Proxies.main.model.dataBlocks[Globals.Proxies.main.model.currentIndex] !== 'undefined' ?
        Globals.Proxies.main.model.dataBlocks[Globals.Proxies.main.model.currentIndex].params['_cell_length_b']['value'] :
        10.0  // NEED FIX
    property real cellLengthC: typeof Globals.Proxies.main.model.dataBlocks[Globals.Proxies.main.model.currentIndex] !== 'undefined' ?
        Globals.Proxies.main.model.dataBlocks[Globals.Proxies.main.model.currentIndex].params['_cell_length_c']['value'] :
        10.0  // NEED FIX

    property real scaleCoeff: defaultScaleCoeff
    property real cellCylinderThickness: 1
    property real axesCylinderThickness: 6
    property real axisConeSize: 25
    property real atomSizeScale: 0.25

    property real defaultScaleCoeff: Math.min(width, height) /
                                     Math.max(cellLengthA, cellLengthB, cellLengthC) *
                                     0.4

    property var defaultEulerRotation: Qt.vector3d(12, -34, -8)
    property var alongAEulerRotation: Qt.vector3d(-90, 90, 180)
    property var alongBEulerRotation: Qt.vector3d(0, 90, 90)
    property var alongCEulerRotation: Qt.vector3d(0, 0, 0)

    color: EaStyle.Colors.chartBackground
    Behavior on color { EaAnimations.ThemeChange {} }

    // Root scene
    Node {
        id: standAloneRootScene

        // Light
        DirectionalLight {
            eulerRotation.x: -30
            eulerRotation.y: 30
        }
        // Light

        // Camera
        OrthographicCamera {
            id: cameraOrthographicFront
            z: Math.max(container.width, container.height)
            lookAtNode: structureViewScene
        }
        PerspectiveCamera {
            id: cameraPerspectiveFront
            z: Math.min(cameraOrthographicFront.z, 470)
            lookAtNode: structureViewScene
        }
        // Camera

        // Sub-scene
        Node {
            id: structureViewScene

            eulerRotation: defaultEulerRotation
            Behavior on eulerRotation { EaAnimations.ThemeChange {} }

            // Unit cell
            Repeater3D {
                id: cell
                model: [
                    // x
                    { "x": 0,   "y":-0.5, "z":-0.5, "rotx": 0, "roty": 0,  "rotz":-90, "len": cellLengthA },
                    { "x": 0,   "y": 0.5, "z":-0.5, "rotx": 0, "roty": 0,  "rotz":-90, "len": cellLengthA },
                    { "x": 0,   "y":-0.5, "z": 0.5, "rotx": 0, "roty": 0,  "rotz":-90, "len": cellLengthA },
                    { "x": 0,   "y": 0.5, "z": 0.5, "rotx": 0, "roty": 0,  "rotz":-90, "len": cellLengthA },
                    // y
                    { "x":-0.5, "y": 0,   "z":-0.5, "rotx": 0, "roty": 0,  "rotz": 0,  "len": cellLengthB },
                    { "x": 0.5, "y": 0,   "z":-0.5, "rotx": 0, "roty": 0,  "rotz": 0,  "len": cellLengthB },
                    { "x":-0.5, "y": 0,   "z": 0.5, "rotx": 0, "roty": 0,  "rotz": 0,  "len": cellLengthB },
                    { "x": 0.5, "y": 0,   "z": 0.5, "rotx": 0, "roty": 0,  "rotz": 0,  "len": cellLengthB },
                    // z
                    { "x":-0.5, "y":-0.5, "z": 0,   "rotx": 0, "roty": 90, "rotz": 90, "len": cellLengthC },
                    { "x": 0.5, "y":-0.5, "z": 0,   "rotx": 0, "roty": 90, "rotz": 90, "len": cellLengthC },
                    { "x":-0.5, "y": 0.5, "z": 0,   "rotx": 0, "roty": 90, "rotz": 90, "len": cellLengthC },
                    { "x": 0.5, "y": 0.5, "z": 0,   "rotx": 0, "roty": 90, "rotz": 90, "len": cellLengthC },
                ]
                Model {
                    source: "#Cylinder"
                    position: Qt.vector3d(cell.model[index].x * cellLengthA * scaleCoeff,
                                          cell.model[index].y * cellLengthB * scaleCoeff,
                                          cell.model[index].z * cellLengthC * scaleCoeff)
                    eulerRotation: Qt.vector3d(cell.model[index].rotx,
                                               cell.model[index].roty,
                                               cell.model[index].rotz)
                    scale: Qt.vector3d(cellCylinderThickness / 100,
                                       cell.model[index].len * scaleCoeff / 100,
                                       cellCylinderThickness / 100)
                    materials: [ DefaultMaterial { diffuseColor: EaStyle.Colors.grey } ]
                }
            }
            // Unit cell

            // Axes vectors
            Node {
                visible: Globals.Vars.showCoordinateVectorsOnModelPage

                // X-axis vector
                Node {
                    Model {
                        source: "#Cylinder"
                        position: Qt.vector3d( axisConeSize,
                                              -0.5 * cellLengthB * scaleCoeff,
                                              -0.5 * cellLengthC * scaleCoeff)
                        eulerRotation: Qt.vector3d(0, 0, -90)
                        scale: Qt.vector3d(axesCylinderThickness / 100,
                                           (scaleCoeff * cellLengthA + 2 * axisConeSize) / 100,
                                           axesCylinderThickness / 100)
                        materials: [ DefaultMaterial { diffuseColor: EaStyle.Colors.red } ]
                    }
                    Model {
                        source: "#Cone"
                        position: Qt.vector3d( 0.5 * cellLengthA * scaleCoeff + 2 * axisConeSize,
                                              -0.5 * cellLengthB * scaleCoeff,
                                              -0.5 * cellLengthC * scaleCoeff)
                        eulerRotation: Qt.vector3d(0, 0, -90)
                        scale: Qt.vector3d(axisConeSize / 100, axisConeSize / 100, axisConeSize / 100)
                        materials: [ DefaultMaterial { diffuseColor: EaStyle.Colors.red } ]
                    }
                }
                // X-axis vector

                // Y-axis vector
                Node {
                    Model {
                        source: "#Cylinder"
                        position: Qt.vector3d(-0.5 * cellLengthA * scaleCoeff,
                                               axisConeSize,
                                              -0.5 * cellLengthC * scaleCoeff)
                        eulerRotation: Qt.vector3d(0, 0, 0)
                        scale: Qt.vector3d(axesCylinderThickness / 100,
                                           (scaleCoeff * cellLengthB + 2 * axisConeSize) / 100,
                                           axesCylinderThickness / 100)
                        materials: [ DefaultMaterial { diffuseColor: EaStyle.Colors.green } ]
                    }
                    Model {
                        source: "#Cone"
                        position: Qt.vector3d(-0.5 * cellLengthA * scaleCoeff,
                                               0.5 * cellLengthB * scaleCoeff + 2 * axisConeSize,
                                              -0.5 * cellLengthC * scaleCoeff)
                        eulerRotation: Qt.vector3d(0, 0, 0)
                        scale: Qt.vector3d(axisConeSize / 100, axisConeSize / 100, axisConeSize / 100)
                        materials: [ DefaultMaterial { diffuseColor: EaStyle.Colors.green } ]
                    }
                }
                // Y-axis vector

                // Z-axis vector
                Node {
                    Model {
                        source: "#Cylinder"
                        position: Qt.vector3d(-0.5 * cellLengthA * scaleCoeff,
                                              -0.5 * cellLengthB * scaleCoeff,
                                               axisConeSize)
                        eulerRotation: Qt.vector3d(0, 90, 90)
                        scale: Qt.vector3d(axesCylinderThickness / 100,
                                           (scaleCoeff * cellLengthC + 2 * axisConeSize) / 100,
                                           axesCylinderThickness / 100)
                        materials: [ DefaultMaterial { diffuseColor: EaStyle.Colors.blue } ]
                    }
                    Model {
                        source: "#Cone"
                        position: Qt.vector3d(-0.5 * cellLengthA * scaleCoeff,
                                              -0.5 * cellLengthB * scaleCoeff,
                                               0.5 * cellLengthC * scaleCoeff + 2 * axisConeSize)
                        eulerRotation: Qt.vector3d(0, 90, 90)
                        scale: Qt.vector3d(axisConeSize / 100, axisConeSize / 100, axisConeSize / 100)
                        materials: [ DefaultMaterial { diffuseColor: EaStyle.Colors.blue } ]
                    }
                }
                // Z-axis vector

            }
            // Axes vectors

            // Atoms
            Repeater3D {
                id: atoms

                model: Globals.Proxies.main.model.structViewAtomsModel

                Model {
                    source: "#Sphere"
                    position: Qt.vector3d((atoms.model[index].x - 0.5) * cellLengthA * scaleCoeff,
                                          (atoms.model[index].y - 0.5) * cellLengthB * scaleCoeff,
                                          (atoms.model[index].z - 0.5) * cellLengthC * scaleCoeff)
                    scale: Qt.vector3d(atomSizeScale * atoms.model[index].diameter,
                                       atomSizeScale * atoms.model[index].diameter,
                                       atomSizeScale * atoms.model[index].diameter)
                    materials: [ DefaultMaterial { diffuseColor: atoms.model[index].color } ]
                }

                onModelChanged: saveImgTimer.restart()
            }
            // Atoms
        }
        // Sub-scene
    }
    // Root scene

    // Renderer
    View3D {
        id: view
        anchors.fill: parent
        importScene: standAloneRootScene
        camera: cameraOrthographicFront  //cameraPerspectiveFront
    }
    // Renderer

    // Rotation controller
    /*
    OrbitCameraController {
        id: cameraController
        anchors.fill: parent
        origin: structureViewScene
        camera: view.camera
    }
    */
    MouseArea {
        property real pressedX
        property real pressedY
        anchors.fill: parent
        onPressed: {
            pressedX = mouseX
            pressedY = mouseY
        }
        onMouseXChanged: Qt.callLater(update)
        onMouseYChanged: Qt.callLater(update)
        function update() {
            const dx = mouseX - pressedX
            const dy = mouseY - pressedY
            pressedX = mouseX
            pressedY = mouseY

            structureViewScene.rotate(dx, Qt.vector3d(0, 1, 0), Node.SceneSpace)
            structureViewScene.rotate(dy, Qt.vector3d(1, 0, 0), Node.SceneSpace)
        }
    }
    // Rotation controller

    // Tool buttons
    Row {
        anchors.top: parent.top
        anchors.right: parent.right

        anchors.topMargin: EaStyle.Sizes.fontPixelSize
        anchors.rightMargin: EaStyle.Sizes.fontPixelSize

        spacing: 0.25 * EaStyle.Sizes.fontPixelSize

        /*
        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "cube"
            ToolTip.text: view.camera === cameraPerspectiveFront ?
                              qsTr("Set orthographic view") :
                              qsTr("Set perspective view")
            onClicked: view.camera === cameraPerspectiveFront ?
                           view.camera = cameraOrthographicFront :
                           view.camera = cameraPerspectiveFront
        }

        Item { height: 1; width: 0.5 * EaStyle.Sizes.fontPixelSize }  // spacer
        */

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "search-plus"
            ToolTip.text: qsTr("Zoom in")
            onClicked: scaleCoeff += 1
        }

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "search-minus"
            ToolTip.text: qsTr("Zoom out")
            onClicked: cameraOrthographicFront.z -= 10 //scaleCoeff -= 1
        }

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "backspace"
            ToolTip.text: qsTr("Reset to default scale")
            onClicked: scaleCoeff = defaultScaleCoeff
        }

        Item { height: 1; width: 0.5 * EaStyle.Sizes.fontPixelSize }  // spacer

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "a"
            ToolTip.text: qsTr("View along the a axis")
            onClicked: structureViewScene.eulerRotation = alongAEulerRotation
        }

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "b"
            ToolTip.text: qsTr("View along the b axis")
            onClicked: structureViewScene.eulerRotation = alongBEulerRotation
        }

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "c"
            ToolTip.text: qsTr("View along the c axis")
            onClicked: structureViewScene.eulerRotation = alongCEulerRotation
        }

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "backspace"
            ToolTip.text: qsTr("Reset to default rotation")
            onClicked: structureViewScene.eulerRotation = defaultEulerRotation
        }
    }
    // Tool buttons

    // Legend
    Rectangle {
        visible: Globals.Vars.showCoordinateVectorsOnModelPage

        width: childrenRect.width
        height: childrenRect.height

        anchors.bottom: container.bottom
        anchors.left: container.left
        anchors.margins: EaStyle.Sizes.fontPixelSize

        color: EaStyle.Colors.mainContentBackgroundHalfTransparent
        Behavior on color { EaAnimations.ThemeChange {} }

        border {
            color: EaStyle.Colors.chartGridLine
            Behavior on color { EaAnimations.ThemeChange {} }
        }

        Column {
            leftPadding: EaStyle.Sizes.fontPixelSize
            rightPadding: EaStyle.Sizes.fontPixelSize
            topPadding: EaStyle.Sizes.fontPixelSize * 0.5
            bottomPadding: EaStyle.Sizes.fontPixelSize * 0.5

            EaElements.Label {
                text: 'a axis'
                color: EaStyle.Colors.red
            }
            EaElements.Label {
                text: 'b axis'
                color: EaStyle.Colors.green
            }
            EaElements.Label {
                text: 'c axis'
                color: EaStyle.Colors.blue
            }
            /*
            EaElements.Label { text: `eulerRotation ${view.camera.eulerRotation}` }
            EaElements.Label { text: `pivot ${view.camera.pivot}` }
            EaElements.Label { text: `position ${view.camera.position}` }
            EaElements.Label { text: `rotation ${view.camera.rotation}` }
            EaElements.Label { text: `scale ${view.camera.scale}` }
            EaElements.Label { text: `scenePosition ${view.camera.scenePosition}` }
            EaElements.Label { text: `sceneRotation ${view.camera.sceneRotation}` }
            EaElements.Label { text: `sceneScale ${view.camera.sceneScale}` }
            EaElements.Label { text: `forward ${view.camera.forward}` }
            EaElements.Label { text: `sceneTransform ${view.camera.sceneTransform}` }
            EaElements.Label { text: `x y z ${view.camera.x} ${view.camera.y} ${view.camera.z}` }
            */
        }
    }
    // Legend

    Component.onDestruction: console.debug(`Structure view container destroyed: ${container}`)
    Component.onCompleted: console.debug(`Structure view container created: ${container}`)

    // NEED FIX
    // For some reasons, when orthographic camera is selected for the first time,
    // scale is incorrect. When camera is changed to perspective one and then back
    // to orthographic, scale jumps to the expected one. The same occures when size
    // of the container is changed. So, this timer is temporary fix to get the
    // correct scale few moments after the structure view is created.
    Timer {
        id: increaseWidthTimer

        running: true
        interval: 1000
        onTriggered: {
            container.width += 1
            decreaseWidthTimer.start()
        }
    }

    Timer {
        id: decreaseWidthTimer

        interval: 1000
        onTriggered: {
            container.width -= 1
        }
    }

    // Auto-saving images
    Timer {
        id: saveImgTimer

        interval: 5000
        onTriggered: saveImg()
    }

    function saveImg() {
        if (Globals.Proxies.main.project.location) {
            const modelCurrenIndex = Globals.Proxies.main.model.currentIndex
            const cifFileName = Globals.Proxies.main.project.dataBlock.loops._model_cif_file[modelCurrenIndex]._name.value
            let split = cifFileName.split('.')
            split.pop()
            const baseFileName = split.join(".")
            const suffix = EaStyle.Colors.isDarkPalette ? '_dark' : '_light'
            const imgFileName = baseFileName + suffix + '.png'
            const path = Globals.Proxies.main.project.location + '/' +
                       Globals.Proxies.main.project.dirNames.models + '/' +
                       imgFileName
            container.grabToImage(function(result) {
                result.saveToFile(path)
            })
        }
    }

}
