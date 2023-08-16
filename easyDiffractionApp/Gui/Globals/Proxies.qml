// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
// SPDX-License-Identifier: BSD-3-Clause
// © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

pragma Singleton

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals
import Gui.Logic as Logic


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    property var main: typeof pyProxy !== 'undefined' && pyProxy !== null ?
                                         pyProxy:
                                         qmlProxy

    //readonly property var main_model_dataBlocks: main.model.dataBlocks
    //readonly property var main_experiment_dataBlocks: main.experiment.dataBlocks
    readonly property var main_fittables_data: main.fittables.data

    property int systemColorScheme: main.backendHelpers.systemColorScheme
    onSystemColorSchemeChanged: EaStyle.Colors.systemColorScheme = systemColorScheme

    readonly property var qmlProxy: QtObject {

        readonly property var backendHelpers: QtObject {
            property int systemColorScheme: -1
        }

        //////////
        // Logger
        //////////

        readonly property var logger: QtObject {
            property string level: 'debug'
        }

        //////////////
        // Connections
        //////////////

        readonly property var connections: QtObject {

            Component.onCompleted: {
                // Project

//                qmlProxy.project.nameChanged.connect(qmlProxy.project.setNeedSaveToTrue)
//                qmlProxy.project.descriptionChanged.connect(qmlProxy.project.setNeedSaveToTrue)
 //               qmlProxy.project.createdChanged.connect(qmlProxy.project.save)

                // Experiment

                qmlProxy.experiment.dataChanged.connect(qmlProxy.project.setNeedSaveToTrue)

                qmlProxy.experiment.dataChanged.connect(qmlProxy.fittables.set)


                qmlProxy.experiment.definedChanged.connect(function() {
                    print(`Experiment created: ${qmlProxy.experiment.defined}`)
                    qmlProxy.fittables.set()
                    qmlProxy.project.setNeedSaveToTrue()
                })

//                qmlProxy.experiment.parameterEdited.connect(function(needSetFittables) {
  //                  qmlProxy.experiment.parametersEdited(needSetFittables)
    //            })
/*
                qmlProxy.experiment.parametersEdited.connect(function(needSetFittables) {
                    print(`Experiment parameters changed. Need set fittables: ${needSetFittables}`)
                    qmlProxy.experiment.parametersChanged()
                    qmlProxy.experiment.loadData()
                    if (needSetFittables) {
                        qmlProxy.fittables.set()
                    }
                    qmlProxy.project.setNeedSaveToTrue()
                })

                qmlProxy.experiment.dataSizeChanged.connect(function() {
                    print(`Experiment data size: ${qmlProxy.experiment.dataSize}`)
                    qmlProxy.experiment.loadData()
                    if (qmlProxy.model.isCreated) {
                        qmlProxy.model.calculateData()
                    }
                })
*/
                // Model


//                qmlProxy.model.dataChanged.connect(qmlProxy.fittables.set)

                //qmlProxy.model.descriptionChanged.connect(qmlProxy.project.setNeedSaveToTrue)
/*
                qmlProxy.model.modelAdded.connect(function() {
                    print(`Model added. Models count: ${qmlProxy.model.models.length}`)
                    qmlProxy.model.calculateData()
                    qmlProxy.fittables.set()
                    qmlProxy.project.setNeedSaveToTrue()
                    qmlProxy.model.modelsChanged()
                })
*/
                qmlProxy.model.parameterEdited.connect(function(needSetFittables) {
                    //qmlProxy.model.parametersEdited(needSetFittables)
                    //qmlProxy.model.dataChanged()
                    qmlProxy.model.calculate()
                    if (needSetFittables) {
                        //print('!!!!!!!!!!', needSetFittables)
                        qmlProxy.fittables.set()
                    }
                    qmlProxy.project.setNeedSaveToTrue()
                })

                /*
                qmlProxy.model.parametersEdited.connect(function(needSetFittables) {
                    //qmlProxy.model.modelsChanged()
                    //qmlProxy.model.calculateData()
                    qmlProxy.model.dataChanged()
                    if (needSetFittables) {
                        qmlProxy.fittables.set()
                    }
                    qmlProxy.project.setNeedSaveToTrue()
                })
                */

                // Fitting

                /*
                qmlProxy.fitting.fitFinishedChanged.connect(function() {
                    print(`Fit finished: ${qmlProxy.fitting.fitFinished}`)
                    const needSetFittables = true
                    qmlProxy.model.parametersEdited(needSetFittables)
                })
                */

            }

        }

        //////////
        // Project
        //////////

        readonly property var project: QtObject {

            readonly property var _EMPTY_DATA: {
                'name': '',
                'description': '',
                'location': '',
                'creationDate': ''
            }

            readonly property var _DEFAULT_DATA: {
                'name': 'Default project',
                'description': 'Default project description',
                'location': '',
                'creationDate': ''
            }

            readonly property var _EXAMPLES: [
                {
                    'name': 'Horizontal line',
                    'description': 'Straight line, horizontal, PicoScope 2204A',
                    'path': '../Resources/Examples/HorizontalLine/project.json'
                },
                {
                    'name': 'Slanting line 1',
                    'description': 'Straight line, positive slope, Tektronix 2430A',
                    'path': '../Resources/Examples/SlantingLine1/project.json'
                },
                {
                    'name': 'Slanting line 2',
                    'description': 'Straight line, negative slope, Siglent SDS1202X-E',
                    'path': '../Resources/Examples/SlantingLine2/project.json'
                }
            ]

            property var data: _DEFAULT_DATA
            property var examples: _EXAMPLES
            property bool created: false
            property bool needSave: false

            function setNeedSaveToTrue() {
                needSave = true
            }

            function create() {
                data = _DEFAULT_DATA
                data.creationDate = `${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`
                dataChanged()  // Emit signal, as it is not emited automatically
                created = true
            }

            function editData(key, value) {
                if (data[key] === value) {
                    return
                }
                data[key] = value
                dataChanged()  // Emit signal, as it is not emited automatically
            }

            function save() {
                let out = {}
                if (created) {
                    out['project'] = data
                }
                if (qmlProxy.experiment.defined) {
                    out['experiment'] = qmlProxy.experiment.dataBlocksNoMeas
                }
                if (qmlProxy.model.defined) {
                    out['model'] = qmlProxy.model.dataBlocks
                }
                const filePath = `${out.project.location}/project.json`
                EaLogic.Utils.writeFile(filePath, JSON.stringify(project))
                needSave = false
            }
        }

        /////////////
        // Experiment
        /////////////

        readonly property var experiment: QtObject {

            readonly property var _EMPTY_DATA: [
                {
                    'name': '',
                    'params': {},
                    'xArray': [],
                    'yArray': []
                }
            ]

            readonly property var _DEFAULT_DATA: [
                {
                    'name': 'PicoScope',
                    'params': {
                        'xMin': {
                            'value': 0.0,
                            'fittable': false
                        },
                        'xMax': {
                            'value': 1.0,
                            'fittable': false
                        },
                        'xStep': {
                            'value': 0.01,
                            'fittable': false
                        }
                    },
                    'xArray': [],
                    'yArray': []
                }
            ]

            property var chartRanges: [ { 'xMin': 0, 'xMax': 1, 'yMin': 0, 'yMax': 1 } ]

            property var data: _EMPTY_DATA
            property bool defined: false

            function load() {
                data = _DEFAULT_DATA  // dataChanged() signal emited automatically
                const xMax = data[0].params.xMax.value
                const xMin = data[0].params.xMin.value
                const xStep = data[0].params.xStep.value
                const length = (xMax - xMin) / xStep + 1
                const xArray = Array.from({ length: length }, (_, i) => i / (length - 1))
                const slope = -3.0
                const yIntercept = 1.5
                const yArray = Logic.LineCalculator.pseudoMeasured(xArray, slope, yIntercept)
                data[0].xArray = xArray
                data[0].yArray = yArray
                dataChanged()  // Emit signal, as it is not emited automatically
                created = true
            }            

            function reset() {
                data = _EMPTY_DATA  // dataChanged() signal emited automatically
                created = false
            }

        }

        ////////
        // Model
        ////////

        readonly property var model: QtObject {
            signal parameterEdited(bool needSetFittables)
            //signal parametersEdited(bool needSetFittables)
            //signal modelAdded()
            //signal modelRemoved()

            readonly property var _EMPTY_DATA: [
                {
                    'name': '',
                    'params': {},
                    'yArray': []
                }
            ]

            readonly property var _DEFAULT_DATA: [
                {
                    'name': 'LineA',
                    'params': {
                        'slope': {
                            'value': 1.0,
                            'error': 0,
                            'min': -5,
                            'max': 5,
                            'unit': '',
                            'fittable': true,
                            'fit': true
                        },
                        'yIntercept': {
                            'value': 0.0,
                            'error': 0,
                            'min': -5,
                            'max': 5,
                            'unit': '',
                            'fittable': true,
                            'fit': true
                        }
                    },
                    'yArray': []
                },
                {
                    'name': 'LineB',
                    'params': {
                        'slope': {
                            'value': -1.5,
                            'error': 0,
                            'min': -5,
                            'max': 5,
                            'unit': '',
                            'fittable': true,
                            'fit': true
                        },
                        'yIntercept': {
                            'value': 0.5,
                            'error': 0,
                            'min': -5,
                            'max': 5,
                            'unit': '',
                            'fittable': true,
                            'fit': true
                        }
                    },
                    'yArray': []
                }
            ]

            property var data: _EMPTY_DATA
            property var totalYArray: []
            property bool created: false
            property int currentIndex: 0

            function load() {
                data = _DEFAULT_DATA  // dataChanged() signal emited automatically
                calculate()
                qmlProxy.fittables.set() //////////////////////////
                created = true
            }

            function reset() {
                data = _EMPTY_DATA  // dataChanged() signal emited automatically
                created = false
            }

            function calculate() {
                for (let i in data) {
                    calculateYArray(i)
                }
                dataChanged()  // Emit signal, as it is not emited automatically
                calculateTotalYArray()
            }

            function calculateYArray(i) {
                const xArray = qmlProxy.experiment.data[0].xArray
                const slope = data[i].params.slope.value
                const yIntercept = data[i].params.yIntercept.value
                const yArray = Logic.LineCalculator.calculated(xArray, slope, yIntercept)
                data[i].yArray = yArray
            }

            function calculateTotalYArray() {
                const length = data[0].yArray.length
                let out = Array(length).fill(0)
                for (const block of data) {
                    out = out.map((val, idx) => val + block.yArray[idx])
                }
                totalYArray = out  // totalYArrayChanged() signal emited automatically
            }

            function editParameter(currentModelIndex, name, item, value, needSetFittables) {
                if (item === 'value') {
                    value = parseFloat(value)
                } else if (item === 'fit') {
                    if (!value) {
                        data[currentModelIndex].params[name].error = 0
                    }
                }
                if (data[currentModelIndex].params[name][item] === value) {
                    return
                }
                data[currentModelIndex].params[name][item] = value
                parameterEdited(needSetFittables)
            }

        }

        //////////
        // Fitting
        //////////

        readonly property var fitting: QtObject {
            property bool isFittingNow: false

            function fit() {
                isFittingNow = true
                /*
                if (qmlProxy.model.fittables.slope.fit) {
                    qmlProxy.model.fittables.slope.value = -3.0015
                    qmlProxy.model.fittables.slope.error = 0.0023
                }
                if (qmlProxy.model.fittables.yIntercept.fit) {
                    qmlProxy.model.fittables.yIntercept.value = 1.4950
                    qmlProxy.model.fittables.yIntercept.error = 0.0045
                }
                */
                isFittingNow = false
            }
        }

        /////////////
        // Parameters
        /////////////

        readonly property var fittables: QtObject {
            property var data: []

            function edit(group, parentIndex, name, item, value) {
                const needSetFittables = false
                if (group === 'experiment') {
                    qmlProxy.experiment.editParameter(parentIndex, name, item, value, needSetFittables)
                } else if (group === 'model') {
                    qmlProxy.model.editParameter(parentIndex, name, item, value, needSetFittables)
                }
            }

            function set() {
                let _data = []
                for (let i in qmlProxy.experiment.data) {
                    const block = qmlProxy.experiment.data[i]
                    for (const name in block.params) {
                        const param = block.params[name]
                        if (param.fittable) {
                            let fittable = {}
                            fittable.group = 'experiment'
                            fittable.name = name
                            fittable.parentIndex = i
                            fittable.parentName = block.name
                            fittable.value = param.value
                            fittable.error = param.error
                            fittable.min = param.min
                            fittable.max = param.max
                            fittable.unit = param.unit
                            fittable.fit = param.fit
                            _data.push(fittable)
                        }
                    }
                }
                for (let i in qmlProxy.model.data) {
                    const block = qmlProxy.model.data[i]
                    for (const name in block.params) {
                        const param = block.params[name]
                        if (param.fittable) {
                            let fittable = {}
                            fittable.group = 'model'
                            fittable.name = name
                            fittable.parentIndex = i
                            fittable.parentName = block.name
                            fittable.value = param.value
                            fittable.error = param.error
                            fittable.min = param.min
                            fittable.max = param.max
                            fittable.unit = param.unit
                            fittable.fit = param.fit
                            _data.push(fittable)
                        }
                    }
                }
                if (_data.length !== 0) {
                    /*
                    for (let i = 0; i < 10000; ++i) {
                        _fittables.push(_fittables[0])
                    }
                    */
                    data = _data  // dataChanged() signal emited automatically
                }
            }

        }

        //////////
        // Summary
        //////////

        readonly property var summary: QtObject {
            property bool isCreated: false

            // https://stackoverflow.com/questions/17882518/reading-and-writing-files-in-qml-qt
            // https://stackoverflow.com/questions/57351643/how-to-save-dynamically-generated-web-page-in-qwebengineview
            function saveHtmlReport(fileUrl) {
                const webEngine = Globals.Refs.summaryReportWebEngine
                webEngine.runJavaScript("document.documentElement.outerHTML",
                                        function(htmlContent) {
                                            const status = EaLogic.Utils.writeFile(fileUrl, htmlContent)
                                        })
            }
        }

        /////////
        // Status
        /////////

        readonly property var status: QtObject {
            property string asXml:
                `<root>
                  <item>
                    <name>Calculations</name>
                    <value>CrysPy</value>
                  </item>
                  <item>
                    <name>Minimization</name>
                    <value>lmfit</value>
                  </item>
                </root>`
            property var asJson: [
                {
                    name: 'Calculations',
                    value: 'CrysPy'
                },
                {
                    name: 'Minimization',
                    value: 'lmfit'
                }
              ]
        }

        ///////////
        // Plotting
        ///////////

        readonly property var plotting: QtObject {
            readonly property bool useWebGL1d: false
            readonly property var libs1d: ['QtCharts']
            property string currentLib1d: 'QtCharts'
        }

    }

    // Charts

    property string currentLib1d: EaGlobals.Vars.currentLib1d
    onCurrentLib1dChanged: main.plotting.currentLib1d = currentLib1d

    // Logging

    property string loggingLevel: EaGlobals.Vars.loggingLevel
    onLoggingLevelChanged: main.logger.level = loggingLevel


    // Common functions

    function rangeValue(name) {
        if (!main.experiment.defined || !main.experiment.chartRanges.length) {
            return 0
        }
        const idx = main.experiment.currentIndex
        return main.experiment.chartRanges[idx][name]
    }

    // Project

    function projectMainParam(name) {
        if (!main.project.created) {
            return { 'value': '', 'prettyName': '' }
        }
        const param = main.project.dataBlock.params[name]
        if (typeof param === 'undefined') {
            return { 'value': '', 'prettyName': '' }
        }
        return main.project.dataBlock.params[name]
    }

    function projectLoopParam(loopName, paramName, rowIndex) {
        if (!main.project.created) {
            return {}
        }
        return main.project.dataBlock.loops[loopName][rowIndex][paramName]
    }

    function setProjectMainParam(param, field, value) {
        console.debug(`*** Editing project main param ${param.name} '${field}' to ${value} ***`)
        main.project.setMainParam(param.name, field, value)
    }

    function resetAll() {
        main.summary.resetAll()
        main.analysis.resetAll()
        main.experiment.resetAll()
        main.model.resetAll()
        main.project.resetAll()
        main.fittables.resetAll()
        main.data.resetAll()
        main.status.resetAll()
    }

    function disableAllPages() {
        disableAllPagesExceptProject()
        Globals.Vars.projectPageEnabled = false
    }

    function disableAllPagesExceptProject() {
        Globals.Vars.summaryPageEnabled = false
        Globals.Vars.analysisPageEnabled = false
        Globals.Vars.experimentPageEnabled = false
        Globals.Vars.modelPageEnabled = false
    }

    // Model

    function modelGroupTitle(title) {
        if (!main.model.defined) {
            return title
        }
        const count = main.model.dataBlocks.length
        return `${title} (${count})`
    }

    function modelLoopTitle(title, loopName) {
        if (!main.model.defined) {
            return title
        }
        const idx = main.model.currentIndex
        const count = main.model.dataBlocks[idx].loops[loopName].length
        return `${title} (${count})`
    }

    function modelMainParam(name) {
        if (!main.model.defined) {
            return {}
        }
        const idx = main.model.currentIndex
        return main.model.dataBlocks[idx].params[name]
    }

    function modelLoopParam(loopName, paramName, rowIndex, blockIndex = main.model.currentIndex) {
        if (!main.model.defined) {
            return {}
        }
        return main.model.dataBlocks[blockIndex].loops[loopName][rowIndex][paramName]
    }

    function setModelMainParamWithFullUpdate(param, field, value) {
        const idx = main.model.currentIndex
        console.debug(`*** Editing (full update) model no. ${idx + 1} main param ${param.name} '${field}' to ${value} ***`)
        main.model.setMainParamWithFullUpdate(idx, param.name, field, value)
    }

    function setModelMainParam(param, field, value) {
        const idx = main.model.currentIndex
        console.debug(`*** Editing model no. ${idx + 1} main param ${param.name} '${field}' to ${value} ***`)
        main.model.setMainParam(idx, param.name, field, value)
    }

    function setModelLoopParamWithFullUpdate(param, field, value) {
        const idx = main.model.currentIndex
        console.debug(`*** Editing (full update) model no. ${idx + 1} loop param ${param.loopName}${param.name}[${param.idx}] '${field}' to ${value} ***`)
        main.model.setLoopParamWithFullUpdate(idx, param.loopName, param.name, param.idx, field, value)
    }

    function setModelLoopParam(param, field, value) {
        const idx = main.model.currentIndex
        console.debug(`*** Editing model no. ${idx + 1} loop param ${param.loopName}${param.name}[${param.idx}] '${field}' to ${value} ***`)
        main.model.setLoopParam(idx, param.loopName, param.name, param.idx, field, value)
    }

    function removeModelLoopRow(loopName, idx) {
        console.debug(`*** Removing model loop row ${loopName}[${idx}] ***`)
        main.model.removeLoopRow(loopName, idx)
    }

    function appendModelLoopRow(loopName) {
        console.debug(`*** Appending model loop row ${loopName} ***`)
        main.model.appendLoopRow(loopName)
    }

    function duplicateModelLoopRow(loopName, idx) {
        console.debug(`*** Duplicating model loop row ${loopName}[${idx}] ***`)
        main.model.duplicateLoopRow(loopName, idx)
    }

    // Experiment

    function experimentGroupTitle(title) {
        if (!main.experiment.defined) {
            return title
        }
        const count = main.experiment.dataBlocksNoMeas.length
        return `${title} (${count})`
    }

    function experimentLoopTitle(title, loopName) {
        if (!main.experiment.defined) {
            return title
        }
        const idx = main.experiment.currentIndex
        const count = main.experiment.dataBlocksNoMeas[idx].loops[loopName].length
        return `${title} (${count})`
    }

    function experimentMainParam(name) {
        if (!main.experiment.defined) {
            return {}
        }
        const idx = main.experiment.currentIndex
        return main.experiment.dataBlocksNoMeas[idx].params[name]
    }

    function experimentLoopParam(loopName, paramName, rowIndex) {
        if (!main.experiment.defined) {
            return {}
        }
        const idx = main.experiment.currentIndex
        return main.experiment.dataBlocksNoMeas[idx].loops[loopName][rowIndex][paramName]
    }

    function setExperimentMainParamWithFullUpdate(param, field, value) {
        const idx = main.experiment.currentIndex
        console.debug(`*** Editing (full update) experiment no. ${idx + 1} main param ${param.name} '${field}' to ${value} ***`)
        main.experiment.setMainParamWithFullUpdate(idx, param.name, field, value)
    }

    function setExperimentMainParam(param, field, value) {
        const idx = main.experiment.currentIndex
        console.debug(`*** Editing experiment no. ${idx + 1} main param ${param.name} '${field}' to ${value} ***`)
        main.experiment.setMainParam(idx, param.name, field, value)
    }

    function setExperimentLoopParamWithFullUpdate(param, field, value) {
        const idx = main.experiment.currentIndex
        console.debug(`*** Editing (full update) experiment no. ${idx + 1} loop param ${param.loopName}${param.name}[${param.idx}] '${field}' to ${value} ***`)
        main.experiment.setLoopParamWithFullUpdate(idx, param.loopName, param.name, param.idx, field, value)
    }

    function setExperimentLoopParam(param, field, value) {
        const idx = main.experiment.currentIndex
        console.debug(`*** Editing experiment no. ${idx + 1} loop param ${param.loopName}${param.name}[${param.idx}] '${field}' to ${value} ***`)
        main.experiment.setLoopParam(idx, param.loopName, param.name, param.idx, field, value)
    }

    function removeExperimentLoopRow(loopName, idx) {
        console.debug(`*** Removing experiment loop row ${loopName}[${idx}] ***`)
        main.experiment.removeLoopRow(loopName, idx)
    }

    function appendExperimentLoopRow(loopName) {
        console.debug(`*** Appending experiment loop row ${loopName} ***`)
        main.experiment.appendLoopRow(loopName)
    }

    function paramName(param, format) {

        //console.info(JSON.stringify(param))

        const textFont = `'${EaStyle.Fonts.fontFamily}'`
        const iconFont = `'${EaStyle.Fonts.iconsFamily}'`
        const textColor = `'${EaStyle.Colors.themeForeground}'`
        const iconColor = `'${EaStyle.Colors.themeForegroundMinor}'`

        let blockIconColor = iconColor
        if (param.blockType === "model") {
            blockIconColor = `'${EaStyle.Colors.models[param.blockIndex]}'`
        } else if (param.blockType === "experiment") {
            blockIconColor = `'${EaStyle.Colors.chartForegroundsExtra[2]}'`
        }

        let groupIconColor = iconColor
        if (param.loopName === "_atom_site") {
            groupIconColor = `'${main.model.atomData(
                        modelLoopParam('_atom_site', '_type_symbol', param.rowIndex, param.blockIndex).value, 'color'
                        )}'`
        } else if (param.loopName === "_phase") {
            groupIconColor = `'${EaStyle.Colors.models[param.rowIndex]}'`
        }

        let prettyRowName = param.rowName
        if (param.prettyRowName) {
            prettyRowName = param.prettyRowName
        }

        const blockTypeHtml =       `<font color=${blockIconColor} face=${textFont}>${param.blockType}</font>`
        const blockIconHtml =       `<font color=${blockIconColor} face=${iconFont}>${param.blockIcon}</font>`
        const blockIndexHtml =      `<font color=${blockIconColor} face=${textFont}>${param.blockIndex + 1}</font>`
        const blockNameHtml =       `<font color=${blockIconColor} face=${textFont}>${param.blockName}</font>`

        const groupIconHtml =       `<font color=${groupIconColor} face=${iconFont}>${param.groupIcon}</font>`
        const prettyloopNameHtml =  `<font color=${groupIconColor} face=${textFont}>${param.prettyLoopName}</font>`
        const loopNameHtml =        `<font color=${groupIconColor} face=${textFont}>${param.loopName}</font>`
        const rowIndexHtml =        `<font color=${groupIconColor} face=${textFont}>${param.rowIndex + 1}</font>`
        const rowNameHtml =         `<font color=${groupIconColor} face=${textFont}>${param.rowName}</font>`
        const rowPrettyNameHtml =   `<font color=${groupIconColor} face=${textFont}>${prettyRowName}</font>`

        const paramIconHtml =       `<font color=${iconColor}      face=${iconFont}>${param.icon}</font>`
        const paramPrettyNameHtml = `<font color=${textColor}      face=${textFont}><b>${param.prettyName}</b></font>`
        const paramNameHtml =       `<font color=${textColor}      face=${textFont}><b>${param.name}</b></font>`
        const paramTitleHtml =      `<font color=${textColor}      face=${textFont}><b>${param.title}</b></font>`

        let name = ''
        let _ = ''



        if (format === EaGlobals.Vars.ShortestWithIconsAndPrettyLabels) {
            _ = '&nbsp;&nbsp;'
            name = `${blockIconHtml}${_}${groupIconHtml}`
            if (param.loopName) name += `${_}${rowPrettyNameHtml}${_}${paramIconHtml}${_}${paramTitleHtml}`
            else name += `${_}${paramIconHtml}${_}${paramTitleHtml}`
        } else if (format === EaGlobals.Vars.ReducedWithIconsAndPrettyLabels) {
            _ = '&nbsp;&nbsp;'
            name = `${blockIconHtml}${_}${blockNameHtml}${_}${groupIconHtml}`
            if (param.loopName) name += `${_}${rowPrettyNameHtml}${_}${paramIconHtml}${_}${paramPrettyNameHtml}`
            else name += `${_}${paramIconHtml}${_}${paramPrettyNameHtml}`
        } else if (format === EaGlobals.Vars.FullWithIconsAndPrettyLabels) {
            _ = '&nbsp;&nbsp;'
            name = `${blockIconHtml}${_}${blockTypeHtml}${_}${blockNameHtml}${_}${groupIconHtml}`
            if (param.loopName) name += `${_}${prettyloopNameHtml}${_}${rowPrettyNameHtml}${_}${paramIconHtml}${_}${paramPrettyNameHtml}`
            else name += `${_}${paramIconHtml}${_}${paramPrettyNameHtml}`
        } else if (format === EaGlobals.Vars.FullWithPrettyLabels) {
            _ = '&nbsp;&nbsp;'
            name = `${blockTypeHtml}${_}${blockNameHtml}`
            if (param.loopName) name += `${_}${prettyloopNameHtml}${_}${rowPrettyNameHtml}${_}${paramPrettyNameHtml}`
            else name += `${_}${paramPrettyNameHtml}`
        } else if (format === EaGlobals.Vars.FullWithLabels) {
            _ = '.'
            name = `${blockTypeHtml}[${blockNameHtml}]`
            if (param.loopName) name += `${_}${loopNameHtml}${paramNameHtml}[${rowNameHtml}]`
            else name += `${_}${paramNameHtml}`
        } else if (format === EaGlobals.Vars.FullWithIndices) {
            _ = '.'
            name = `${blockTypeHtml}[${blockIndexHtml}]`
            if (param.loopName) name += `${_}${loopNameHtml}${paramNameHtml}[${rowIndexHtml}]`
            else name += `${_}${paramNameHtml}`
        } else if (format === EaGlobals.Vars.PlainFullWithLabels) {
            _ = '.'
            name = `${param.blockType}[${param.blockName}]`
            if (param.loopName) name += `${_}${param.loopName}${param.name}[${param.rowName}]`
            else name += `${_}${param.name}`
        }

        //console.info(name)
        return name
    }


}
