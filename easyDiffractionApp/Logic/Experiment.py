# SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
# SPDX-License-Identifier: BSD-3-Clause
# © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import os
import copy
import numpy as np
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtCore import QFile, QTextStream, QIODevice
from PySide6.QtQml import QJSValue

from EasyApp.Logic.Logging import console
from Logic.Helpers import IO
from Logic.Calculators import CryspyParser
from Logic.Data import Data

try:
    import cryspy
    from cryspy.H_functions_global.function_1_cryspy_objects import \
        str_to_globaln
    from cryspy.procedure_rhochi.rhochi_by_dictionary import \
        rhochi_calc_chi_sq_by_dictionary
    console.debug('CrysPy module imported')
except ImportError:
    console.debug('No CrysPy module found')


_DEFAULT_DATA_BLOCK_NO_MEAS = """data_pnd

_diffrn_radiation_probe neutron
_diffrn_radiation_wavelength 1.9

_pd_meas_2theta_offset 0.0

_pd_instr_resolution_u 0.04
_pd_instr_resolution_v -0.05
_pd_instr_resolution_w 0.06
_pd_instr_resolution_x 0
_pd_instr_resolution_y 0

_pd_instr_reflex_asymmetry_p1 0
_pd_instr_reflex_asymmetry_p2 0
_pd_instr_reflex_asymmetry_p3 0
_pd_instr_reflex_asymmetry_p4 0

loop_
_phase_label
_phase_scale
ph 1.0

loop_
_pd_background_2theta
_pd_background_intensity
0 100
180 100

loop_
_pd_meas_2theta
_pd_meas_intensity
_pd_meas_intensity_sigma
"""

_DEFAULT_DATA_BLOCK = _DEFAULT_DATA_BLOCK_NO_MEAS + """36.5 1    1
37.0 10   3
37.5 700  25
38.0 1100 30
38.5 50   7
39.0 1    1
"""


class Experiment(QObject):
    definedChanged = Signal()
    currentIndexChanged = Signal()
    dataBlocksChanged = Signal()
    dataBlocksNoMeasChanged = Signal()
    dataBlocksMeasOnlyChanged = Signal()
    dataBlocksCifChanged = Signal()
    dataBlocksCifNoMeasChanged = Signal()
    dataBlocksCifMeasOnlyChanged = Signal()
    yMeasArraysChanged = Signal()
    yBkgArraysChanged = Signal()
    yCalcTotalArraysChanged = Signal()
    yResidArraysChanged = Signal()
    xBraggDictsChanged = Signal()
    chartRangesChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent

        self._defined = False
        self._currentIndex = -1

        self._dataBlocksNoMeas = []
        self._dataBlocksMeasOnly = []

        self._dataBlocksCif = []
        self._dataBlocksCifNoMeas = []
        self._dataBlocksCifMeasOnly = []

        self._xArrays = []
        self._yMeasArrays = []
        self._syMeasArrays = []
        self._yBkgArrays = []
        self._yCalcTotalArrays = []
        self._yResidArrays = []
        self._xBraggDicts = []

        self._chartRanges = []

    # QML accessible properties

    @Property('QVariant', notify=chartRangesChanged)
    def chartRanges(self):
        return self._chartRanges

    @Property(bool, notify=definedChanged)
    def defined(self):
        return self._defined

    @defined.setter
    def defined(self, newValue):
        if self._defined == newValue:
            return
        self._defined = newValue
        console.debug(IO.formatMsg('main', f'Experiment defined: {newValue}'))
        self.definedChanged.emit()

    @Property(int, notify=currentIndexChanged)
    def currentIndex(self):
        return self._currentIndex

    @currentIndex.setter
    def currentIndex(self, newValue):
        if self._currentIndex == newValue:
            return
        self._currentIndex = newValue
        console.debug(f"Current experiment index: {newValue}")
        self.currentIndexChanged.emit()

    @Property('QVariant', notify=dataBlocksMeasOnlyChanged)
    def dataBlocksMeasOnly(self):
        #console.error('EXPERIMENT DATABLOCK (MEAS ONLY) GETTER')
        return self._dataBlocksMeasOnly

    @Property('QVariant', notify=dataBlocksNoMeasChanged)
    def dataBlocksNoMeas(self):
        #console.error('EXPERIMENT DATABLOCK (NO MEAS) GETTER')
        return self._dataBlocksNoMeas

    @Property('QVariant', notify=dataBlocksCifChanged)
    def dataBlocksCif(self):
        return self._dataBlocksCif

    @Property('QVariant', notify=dataBlocksCifNoMeasChanged)
    def dataBlocksCifNoMeas(self):
        return self._dataBlocksCifNoMeas

    @Property('QVariant', notify=dataBlocksCifMeasOnlyChanged)
    def dataBlocksCifMeasOnly(self):
        return self._dataBlocksCifMeasOnly

    # QML accessible methods

    @Slot()
    def addDefaultExperiment(self):
        console.debug('Adding default experiment')
        self.loadExperimentsFromEdCif(_DEFAULT_DATA_BLOCK)

    @Slot('QVariant')
    def loadExperimentsFromResources(self, fpaths):
        if type(fpaths) == QJSValue:
            fpaths = fpaths.toVariant()
        for fpath in fpaths:
            console.debug(f"Loading experiment(s) from: {fpath}")
            file = QFile(fpath)
            if not file.open(QIODevice.ReadOnly | QIODevice.Text):
                console.error('Not found in resources')
                return
            stream = QTextStream(file)
            edCif = stream.readAll()
            self.loadExperimentsFromEdCif(edCif)

    @Slot('QVariant')
    def loadExperimentsFromFiles(self, fpaths):
        if type(fpaths) == QJSValue:
            fpaths = fpaths.toVariant()
        for fpath in fpaths:
            fpath = fpath.toLocalFile()
            fpath = IO.generalizePath(fpath)
            _, fext = os.path.splitext(fpath)
            console.debug(f"Loading experiment(s) from: {fpath}")
            with open(fpath, 'r') as file:
                fileContent = file.read()
            if fext == '.xye':
                fileContent = _DEFAULT_DATA_BLOCK_NO_MEAS + fileContent
            self.loadExperimentsFromEdCif(fileContent)

    @Slot(str)
    def loadExperimentsFromEdCif(self, edCif):
        cryspyObj = self._proxy.data._cryspyObj
        cryspyCif = CryspyParser.edCifToCryspyCif(edCif)
        cryspyExperimentsObj = str_to_globaln(cryspyCif)

        # Add/modify CryspyObj with ranges based on the measured data points in _pd_meas loop
        pd_meas_2theta_range_min = 0  # default value to be updated later
        pd_meas_2theta_range_max = 180  # default value to be updated later
        defaultEdRangeCif = f'_pd_meas_2theta_range_min {pd_meas_2theta_range_min}\n_pd_meas_2theta_range_max {pd_meas_2theta_range_max}'
        cryspyRangeCif = CryspyParser.edCifToCryspyCif(defaultEdRangeCif)
        cryspyRangeObj = str_to_globaln(cryspyRangeCif).items
        for dataBlock in cryspyExperimentsObj.items:
            for item in dataBlock.items:
                if type(item) == cryspy.C_item_loop_classes.cl_1_pd_meas.PdMeasL:
                    pd_meas_2theta_range_min = item.items[0].ttheta
                    pd_meas_2theta_range_max = item.items[-1].ttheta
                    cryspyRangeObj[0].ttheta_min = pd_meas_2theta_range_min
                    cryspyRangeObj[0].ttheta_max = pd_meas_2theta_range_max
            dataBlock.add_items(cryspyRangeObj)

        # Add/modify CryspyObj with phases based on the already loaded phases
        loadedModelNames = [block['name']['value'] for block in self._proxy.model.dataBlocks]
        for dataBlock in cryspyExperimentsObj.items:
            for itemIdx, item in enumerate(dataBlock.items):
                if type(item) == cryspy.C_item_loop_classes.cl_1_phase.PhaseL:
                    cryspyModelNames = [phase.label for phase in item.items]
                    for modelIdx, modelName in enumerate(cryspyModelNames):
                        if modelName not in loadedModelNames:
                            del item.items[modelIdx]
                    if not len(item.items):
                        del dataBlock.items[itemIdx]
            itemTypes = [type(item) for item in dataBlock.items]
            if cryspy.C_item_loop_classes.cl_1_phase.PhaseL not in itemTypes:
                defaultEdModelsCif = 'loop_\n_phase_label\n_phase_scale'
                for modelName in loadedModelNames:
                    defaultEdModelsCif += f'\n{modelName} 1.0'
                cryspyPhasesCif = CryspyParser.edCifToCryspyCif(defaultEdModelsCif)
                cryspyPhasesObj = str_to_globaln(cryspyPhasesCif).items
                dataBlock.add_items(cryspyPhasesObj)

        experimentsCountBefore = len(self.cryspyObjExperiments())
        cryspyObj.add_items(cryspyExperimentsObj.items)
        experimentsCountAfter = len(self.cryspyObjExperiments())
        success = experimentsCountAfter - experimentsCountBefore

        if success:
            cryspyExperimentsDict = cryspyExperimentsObj.get_dictionary()
            edExperimentsMeasOnly, edExperimentsNoMeas = CryspyParser.cryspyObjAndDictToEdExperiments(cryspyExperimentsObj,
                                                                                                      cryspyExperimentsDict)

            self._proxy.data._cryspyDict.update(cryspyExperimentsDict)
            self._dataBlocksMeasOnly += edExperimentsMeasOnly
            self._dataBlocksNoMeas += edExperimentsNoMeas

            self._currentIndex = len(self.dataBlocksNoMeas) - 1
            if not self.defined:
                self.defined = bool(len(self.dataBlocksNoMeas))

            console.debug(IO.formatMsg('sub', f'{len(edExperimentsMeasOnly)} experiment(s)', 'meas data only', 'to intern dataset', 'added'))
            console.debug(IO.formatMsg('sub', f'{len(edExperimentsNoMeas)} experiment(s)', 'without meas data', 'to intern dataset', 'added'))

            self.dataBlocksChanged.emit()
        else:
            console.debug(IO.formatMsg('sub', 'No experiment(s)', '', 'to intern dataset', 'added'))

    @Slot(str)
    def replaceExperiment(self, edCif=''):
        console.debug("Cryspy obj and dict need to be replaced")

        currentDataBlock = self.dataBlocksNoMeas[self.currentIndex]
        currentExperimentName = currentDataBlock['name']['value']

        cryspyObjBlockNames = [item.data_name for item in self._proxy.data._cryspyObj.items]
        cryspyObjBlockIdx = cryspyObjBlockNames.index(currentExperimentName)

        cryspyDictBlockName = f'pd_{currentExperimentName}'

        if not edCif:
            edCif = CryspyParser.dataBlockToCif(currentDataBlock)
        cryspyCif = CryspyParser.edCifToCryspyCif(edCif)
        cryspyExperimentsObj = str_to_globaln(cryspyCif)
        cryspyExperimentsDict = cryspyExperimentsObj.get_dictionary()
        _, edExperimentsNoMeas = CryspyParser.cryspyObjAndDictToEdExperiments(cryspyExperimentsObj,
                                                                              cryspyExperimentsDict)

        self._proxy.data._cryspyObj.items[cryspyObjBlockIdx] = cryspyExperimentsObj.items[0]
        self._proxy.data._cryspyDict[cryspyDictBlockName] = cryspyExperimentsDict[cryspyDictBlockName]
        self._dataBlocksNoMeas[self.currentIndex] = edExperimentsNoMeas[0]

        console.debug(f"Experiment data block '{currentExperimentName}' (no. {self.currentIndex + 1}) (without measured data) has been replaced")
        self.dataBlocksNoMeasChanged.emit()  # self.dataBlocksNoMeasChanged.emit(blockIdx)

#        # remove experiment from self._proxy.data._cryspyDict
#        currentExperimentName = self.dataBlocks[self.currentIndex]['name']
#        del self._proxy.data._cryspyDict[f'pd_{currentExperimentName}']
#
#        # add experiment to self._proxy.data._cryspyDict
#        cifNoMeas = CryspyParser.dataBlocksToCif(self._dataBlocks)
#        cifMeasOnly = self.dataBlocksCifMeasOnly
#        edCif = cifNoMeas + '\n' + cifMeasOnly
#        self.loadExperimentsFromEdCif(edCif)

    @Slot(int)
    def removeExperiment(self, index):
        console.debug(f"Removing experiment no. {index + 1}")
        self.currentIndex = index - 1
        del self._dataBlocksNoMeas[index]
        del self._dataBlocksMeasOnly[index]
        del self._xArrays[index]
        del self._yMeasArrays[index]
        del self._yBkgArrays[index]

        self.defined = bool(len(self.dataBlocksNoMeas))

        self.dataBlocksNoMeasChanged.emit()
        self.dataBlocksMeasOnlyChanged.emit()
        self.yMeasArraysChanged.emit()
        self.yBkgArraysChanged.emit()
        console.debug(f"Experiment no. {index + 1} has been removed")

    @Slot()
    def resetAll(self):
        self.defined = False
        self._currentIndex = -1
        self._dataBlocksNoMeas = []
        self._dataBlocksMeasOnly = []
        self._dataBlocksCif = []
        self._dataBlocksCifNoMeas = ""
        self._dataBlocksCifMeasOnly = ""
        self._xArrays = []
        self._yMeasArrays = []
        self._syMeasArrays = []
        self._yBkgArrays = []
        self._yCalcTotalArrays = []
        self._yResidArrays = []
        self._xBraggDicts = []
        self._chartRanges = []
        #self.dataBlocksChanged.emit()
        console.debug("All experiments removed")

    @Slot(int, str, str, 'QVariant')
    def setMainParamWithFullUpdate(self, blockIndex, paramName, field, value):
        changedIntern = self.editDataBlockMainParam(blockIndex, paramName, field, value)
        if not changedIntern:
            return
        self.replaceExperiment()

    @Slot(int, str, str, 'QVariant')
    def setMainParam(self, blockIndex, paramName, field, value):
        changedIntern = self.editDataBlockMainParam(blockIndex, paramName, field, value)
        changedCryspy = self.editCryspyDictByMainParam(blockIndex, paramName, field, value)
        if changedIntern and changedCryspy:
            self.dataBlocksNoMeasChanged.emit()

    @Slot(int, str, str, int, str, 'QVariant')
    def setLoopParamWithFullUpdate(self, blockIndex, loopName, paramName, rowIndex, field, value):
        changedIntern = self.editDataBlockLoopParam(blockIndex, loopName, paramName, rowIndex, field, value)
        if not changedIntern:
            return
        self.replaceExperiment()

    @Slot(int, str, str, int, str, 'QVariant')
    def setLoopParam(self, blockIndex, loopName, paramName, rowIndex, field, value):
        changedIntern = self.editDataBlockLoopParam(blockIndex, loopName, paramName, rowIndex, field, value)
        changedCryspy = self.editCryspyDictByLoopParam(blockIndex, loopName, paramName, rowIndex, field, value)
        if changedIntern and changedCryspy:
            self.dataBlocksNoMeasChanged.emit()

    @Slot(str, int)
    def removeLoopRow(self, loopName, rowIndex):
        self.removeDataBlockLoopRow(loopName, rowIndex)
        self.replaceExperiment()

    @Slot(str)
    def appendLoopRow(self, loopName):
        self.appendDataBlockLoopRow(loopName)
        self.replaceExperiment()

    @Slot()
    def resetBkgToDefault(self):
        self.resetDataBlockBkgToDefault()
        self.replaceExperiment()

    # Private methods

    def cryspyObjExperiments(self):
        cryspyObj = self._proxy.data._cryspyObj
        cryspyExperimentType = cryspy.E_data_classes.cl_2_pd.Pd
        experiments = [block for block in cryspyObj.items if type(block) == cryspyExperimentType]
        return experiments

    def removeDataBlockLoopRow(self, loopName, rowIndex):
        block = 'experiment'
        blockIndex = self._currentIndex
        del self._dataBlocksNoMeas[blockIndex]['loops'][loopName][rowIndex]

        console.debug(f"Intern dict ▌ {block}[{blockIndex}].{loopName}[{rowIndex}] has been removed")

    def appendDataBlockLoopRow(self, loopName):
        block = 'experiment'
        blockIndex = self._currentIndex

        lastBkgPoint = self._dataBlocksNoMeas[blockIndex]['loops'][loopName][-1]

        newBkgPoint = copy.deepcopy(lastBkgPoint)
        newBkgPoint['_2theta']['value'] += 10

        self._dataBlocksNoMeas[blockIndex]['loops'][loopName].append(newBkgPoint)
        atomsCount = len(self._dataBlocksNoMeas[blockIndex]['loops'][loopName])

        console.debug(f"Intern dict ▌ {block}[{blockIndex}].{loopName}[{atomsCount}] has been added")

    def resetDataBlockBkgToDefault(self):
        block = 'experiment'
        blockIndex = self._currentIndex
        loopName = '_pd_background'

        firstBkgPoint = copy.deepcopy(self._dataBlocksNoMeas[blockIndex]['loops'][loopName][0])  # copy of the 1st point
        firstBkgPoint['_2theta']['value'] = 0
        firstBkgPoint['_intensity']['value'] = 0

        lastBkgPoint = copy.deepcopy(firstBkgPoint)
        lastBkgPoint['_2theta']['value'] = 180

        self._dataBlocksNoMeas[blockIndex]['loops'][loopName] = [firstBkgPoint, lastBkgPoint]

        console.debug(f"Intern dict ▌ {block}[{blockIndex}].{loopName} has been reset to default values")

    def editDataBlockMainParam(self, blockIndex, paramName, field, value):
        block = 'experiment'
        oldValue = self._dataBlocksNoMeas[blockIndex]['params'][paramName][field]
        if oldValue == value:
            return False
        self._dataBlocksNoMeas[blockIndex]['params'][paramName][field] = value
        if type(value) == float:
            console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value:.6f}', f'{block}[{blockIndex}].{paramName}.{field}'))
        else:
            console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value}', f'{block}[{blockIndex}].{paramName}.{field}'))
        return True

    def editDataBlockLoopParam(self, blockIndex, loopName, paramName, rowIndex, field, value):
        block = 'experiment'
        oldValue = self._dataBlocksNoMeas[blockIndex]['loops'][loopName][rowIndex][paramName][field]
        if oldValue == value:
            return False
        self._dataBlocksNoMeas[blockIndex]['loops'][loopName][rowIndex][paramName][field] = value
        if type(value) == float:
            console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value:.6f}', f'{block}[{blockIndex}].{loopName}[{rowIndex}].{paramName}.{field}'))
        else:
            console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value}', f'{block}[{blockIndex}].{loopName}[{rowIndex}].{paramName}.{field}'))
        return True

    def editCryspyDictByMainParam(self, blockIndex, paramName, field, value):
        if field != 'value' and field != 'fit':
            return True

        path, value = self.cryspyDictPathByMainParam(blockIndex, paramName, value)
        if field == 'fit':
            path[1] = f'flags_{path[1]}'

        oldValue = self._proxy.data._cryspyDict[path[0]][path[1]][path[2]]
        if oldValue == value:
            return False
        self._proxy.data._cryspyDict[path[0]][path[1]][path[2]] = value

        console.debug(IO.formatMsg('sub', 'Cryspy dict', f'{oldValue} → {value}', f'{path}'))
        return True

    def editCryspyDictByLoopParam(self, blockIndex, loopName, paramName, rowIndex, field, value):
        if field != 'value' and field != 'fit':
            return True

        path, value = self.cryspyDictPathByLoopParam(blockIndex, loopName, paramName, rowIndex, value)
        if field == 'fit':
            path[1] = f'flags_{path[1]}'

        oldValue = self._proxy.data._cryspyDict[path[0]][path[1]][path[2]]
        if oldValue == value:
            return False
        self._proxy.data._cryspyDict[path[0]][path[1]][path[2]] = value

        console.debug(IO.formatMsg('sub', 'Cryspy dict', f'{oldValue} → {value}', f'{path}'))
        return True

    def cryspyDictPathByMainParam(self, blockIndex, paramName, value):
        blockName = self._dataBlocksNoMeas[blockIndex]['name']['value']
        path = ['','','']
        path[0] = f"pd_{blockName}"

        # _diffrn_radiation
        if paramName == '_diffrn_radiation_wavelength':
            path[1] = 'wavelength'
            path[2] = 0

        # _pd_meas_2theta_offset
        elif paramName == '_pd_meas_2theta_offset':
            path[1] = 'offset_ttheta'
            path[2] = 0
            value = np.deg2rad(value)

        # _pd_instr_resolution
        elif paramName == '_pd_instr_resolution_u':
            path[1] = 'resolution_parameters'
            path[2] = 0
        elif paramName == '_pd_instr_resolution_v':
            path[1] = 'resolution_parameters'
            path[2] = 1
        elif paramName == '_pd_instr_resolution_w':
            path[1] = 'resolution_parameters'
            path[2] = 2
        elif paramName == '_pd_instr_resolution_x':
            path[1] = 'resolution_parameters'
            path[2] = 3
        elif paramName == '_pd_instr_resolution_y':
            path[1] = 'resolution_parameters'
            path[2] = 4
        elif paramName == '_pd_instr_resolution_z':
            path[1] = 'resolution_parameters'
            path[2] = 5

        # _pd_instr_reflex_asymmetry
        elif paramName == '_pd_instr_reflex_asymmetry_p1':
            path[1] = 'asymmetry_parameters'
            path[2] = 0
        elif paramName == '_pd_instr_reflex_asymmetry_p2':
            path[1] = 'asymmetry_parameters'
            path[2] = 1
        elif paramName == '_pd_instr_reflex_asymmetry_p3':
            path[1] = 'asymmetry_parameters'
            path[2] = 2
        elif paramName == '_pd_instr_reflex_asymmetry_p4':
            path[1] = 'asymmetry_parameters'
            path[2] = 3

        # undefined
        else:
            console.error(f"Undefined parameter name '{paramName}'")

        return path, value

    def cryspyDictPathByLoopParam(self, blockIndex, loopName, paramName, rowIndex, value):
        blockName = self._dataBlocksNoMeas[blockIndex]['name']['value']
        path = ['','','']
        path[0] = f"pd_{blockName}"

        # _pd_background
        if loopName == '_pd_background':
            if paramName == '_2theta':
                path[1] = 'background_ttheta'
                path[2] = rowIndex
                value = np.deg2rad(value)
            if paramName == '_intensity':
                path[1] = 'background_intensity'
                path[2] = rowIndex

        # _phase
        if loopName == '_phase':
            if paramName == '_scale':
                path[1] = 'phase_scale'
                path[2] = rowIndex

        return path, value

    def paramValueByFieldAndCrypyParamPath(self, field, path):  # NEED FIX: code duplicate of editDataBlockByLmfitParams
        block, group, idx = path

        # pd (powder diffraction) block
        if block.startswith('pd_'):
            blockName = block[3:]
            loopName = None
            paramName = None
            rowIndex = None

            # wavelength
            if group == 'wavelength':
                paramName = '_diffrn_radiation_wavelength'

            # offset_ttheta
            elif group == 'offset_ttheta':
                paramName = '_pd_meas_2theta_offset'

            # resolution_parameters
            elif group == 'resolution_parameters':
                if idx[0] == 0:
                    paramName = '_pd_instr_resolution_u'
                elif idx[0] == 1:
                    paramName = '_pd_instr_resolution_v'
                elif idx[0] == 2:
                    paramName = '_pd_instr_resolution_w'
                elif idx[0] == 3:
                    paramName = '_pd_instr_resolution_x'
                elif idx[0] == 4:
                    paramName = '_pd_instr_resolution_y'
                elif idx[0] == 5:
                    paramName = '_pd_instr_resolution_z'

            # asymmetry_parameters
            elif group == 'asymmetry_parameters':
                if idx[0] == 0:
                    paramName = '_pd_instr_reflex_asymmetry_p1'
                elif idx[0] == 1:
                    paramName = '_pd_instr_reflex_asymmetry_p2'
                elif idx[0] == 2:
                    paramName = '_pd_instr_reflex_asymmetry_p3'
                elif idx[0] == 3:
                    paramName = '_pd_instr_reflex_asymmetry_p4'

            # background_ttheta
            elif group == 'background_ttheta':
                loopName = '_pd_background'
                paramName = '_2theta'
                rowIndex = idx[0]

            # background_intensity
            elif group == 'background_intensity':
                loopName = '_pd_background'
                paramName = '_intensity'
                rowIndex = idx[0]

            # phase_scale
            elif group == 'phase_scale':
                loopName = '_phase'
                paramName = '_scale'
                rowIndex = idx[0]

            blockIndex = [block['name']['value'] for block in self._dataBlocksNoMeas].index(blockName)

            if loopName is None:
                return self.dataBlocksNoMeas[blockIndex]['params'][paramName][field]
            else:
                return self.dataBlocksNoMeas[blockIndex]['loops'][loopName][rowIndex][paramName][field]

        return None

    def editDataBlockByLmfitParams(self, params):
        for param in params.values():
            block, group, idx = Data.strToCryspyDictParamPath(param.name)

            # pd (powder diffraction) block
            if block.startswith('pd_'):
                blockName = block[3:]
                loopName = None
                paramName = None
                rowIndex = None
                value = param.value
                error = 0
                if param.stderr is not None:
                    error = param.stderr

                # wavelength
                if group == 'wavelength':
                    paramName = '_diffrn_radiation_wavelength'

                # offset_ttheta
                elif group == 'offset_ttheta':
                    paramName = '_pd_meas_2theta_offset'
                    value = np.rad2deg(value)

                # resolution_parameters
                elif group == 'resolution_parameters':
                    if idx[0] == 0:
                        paramName = '_pd_instr_resolution_u'
                    elif idx[0] == 1:
                        paramName = '_pd_instr_resolution_v'
                    elif idx[0] == 2:
                        paramName = '_pd_instr_resolution_w'
                    elif idx[0] == 3:
                        paramName = '_pd_instr_resolution_x'
                    elif idx[0] == 4:
                        paramName = '_pd_instr_resolution_y'
                    elif idx[0] == 5:
                        paramName = '_pd_instr_resolution_z'

                # asymmetry_parameters
                elif group == 'asymmetry_parameters':
                    if idx[0] == 0:
                        paramName = '_pd_instr_reflex_asymmetry_p1'
                    elif idx[0] == 1:
                        paramName = '_pd_instr_reflex_asymmetry_p2'
                    elif idx[0] == 2:
                        paramName = '_pd_instr_reflex_asymmetry_p3'
                    elif idx[0] == 3:
                        paramName = '_pd_instr_reflex_asymmetry_p4'

                # background_ttheta
                elif group == 'background_ttheta':
                    loopName = '_pd_background'
                    paramName = '_2theta'
                    rowIndex = idx[0]
                    value = np.rad2deg(value)

                # background_intensity
                elif group == 'background_intensity':
                    loopName = '_pd_background'
                    paramName = '_intensity'
                    rowIndex = idx[0]

                # phase_scale
                elif group == 'phase_scale':
                    loopName = '_phase'
                    paramName = '_scale'
                    rowIndex = idx[0]

                value = float(value)  # convert float64 to float (needed for QML access)
                error = float(error)  # convert float64 to float (needed for QML access)
                blockIndex = [block['name']['value'] for block in self._dataBlocksNoMeas].index(blockName)

                if loopName is None:
                    self.editDataBlockMainParam(blockIndex, paramName, 'value', value)
                    self.editDataBlockMainParam(blockIndex, paramName, 'error', error)
                else:
                    self.editDataBlockLoopParam(blockIndex, loopName, paramName, rowIndex, 'value', value)
                    self.editDataBlockLoopParam(blockIndex, loopName, paramName, rowIndex, 'error', error)

    def editDataBlockByCryspyDictParams(self, params):
        for param in params:
            block, group, idx = Data.strToCryspyDictParamPath(param)

            # pd (powder diffraction) block
            if block.startswith('pd_'):
                blockName = block[3:]
                loopName = None
                paramName = None
                rowIndex = None
                value = self._proxy.data._cryspyDict[block][group][idx]

                # wavelength
                if group == 'wavelength':
                    paramName = '_diffrn_radiation_wavelength'

                # offset_ttheta
                elif group == 'offset_ttheta':
                    paramName = '_pd_meas_2theta_offset'
                    value = np.rad2deg(value)

                # resolution_parameters
                elif group == 'resolution_parameters':
                    if idx[0] == 0:
                        paramName = '_pd_instr_resolution_u'
                    elif idx[0] == 1:
                        paramName = '_pd_instr_resolution_v'
                    elif idx[0] == 2:
                        paramName = '_pd_instr_resolution_w'
                    elif idx[0] == 3:
                        paramName = '_pd_instr_resolution_x'
                    elif idx[0] == 4:
                        paramName = '_pd_instr_resolution_y'
                    elif idx[0] == 5:
                        paramName = '_pd_instr_resolution_z'

                # asymmetry_parameters
                elif group == 'asymmetry_parameters':
                    if idx[0] == 0:
                        paramName = '_pd_instr_reflex_asymmetry_p1'
                    elif idx[0] == 1:
                        paramName = '_pd_instr_reflex_asymmetry_p2'
                    elif idx[0] == 2:
                        paramName = '_pd_instr_reflex_asymmetry_p3'
                    elif idx[0] == 3:
                        paramName = '_pd_instr_reflex_asymmetry_p4'

                # background_ttheta
                elif group == 'background_ttheta':
                    loopName = '_pd_background'
                    paramName = '_2theta'
                    rowIndex = idx[0]
                    value = np.rad2deg(value)

                # background_intensity
                elif group == 'background_intensity':
                    loopName = '_pd_background'
                    paramName = '_intensity'
                    rowIndex = idx[0]

                # phase_scale
                elif group == 'phase_scale':
                    loopName = '_phase'
                    paramName = '_scale'
                    rowIndex = idx[0]

                value = float(value)  # convert float64 to float (needed for QML access)
                blockIndex = [block['name']['value'] for block in self._dataBlocksNoMeas].index(blockName)

                if loopName is None:
                    self.editDataBlockMainParam(blockIndex, paramName, 'value', value)
                else:
                    self.editDataBlockLoopParam(blockIndex, loopName, paramName, rowIndex, 'value', value)

    def runCryspyCalculations(self):
        result = rhochi_calc_chi_sq_by_dictionary(
            self._proxy.data._cryspyDict,
            dict_in_out=self._proxy.data._cryspyInOutDict,
            flag_use_precalculated_data=False,
            flag_calc_analytical_derivatives=False)

        console.debug(IO.formatMsg('sub', 'Cryspy calculations', 'finished'))

        chiSq = result[0]
        self._proxy.fitting._pointsCount = result[1]
        self._proxy.fitting._freeParamsCount = len(result[4])
        self._proxy.fitting.chiSq = chiSq / (self._proxy.fitting._pointsCount - self._proxy.fitting._freeParamsCount)

        gofLastIter = self._proxy.fitting.chiSq  # NEED FIX
        if self._proxy.fitting.chiSqStart is None:
            self._proxy.status.goodnessOfFit = f'{gofLastIter:0.2f}'                           # NEED move to connection
        else:
            gofStart = self._proxy.fitting.chiSqStart # NEED FIX
            self._proxy.status.goodnessOfFit = f'{gofStart:0.2f} → {gofLastIter:0.2f}'  # NEED move to connection
        if not self._proxy.fitting._freezeChiSqStart:
            self._proxy.fitting.chiSqStart = self._proxy.fitting.chiSq

    def setMeasuredArraysForSingleExperiment(self, idx):
        ed_name = self._proxy.experiment.dataBlocksNoMeas[idx]['name']['value']
        cryspy_block_name = f'pd_{ed_name}'
        cryspyInOutDict = self._proxy.data._cryspyInOutDict

        # X data
        x_array = cryspyInOutDict[cryspy_block_name]['ttheta']
        x_array = np.rad2deg(x_array)
        self.setXArray(x_array, idx)

        # Measured Y data
        y_meas_array = cryspyInOutDict[cryspy_block_name]['signal_exp'][0]
        self.setYMeasArray(y_meas_array, idx)

        # Standard deviation of the measured Y data
        sy_meas_array = cryspyInOutDict[cryspy_block_name]['signal_exp'][1]
        self.setSYMeasArray(sy_meas_array, idx)

    def setCalculatedArraysForSingleExperiment(self, idx):
        ed_name = self._proxy.experiment.dataBlocksNoMeas[idx]['name']['value']
        cryspy_block_name = f'pd_{ed_name}'
        cryspyInOutDict = self._proxy.data._cryspyInOutDict

        # Background Y data # NED FIX: use calculatedYBkgArray()
        y_bkg_array = cryspyInOutDict[cryspy_block_name]['signal_background']
        self.setYBkgArray(y_bkg_array, idx)

        # Total calculated Y data (sum of all phases up and down polarisation plus background)
        y_calc_total_array = cryspyInOutDict[cryspy_block_name]['signal_plus'] + \
                             cryspyInOutDict[cryspy_block_name]['signal_minus'] + \
                             y_bkg_array
        self.setYCalcTotalArray(y_calc_total_array, idx)

        # Residual (Ymeas -Ycalc)
        y_meas_array = self._yMeasArrays[idx]
        y_resid_array = y_meas_array - y_calc_total_array
        self.setYResidArray(y_resid_array, idx)

        # Bragg peaks data
        #cryspyInOutDict[cryspy_name]['dict_in_out_co2sio4']['index_hkl'] # [0] - h array, [1] - k array, [2] - l array
        #cryspyInOutDict[cryspy_name]['dict_in_out_co2sio4']['ttheta_hkl'] # need rad2deg
        modelNames = [key[12:] for key in cryspyInOutDict[cryspy_block_name].keys() if 'dict_in_out' in key]
        xBraggDict = {}
        for modelName in modelNames:
            x_bragg_array = cryspyInOutDict[cryspy_block_name][f'dict_in_out_{modelName}']['ttheta_hkl']
            x_bragg_array = np.rad2deg(x_bragg_array)
            xBraggDict[modelName] = x_bragg_array
        self.setXBraggDict(xBraggDict, idx)

    def setChartRangesForSingleExperiment(self, idx):
        x_array = self._xArrays[idx]
        y_meas_array = self._yMeasArrays[idx]
        x_min = float(x_array.min())
        x_max = float(x_array.max())
        y_min = float(y_meas_array.min())
        y_max = float(y_meas_array.max())
        y_range = y_max - y_min
        y_extra = y_range * 0.1
        y_min -= y_extra
        y_max += y_extra
        ranges = {'xMin':x_min, 'xMax':x_max, 'yMin':y_min, 'yMax':y_max}
        self.setChartRanges(ranges, idx)

    def replaceArrays(self):
        for idx in range(len(self._dataBlocksMeasOnly)):
            self.setCalculatedArraysForSingleExperiment(idx)

    def addArraysAndChartRanges(self):
        for idx in range(len(self._xArrays), len(self._dataBlocksMeasOnly)):
            self.setMeasuredArraysForSingleExperiment(idx)
            self.setCalculatedArraysForSingleExperiment(idx)
            self.setChartRangesForSingleExperiment(idx)

    def setXArray(self, xArray, idx):
        try:
            self._xArrays[idx] = xArray
            console.debug(IO.formatMsg('sub', 'X', f'experiment no. {idx + 1}', 'in intern dataset', 'replaced'))
        except IndexError:
            self._xArrays.append(xArray)
            console.debug(IO.formatMsg('sub', 'X', f'experiment no. {len(self._xArrays)}', 'to intern dataset', 'added'))

    def setYMeasArray(self, yMeasArray, idx):
        try:
            self._yMeasArrays[idx] = yMeasArray
            console.debug(IO.formatMsg('sub', 'Y-meas', f'experiment no. {idx + 1}', 'in intern dataset', 'replaced'))
        except IndexError:
            self._yMeasArrays.append(yMeasArray)
            console.debug(IO.formatMsg('sub', 'Y-meas', f'experiment no. {len(self._yMeasArrays)}', 'to intern dataset', 'added'))
        self.yMeasArraysChanged.emit()

    def setSYMeasArray(self, syMeasArray, idx):
        try:
            self._syMeasArrays[idx] = syMeasArray
            console.debug(IO.formatMsg('sub', 'sY-meas', f'experiment no. {idx + 1}', 'in intern dataset', 'replaced'))
        except IndexError:
            self._syMeasArrays.append(syMeasArray)
            console.debug(IO.formatMsg('sub', 'sY-meas', f'experiment no. {len(self._syMeasArrays)}', 'to intern dataset', 'added'))

    def setYBkgArray(self, yBkgArray, idx):
        try:
            self._yBkgArrays[idx] = yBkgArray
            console.debug(IO.formatMsg('sub', 'Y-bkg (inter)', f'experiment no. {idx + 1}', 'in intern dataset', 'replaced'))
        except IndexError:
            self._yBkgArrays.append(yBkgArray)
            console.debug(IO.formatMsg('sub', 'Y-bkg (inter)', f'experiment no. {len(self._yBkgArrays)}', 'to intern dataset', 'added'))
        self.yBkgArraysChanged.emit()

    def setYCalcTotalArray(self, yCalcTotalArray, idx):
        try:
            self._yCalcTotalArrays[idx] = yCalcTotalArray
            console.debug(IO.formatMsg('sub', 'Y-calc (total)', f'experiment no. {idx + 1}', 'in intern dataset', 'replaced'))
        except IndexError:
            self._yCalcTotalArrays.append(yCalcTotalArray)
            console.debug(IO.formatMsg('sub', 'Y-calc (total)', f'experiment no. {len(self._yCalcTotalArrays)}', 'to intern dataset', 'added'))
        self.yCalcTotalArraysChanged.emit()

    def setYResidArray(self, yResidArray, idx):
        try:
            self._yResidArrays[idx] = yResidArray
            console.debug(IO.formatMsg('sub', 'Y-resid (meas-calc)', f'experiment no. {idx + 1}', 'in intern dataset', 'replaced'))
        except IndexError:
            self._yResidArrays.append(yResidArray)
            console.debug(IO.formatMsg('sub', 'Y-resid (meas-calc)', f'experiment no. {len(self._yResidArrays)}', 'to intern dataset', 'added'))
        self.yResidArraysChanged.emit()

    def setXBraggDict(self, xBraggDict, idx):
        try:
            self._xBraggDicts[idx] = xBraggDict
            console.debug(IO.formatMsg('sub', 'X-Bragg (peaks)', f'experiment no. {idx + 1}', 'in intern dataset', 'replaced'))
        except IndexError:
            self._xBraggDicts.append(xBraggDict)
            console.debug(IO.formatMsg('sub', 'X-Bragg (peaks)', f'experiment no. {len(self._xBraggDicts)}', 'to intern dataset', 'added'))
        self.xBraggDictsChanged.emit()

    def setChartRanges(self, ranges, idx):
        try:
            self._chartRanges[idx] = ranges
            console.debug(IO.formatMsg('sub', 'Chart ranges', f'experiment no. {idx + 1}', 'in intern dataset', 'replaced'))
        except IndexError:
            self._chartRanges.append(ranges)
            console.debug(IO.formatMsg('sub', 'Chart ranges', f'experiment no. {len(self._chartRanges)}', 'to intern dataset', 'added'))
        self.chartRangesChanged.emit()

    def setDataBlocksCifNoMeas(self):
        self._dataBlocksCifNoMeas = [CryspyParser.dataBlockToCif(block) for block in self._dataBlocksNoMeas]
        console.debug(IO.formatMsg('sub', f'{len(self._dataBlocksCifNoMeas)} experiment(s)', 'without meas data', 'to CIF string', 'converted'))
        self.dataBlocksCifNoMeasChanged.emit()

    def setDataBlocksCifMeasOnly(self):
        self._dataBlocksCifMeasOnly = [CryspyParser.dataBlockToCif(block, includeBlockName=False) for block in self._dataBlocksMeasOnly]
        console.debug(IO.formatMsg('sub', f'{len(self._dataBlocksCifMeasOnly)} experiment(s)', 'meas data only', 'to CIF string', 'converted'))
        self.dataBlocksCifMeasOnlyChanged.emit()

    def setDataBlocksCif(self):
        self.setDataBlocksCifNoMeas()
        self.setDataBlocksCifMeasOnly()
        cifMeasOnlyReduced =  [block.split('\n')[:10] + ['...'] + block.split('\n')[-6:] for block in self._dataBlocksCifMeasOnly]
        cifMeasOnlyReduced = ['\n'.join(block) for block in cifMeasOnlyReduced]
        cifMeasOnlyReduced = [f'\n{block}' for block in cifMeasOnlyReduced]
        cifMeasOnlyReduced = [block.rstrip() for block in cifMeasOnlyReduced]
        self._dataBlocksCif = [[noMeas, measOnlyReduced] for (noMeas, measOnlyReduced) in zip(self._dataBlocksCifNoMeas, cifMeasOnlyReduced)]
        console.debug(IO.formatMsg('sub', f'{len(self._dataBlocksCif)} experiment(s)', 'simplified meas data', 'to CIF string', 'converted'))
        self.dataBlocksCifChanged.emit()
