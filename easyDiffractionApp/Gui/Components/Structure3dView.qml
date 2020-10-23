import QtQuick 2.13
import QtQuick.Controls 2.13
import QtDataVisualization 1.3

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    property real xAxisLength: 1.0
    property real yAxisLength: 1.0
    property real zAxisLength: 1.0
    property real xRotationInitial: -50.0
    property real yRotationInitial:  3.0
    property real zoomLevelInitial: 150.0
    property real xTargetInitial: 0.0
    property real yTargetInitial: 0.0
    property real zTargetInitial: 0.0
    property int animationDuration: 1000
    property var currentPhaseAllSites: ExGlobals.Constants.proxy.currentPhaseAllSites
    property var phaseList: ExGlobals.Constants.proxy.phaseList

    color: EaStyle.Colors.mainContentBackground

    Scatter3D {
        id: chart

        width: Math.min(parent.width, parent.height)
        height: Math.min(parent.width, parent.height)

        anchors.centerIn: parent

        // Camera view settings
        orthoProjection: false
        //scene.activeCamera.cameraPreset: Camera3D.CameraPresetIsometricLeftHigh
        scene.activeCamera.xRotation: xRotationInitial
        scene.activeCamera.yRotation: yRotationInitial
        scene.activeCamera.zoomLevel: zoomLevelInitial
        scene.activeCamera.target.x: xTargetInitial
        scene.activeCamera.target.y: yTargetInitial
        scene.activeCamera.target.z: zTargetInitial

        // Geometrical settings
        aspectRatio: Math.max(xAxisLength, zAxisLength) / yAxisLength
        horizontalAspectRatio: xAxisLength / zAxisLength

        // Interactivity
        selectionMode: AbstractGraph3D.SelectionNone // Left mouse button will be used for "reset view" coded below

        // Visualization settings
        theme: Theme3D {
            type: Theme3D.ThemeUserDefined
            ambientLightStrength: 0.5
            lightStrength: 5.0
            windowColor: EaStyle.Colors.chartBackground
            backgroundEnabled: false
            labelBackgroundEnabled: false
            labelBorderEnabled: false
            labelTextColor: EaStyle.Colors.chartLabels
            gridEnabled: false
            //font.pointSize: 60
            //font.family: Generic.Style.fontFamily
        }
        shadowQuality: AbstractGraph3D.ShadowQualityNone // AbstractGraph3D.ShadowQualitySoftHigh

        // Axes
        axisX: ValueAxis3D { labelFormat: "" }
        axisY: ValueAxis3D { labelFormat: "" }
        axisZ: ValueAxis3D { labelFormat: "" }

        //GenericAppElements.AtomScatter3DSeries {
        //    atomModel: Generic.Constants.proxy.cellBox
        //}

        // Unit cell chart settings
        Scatter3DSeries {
            mesh: Abstract3DSeries.MeshSphere
            itemSize: 0.03
            baseColor: EaStyle.Colors.chartForeground
            colorStyle: Theme3D.ColorStyleUniform

            ItemModelScatterDataProxy {
                itemModel: ListModel { id: cellBoxModel }
                xPosRole: "x"
                yPosRole: "y"
                zPosRole: "z"
            }
        }
    }

    ///////////
    // Helpers
    ///////////

    // Reset view with animation: Override default left mouse button
    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton //Qt.AllButtons
        //propagateComposedEvents: true
        //onPressed: mouse.accepted = false
        onReleased: animo.restart()
    }

    // Animation
    ParallelAnimation {
        id: animo
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.target.x"; to: xTargetInitial; duration: animationDuration }
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.target.y"; to: yTargetInitial; duration: animationDuration }
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.target.z"; to: zTargetInitial; duration: animationDuration }
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.xRotation"; to: xRotationInitial; duration: animationDuration }
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.yRotation"; to: yRotationInitial; duration: animationDuration }
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.zoomLevel"; to: zoomLevelInitial; duration: animationDuration }
    }

    // Update atoms
    //onCurrentPhaseAllSitesChanged: updateCell()
    onPhaseListChanged: updateCell()

    // Logic

    function createAtom() {
        const qmlString =
                'import QtQuick 2.13 \n' +
                'import QtDataVisualization 1.3 \n' +
                'Scatter3DSeries { \n' +
                    'property real atomSize: 0.5 \n' +
                    'property color atomColor: "coral" \n' +
                    'property alias atomModel: itemModel \n' +
                    'itemSize: atomSize \n' +
                    'baseColor: atomColor \n' +
                    'mesh: Abstract3DSeries.MeshSphere \n' +
                    'ItemModelScatterDataProxy { \n' +
                        'itemModel: ListModel { id: itemModel } \n' +
                        'xPosRole: "x" \n' +
                        'yPosRole: "y" \n' +
                        'zPosRole: "z" \n' +
                     '} \n' +
                '} \n'
        const atom = Qt.createQmlObject(qmlString, chart)
        return atom
    }

    function atomColors(idx) {
        const colors = ["coral", "steelblue", "olivedrab", "chocolate", "cadetblue", "darkseagreen", "cornflowerblue"]
        return colors[idx]
    }

    function updateCell() {
        // Get phase
        const phase = ExGlobals.Constants.proxy.phaseList[ExGlobals.Constants.proxy.currentPhaseIndex]
        if (typeof phase === 'undefined' || !Object.keys(phase).length) {
            return
        }

        ///print(JSON.stringify(ExGlobals.Constants.proxy.phaseList))

        // Unit cell parameters
        const a = phase.cell.length_a.value
        const b = phase.cell.length_b.value
        const c = phase.cell.length_c.value

        // Update axes lengths
        xAxisLength = a // in horizontal plane
        yAxisLength = b // vertical
        zAxisLength = c // in horizontal plane

        // Clear cell box model
        cellBoxModel.clear()

        // Draw cell box
        const n = 200
        for (let i = 0; i <= n; i++) {
            cellBoxModel.append({ x: i/n*a, y: 0.0*b, z: 0.0*c })
            cellBoxModel.append({ x: i/n*a, y: 1.0*b, z: 0.0*c })
            cellBoxModel.append({ x: i/n*a, y: 0.0*b, z: 1.0*c })
            cellBoxModel.append({ x: i/n*a, y: 1.0*b, z: 1.0*c })
            cellBoxModel.append({ x: 0.0*a, y: i/n*b, z: 0.0*c })
            cellBoxModel.append({ x: 1.0*a, y: i/n*b, z: 0.0*c })
            cellBoxModel.append({ x: 0.0*a, y: i/n*b, z: 1.0*c })
            cellBoxModel.append({ x: 1.0*a, y: i/n*b, z: 1.0*c })
            cellBoxModel.append({ x: 0.0*a, y: 0.0*b, z: i/n*c })
            cellBoxModel.append({ x: 1.0*a, y: 0.0*b, z: i/n*c })
            cellBoxModel.append({ x: 0.0*a, y: 1.0*b, z: i/n*c })
            cellBoxModel.append({ x: 1.0*a, y: 1.0*b, z: i/n*c })
        }

        // Remove atom scatters, but unit cell box (number 1)
        for (let i = 1, len = chart.seriesList.length; i < len; i++) {
            chart.removeSeries(chart.seriesList[1])
        }

        // Populate chart with atoms. Every atom is an individual scatter serie
        const sites = ExGlobals.Constants.proxy.currentPhaseAllSites //(ExGlobals.Constants.proxy.currentPhaseIndex)
        let atom_idx = 0
        for (let atom_label in sites) {
            for (let site_fracts_idx in sites[atom_label]) {
                let atom = createAtom()
                atom.atomColor = atomColors(atom_idx)
                atom.atomModel.append({
                    x: sites[atom_label][site_fracts_idx][0] * a,
                    y: sites[atom_label][site_fracts_idx][1] * b,
                    z: sites[atom_label][site_fracts_idx][2] * c
                })
                chart.addSeries(atom)
            }
            atom_idx++
        }
    }

}


