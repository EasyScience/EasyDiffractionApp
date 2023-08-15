import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick3D
import QtQuick3D.Helpers

Rectangle {
    id: container

    property real cellLengthA: 10
    property real cellLengthB: 6
    property real cellLengthC: 4
    property real extraLength: 10//Math.max(cellLengthA, cellLengthB, cellLengthC) * 0.2

    property real scaleCoeff: 25//Math.min(width, height) /
                              //Math.max(cellLengthA, cellLengthB, cellLengthC) *
                              //0.5
    property real cellCylinderThickness: 1
    property real axesCylinderThickness: 5
    property real axisConeSize: 20

    property var defaultEulerRotation: Qt.vector3d(12, -34, -8)
    property var alongAEulerRotation: Qt.vector3d(-90, 90, -180)
    property var alongBEulerRotation: Qt.vector3d(0, 90, 90)
    property var alongCEulerRotation: Qt.vector3d(0, 0, 0)

    width: 500
    height: 500
    color: "#bbb"

//    onWidthChanged: console.error(`+++++++++++++ w: ${width}`)
//    onHeightChanged: console.error(`============= h: ${height}`)



    // Root scene
    Node {
        id: standAloneScene

        // Light
        DirectionalLight {
            eulerRotation.x: -30
            eulerRotation.y: 30
        }
        // Light

        // Camera
        OrthographicCamera {
            id: cameraOrthographicFront
            z: 500//Math.max(container.width, container.height)
            lookAtNode: node
        }
        //PerspectiveCamera {
        //    id: cameraPerspectiveFront
        //    z: Math.min(cameraOrthographicFront.z, 470)
        //    lookAtNode: node
        //}
        // Camera

        // Sub-scene
        Node {
            id: node

            eulerRotation: defaultEulerRotation

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
                    materials: [ DefaultMaterial { diffuseColor: "grey" } ]
                }
            }
            // Unit cell


            // Axes vectors
            Node {

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
                        materials: [ DefaultMaterial { diffuseColor: 'red' } ]
                    }
                    Model {
                        source: "#Cone"
                        position: Qt.vector3d( 0.5 * cellLengthA * scaleCoeff + 2 * axisConeSize,
                                              -0.5 * cellLengthB * scaleCoeff,
                                              -0.5 * cellLengthC * scaleCoeff)
                        eulerRotation: Qt.vector3d(0, 0, -90)
                        scale: Qt.vector3d(axisConeSize / 100, axisConeSize / 100, axisConeSize / 100)
                        materials: [ DefaultMaterial { diffuseColor: 'red' } ]
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
                        materials: [ DefaultMaterial { diffuseColor: 'green' } ]
                    }
                    Model {
                        source: "#Cone"
                        position: Qt.vector3d(-0.5 * cellLengthA * scaleCoeff,
                                               0.5 * cellLengthB * scaleCoeff + 2 * axisConeSize,
                                              -0.5 * cellLengthC * scaleCoeff)
                        eulerRotation: Qt.vector3d(0, 0, 0)
                        scale: Qt.vector3d(axisConeSize / 100, axisConeSize / 100, axisConeSize / 100)
                        materials: [ DefaultMaterial { diffuseColor: 'green' } ]
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
                        materials: [ DefaultMaterial { diffuseColor: 'blue' } ]
                    }
                    Model {
                        source: "#Cone"
                        position: Qt.vector3d(-0.5 * cellLengthA * scaleCoeff,
                                              -0.5 * cellLengthB * scaleCoeff,
                                               0.5 * cellLengthC * scaleCoeff + 2 * axisConeSize)
                        eulerRotation: Qt.vector3d(0, 90, 90)
                        scale: Qt.vector3d(axisConeSize / 100, axisConeSize / 100, axisConeSize / 100)
                        materials: [ DefaultMaterial { diffuseColor: 'blue' } ]
                    }
                }
                // Z-axis vector

            }
            // Axes vectors

            // Atoms
            Repeater3D {
                id: atoms
                model: [
                    { x: 0,   y: 0,   z: 0,   diameter: 0.2, color: 'coral'},
                    { x: 0,   y: 1,   z: 0,   diameter: 0.2, color: 'coral'},
                    { x: 1,   y: 0,   z: 0,   diameter: 0.2, color: 'coral'},
                    { x: 1,   y: 1,   z: 0,   diameter: 0.2, color: 'coral'},
                    { x: 0,   y: 0,   z: 1,   diameter: 0.2, color: 'coral'},
                    { x: 0,   y: 1,   z: 1,   diameter: 0.2, color: 'coral'},
                    { x: 1,   y: 0,   z: 1,   diameter: 0.2, color: 'coral'},
                    { x: 1,   y: 1,   z: 1,   diameter: 0.2, color: 'coral'},
                    { x: 0.5, y: 0.5, z: 0.5, diameter: 0.1, color: 'steelblue'}
                ]
                Model {
                    source: "#Sphere"
                    position: Qt.vector3d((atoms.model[index].x - 0.5) * cellLengthA * scaleCoeff,
                                          (atoms.model[index].y - 0.5) * cellLengthB * scaleCoeff,
                                          (atoms.model[index].z - 0.5) * cellLengthC * scaleCoeff)
                    scale: Qt.vector3d(atoms.model[index].diameter,
                                       atoms.model[index].diameter,
                                       atoms.model[index].diameter)
                    materials: [ DefaultMaterial { diffuseColor: atoms.model[index].color } ]
                }
            }
            // Atoms
        }
        // Sub-scene
    }
    // Root scene

    //
    View3D {
        id: view
        anchors.fill: parent
        importScene: standAloneScene
        camera: cameraOrthographicFront
    }
    //

    // Rotation controller
    /*
    OrbitCameraController {
        id: cameraController
        anchors.fill: parent
        origin: node
        camera: view.camera
    }
    */
    MouseArea {
        anchors.fill:parent
        property real pressedX
        property real pressedY
        onMouseXChanged: Qt.callLater(update)
        onMouseYChanged: Qt.callLater(update)
        onPressed: {
            [pressedX,pressedY] = [mouseX,mouseY];
        }
        function update() {
            let [dx,dy] = [mouseX - pressedX,mouseY - pressedY];
            [pressedX,pressedY] = [mouseX,mouseY];
            node.rotate(dx, Qt.vector3d(0, 1, 0), Node.SceneSpace);
            node.rotate(dy, Qt.vector3d(1, 0, 0), Node.SceneSpace);
        }
    }
    // Rotation controller

    // Tool buttons
    Row {
        anchors.top: parent.top
        anchors.right: parent.right

        Button {
            text: 'View'
            onClicked: view.camera === cameraPerspectiveFront ?
                           view.camera = cameraOrthographicFront :
                           view.camera = cameraPerspectiveFront
        }
        Button {
            text: 'x'
            onClicked: node.eulerRotation = alongAEulerRotation
        }
        Button {
            text: 'y'
            onClicked: node.eulerRotation = alongBEulerRotation
        }
        Button {
            text: 'z'
            onClicked: node.eulerRotation = alongCEulerRotation
        }
        Button {
            text: 'Reset'
            onClicked: node.eulerRotation = defaultEulerRotation
        }
    }
    // Tool buttons

    // Legend
    Rectangle {
        width: childrenRect.width
        height: childrenRect.height

        anchors.bottom: container.bottom
        anchors.left: container.left
        anchors.margins: 12

        color: '#aaa'

        Column {
            leftPadding: 12
            rightPadding: 12
            topPadding: 6
            bottomPadding: 6

            Label {
                text: 'x-axis'
                color: 'red'
            }
            Label {
                text: 'y-axis'
                color: 'green'
            }
            Label {
                text: 'z-axis'
                color: 'blue'
            }
            //
            Label { text: `eulerRotation ${node.eulerRotation}` }
            //Label { text: `pivot ${node.pivot}` }
            //Label { text: `position ${node.position}` }
            //Label { text: `rotation ${node.rotation}` }
            //Label { text: `scale ${node.scale}` }
            //Label { text: `scenePosition ${node.scenePosition}` }
            //Label { text: `sceneRotation ${node.sceneRotation}` }
            //Label { text: `sceneScale ${node.sceneScale}` }
            //
            //Label { text: `width ${container.width}` }
            //Label { text: `height ${container.height}` }
            //Label { text: `Math.min(width, height) ${Math.min(container.width, container.height)}` }
            //Label { text: `Math.max(cellLengthA, cellLengthB, cellLengthC) ${Math.max(cellLengthA, cellLengthB, cellLengthC)}` }
            //Label { text: `cameraOrthographicFront.z ${cameraOrthographicFront.z}` }
            //Label { text: `cameraPerspectiveFront.z ${cameraPerspectiveFront.z}` }
            //Label { text: `scaleCoeff ${scaleCoeff}` }
        }
    }
    // Legend

}
