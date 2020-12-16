import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Dialogs 1.2
import QtQuick.Window 2.12
import QtQuick.Controls.Material 2.12
import QtCharts 2.3
import QtVTK 1.0

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements

//Rectangle {
//    property real xAxisLength: 1.0
//    property real yAxisLength: 1.0
//    property real zAxisLength: 1.0
//    property real xRotationInitial: -50.0
//    property real yRotationInitial:  3.0
//    property real zoomLevelInitial: 150.0
//    property real xTargetInitial: 0.0
//    property real yTargetInitial: 0.0
//    property real zTargetInitial: 0.0
//    property int animationDuration: 1000
//    property var currentPhaseAllSites: ExGlobals.Constants.proxy.currentPhaseAllSites
//    property var phasesAsObj: ExGlobals.Constants.proxy.phasesAsObj
//
//    color: EaStyle.Colors.mainContentBackground
//
//    Scatter3D {
//        id: chart
//
//        width: Math.min(parent.width, parent.height)
//        height: Math.min(parent.width, parent.height)
//
//        anchors.centerIn: parent
//
//        // Camera view settings
//        orthoProjection: false
//        //scene.activeCamera.cameraPreset: Camera3D.CameraPresetIsometricLeftHigh
//        scene.activeCamera.xRotation: xRotationInitial
//        scene.activeCamera.yRotation: yRotationInitial
//        scene.activeCamera.zoomLevel: zoomLevelInitial
//        scene.activeCamera.target.x: xTargetInitial
//        scene.activeCamera.target.y: yTargetInitial
//        scene.activeCamera.target.z: zTargetInitial
//
//        // Geometrical settings
//        aspectRatio: Math.max(xAxisLength, zAxisLength) / yAxisLength
//        horizontalAspectRatio: xAxisLength / zAxisLength
//
//        // Interactivity
//        selectionMode: AbstractGraph3D.SelectionNone // Left mouse button will be used for "reset view" coded below
//
//        // Visualization settings
//        theme: Theme3D {
//            type: Theme3D.ThemeUserDefined
//            ambientLightStrength: 0.5
//            lightStrength: 5.0
//            windowColor: EaStyle.Colors.chartBackground
//            backgroundEnabled: false
//            labelBackgroundEnabled: false
//            labelBorderEnabled: false
//            labelTextColor: EaStyle.Colors.chartLabels
//            gridEnabled: false
//            //font.pointSize: 60
//            //font.family: Generic.Style.fontFamily
//        }
//        shadowQuality: AbstractGraph3D.ShadowQualityNone // AbstractGraph3D.ShadowQualitySoftHigh
//
//        // Axes
//        axisX: ValueAxis3D { labelFormat: "" }
//        axisY: ValueAxis3D { labelFormat: "" }
//        axisZ: ValueAxis3D { labelFormat: "" }
//
//        //GenericAppElements.AtomScatter3DSeries {
//        //    atomModel: Generic.Constants.proxy.cellBox
//        //}
//
//        // Unit cell chart settings
//        Scatter3DSeries {
//            mesh: Abstract3DSeries.MeshSphere
//            itemSize: 0.03
//            baseColor: EaStyle.Colors.chartForeground
//            colorStyle: Theme3D.ColorStyleUniform
//
//            ItemModelScatterDataProxy {
//                itemModel: ListModel { id: cellBoxModel }
//                xPosRole: "x"
//                yPosRole: "y"
//                zPosRole: "z"
//            }
//        }
//    }
//
//    ///////////
//    // Helpers
//    ///////////
//
//    // Reset view with animation: Override default left mouse button
//    MouseArea {
//        anchors.fill: parent
//        acceptedButtons: Qt.LeftButton //Qt.AllButtons
//        //propagateComposedEvents: true
//        //onPressed: mouse.accepted = false
//        onReleased: animo.restart()
//    }
//
//    // Animation
//    ParallelAnimation {
//        id: animo
//        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.target.x"; to: xTargetInitial; duration: animationDuration }
//        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.target.y"; to: yTargetInitial; duration: animationDuration }
//        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.target.z"; to: zTargetInitial; duration: animationDuration }
//        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.xRotation"; to: xRotationInitial; duration: animationDuration }
//        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.yRotation"; to: yRotationInitial; duration: animationDuration }
//        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.zoomLevel"; to: zoomLevelInitial; duration: animationDuration }
//    }
//
//    // Update atoms
//    //onCurrentPhaseAllSitesChanged: updateCell()
//    onphasesAsObjChanged: updateCell()
//
//    // Logic
//
//    function createAtom() {
//        const qmlString =
//                'import QtQuick 2.13 \n' +
//                'import QtDataVisualization 1.3 \n' +
//                'Scatter3DSeries { \n' +
//                    'property real atomSize: 0.5 \n' +
//                    'property color atomColor: "coral" \n' +
//                    'property alias atomModel: itemModel \n' +
//                    'itemSize: atomSize \n' +
//                    'baseColor: atomColor \n' +
//                    'mesh: Abstract3DSeries.MeshSphere \n' +
//                    'ItemModelScatterDataProxy { \n' +
//                        'itemModel: ListModel { id: itemModel } \n' +
//                        'xPosRole: "x" \n' +
//                        'yPosRole: "y" \n' +
//                        'zPosRole: "z" \n' +
//                     '} \n' +
//                '} \n'
//        const atom = Qt.createQmlObject(qmlString, chart)
//        return atom
//    }
//
//    function atomColors(idx) {
//        const colors = ["coral", "steelblue", "olivedrab", "chocolate", "cadetblue", "darkseagreen", "cornflowerblue"]
//        return colors[idx]
//    }
//
//    function updateCell() {
//        // Get phase
//        const phase = ExGlobals.Constants.proxy.phasesAsObj[ExGlobals.Constants.proxy.currentPhaseIndex]
//        if (typeof phase === 'undefined' || !Object.keys(phase).length) {
//            return
//        }
//
//        ///print(JSON.stringify(ExGlobals.Constants.proxy.phasesAsObj))
//
//        // Unit cell parameters
//        const a = phase.cell.length_a.value
//        const b = phase.cell.length_b.value
//        const c = phase.cell.length_c.value
//
//        // Update axes lengths
//        xAxisLength = a // in horizontal plane
//        yAxisLength = b // vertical
//        zAxisLength = c // in horizontal plane
//
//        // Clear cell box model
//        cellBoxModel.clear()
//
//        // Draw cell box
//        const n = 200
//        for (let i = 0; i <= n; i++) {
//            cellBoxModel.append({ x: i/n*a, y: 0.0*b, z: 0.0*c })
//            cellBoxModel.append({ x: i/n*a, y: 1.0*b, z: 0.0*c })
//            cellBoxModel.append({ x: i/n*a, y: 0.0*b, z: 1.0*c })
//            cellBoxModel.append({ x: i/n*a, y: 1.0*b, z: 1.0*c })
//            cellBoxModel.append({ x: 0.0*a, y: i/n*b, z: 0.0*c })
//            cellBoxModel.append({ x: 1.0*a, y: i/n*b, z: 0.0*c })
//            cellBoxModel.append({ x: 0.0*a, y: i/n*b, z: 1.0*c })
//            cellBoxModel.append({ x: 1.0*a, y: i/n*b, z: 1.0*c })
//            cellBoxModel.append({ x: 0.0*a, y: 0.0*b, z: i/n*c })
//            cellBoxModel.append({ x: 1.0*a, y: 0.0*b, z: i/n*c })
//            cellBoxModel.append({ x: 0.0*a, y: 1.0*b, z: i/n*c })
//            cellBoxModel.append({ x: 1.0*a, y: 1.0*b, z: i/n*c })
//        }
//
//        // Remove atom scatters, but unit cell box (number 1)
//        for (let i = 1, len = chart.seriesList.length; i < len; i++) {
//            chart.removeSeries(chart.seriesList[1])
//        }
//
//        // Populate chart with atoms. Every atom is an individual scatter serie
//        const sites = ExGlobals.Constants.proxy.currentPhaseAllSites //(ExGlobals.Constants.proxy.currentPhaseIndex)
//        let atom_idx = 0
//        for (let atom_label in sites) {
//            for (let site_fracts_idx in sites[atom_label]) {
//                let atom = createAtom()
//                atom.atomColor = atomColors(atom_idx)
//                atom.atomModel.append({
//                    x: sites[atom_label][site_fracts_idx][0] * a,
//                    y: sites[atom_label][site_fracts_idx][1] * b,
//                    z: sites[atom_label][site_fracts_idx][2] * c
//                })
//                chart.addSeries(atom)
//            }
//            atom_idx++
//        }
//    }
    Rectangle {
        id: screenCanvasUI
//        anchors.fill: parent

        VtkFboItem {
            id: vtkFboItem
            objectName: "vtkFboItem"
            anchors.fill: parent
//            width: Math.min(parent.width, parent.height)
//            height: Math.min(parent.width, parent.height)
        }

        MouseArea {
            acceptedButtons: Qt.AllButtons
            anchors.fill: parent
            scrollGestureEnabled: false

            onPositionChanged: (mouse) => {
                print('Mouse moved')
                _vtkHandler.mouseMoveEvent(pressedButtons, mouseX, mouseY);
                mouse.accepted = false;
            }
            onPressed: (mouse) => {
                _vtkHandler.mousePressEvent(pressedButtons, mouseX, mouseY);
                mouse.accepted = false;
                // if u want to propagate the pressed event
                // so the VtkFboItem instance can receive it
                // then uncomment the belowed line
                // mouse.ignore() // or mouse.accepted = false
            }
            onReleased: (mouse) => {
                _vtkHandler.mouseReleaseEvent(pressedButtons, mouseX, mouseY);
                print(mouse);
                mouse.accepted = false;
            }
            onWheel: (wheel) => {
                wheel.accepted = false;
            }
        }

        EaElements.Label {
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: EaStyle.Sizes.fontPixelSize

            topPadding: 0.5*EaStyle.Sizes.fontPixelSize
            bottomPadding: 0.5*EaStyle.Sizes.fontPixelSize
            leftPadding: EaStyle.Sizes.fontPixelSize
            rightPadding: EaStyle.Sizes.fontPixelSize

            background: Rectangle {
                color: EaStyle.Colors.mainContentBackground
                opacity: 0.5
            }

            textFormat: Text.RichText

            text: `Axes colors: <font color=red>a</font>, <font color=#008000>b</font>, <font color=blue>c</font>`
        }


        /*
        Button {
            id: clearScene
            text: "Clear Scene"
            highlighted: true
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 50
            onClicked: _vtkHandler.clearScene()

            ToolTip.visible: hovered
            ToolTip.delay: 1000
            ToolTip.text: "Show 2D Chart in right corner"
        }

        Button {
            id: createScene
            text: "Create Lattice"
            highlighted: true
            anchors.right: clearScene.left
            anchors.bottom: parent.bottom
            anchors.margins: 50
            onClicked: _vtkHandler.create_plot_system()

            ToolTip.visible: hovered
            ToolTip.delay: 1000
            ToolTip.text: "Open a 3D model into the canvas"
        }
        */



    }


