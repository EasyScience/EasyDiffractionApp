# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import copy
import re
import random
import numpy as np
from PySide6.QtCore import QObject, Signal, Slot, Property, QThreadPool
from PySide6.QtCore import QFile, QTextStream, QIODevice
from PySide6.QtQml import QJSValue

from EasyApp.Logic.Logging import console
from Logic.Helpers import IO
from Logic.Calculators import CryspyParser
from Logic.Tables import PERIODIC_TABLE
from Logic.Data import Data

try:
    import cryspy
    from cryspy.H_functions_global.function_1_cryspy_objects import \
        str_to_globaln
    from cryspy.A_functions_base.database import DATABASE
    from cryspy.A_functions_base.function_2_space_group import \
        REFERENCE_TABLE_IT_COORDINATE_SYSTEM_CODE_NAME_HM_EXTENDED, \
        REFERENCE_TABLE_IT_NUMBER_NAME_HM_FULL, \
        ACCESIBLE_NAME_HM_SHORT
    from cryspy.procedure_rhochi.rhochi_by_dictionary import \
        rhochi_calc_chi_sq_by_dictionary
    console.debug('CrysPy module imported')
except ImportError:
    console.error('No CrysPy module found')


_DEFAULT_CIF_BLOCK = """data_default

_space_group_name_H-M_alt "P b n m"

_cell_length_a 10
_cell_length_b 6
_cell_length_c 5
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_adp_type
_atom_site_B_iso_or_equiv
O O 0 0 0 1 Biso 0
"""


class Model(QObject):
    definedChanged = Signal()
    currentIndexChanged = Signal()
    dataBlocksChanged = Signal()
    dataBlocksCifChanged = Signal()

    structViewAtomsModelChanged = Signal()
    structViewCellModelChanged = Signal()
    structViewAxesModelChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._defined = False
        self._currentIndex = -1
        self._dataBlocks = []
        self._dataBlocksCif = []

        self._structureViewUpdater = StructureViewUpdater(self._proxy)

        self._structViewAtomsModel = []
        self._structViewCellModel = []
        self._structViewAxesModel = []

        self._spaceGroupDict = {}
        self._spaceGroupNames = self.createSpaceGroupNames()
        self._isotopesNames = self.createIsotopesNames()

    # QML accessible properties

    @Property('QVariant', constant=True)
    def spaceGroupNames(self):
        return self._spaceGroupNames

    @Property('QVariant', constant=True)
    def isotopesNames(self):
        return self._isotopesNames

    @Property(bool, notify=definedChanged)
    def defined(self):
        return self._defined
    
    @defined.setter
    def defined(self, newValue):
        if self._defined == newValue:
            return
        self._defined = newValue
        console.debug(IO.formatMsg('main', f'Model defined: {newValue}'))

        self.definedChanged.emit()

    @Property(int, notify=currentIndexChanged)
    def currentIndex(self):
        return self._currentIndex

    @currentIndex.setter
    def currentIndex(self, newValue):
        if self._currentIndex == newValue:
            return
        self._currentIndex = newValue
        console.debug(f"Current model index: {newValue}")
        self.currentIndexChanged.emit()

    @Property('QVariant', notify=dataBlocksChanged)
    def dataBlocks(self):
        return self._dataBlocks

    @Property('QVariant', notify=dataBlocksCifChanged)
    def dataBlocksCif(self):
        return self._dataBlocksCif

    @Property('QVariant', notify=structViewAtomsModelChanged)
    def structViewAtomsModel(self):
        return self._structViewAtomsModel

    @Property('QVariant', notify=structViewCellModelChanged)
    def structViewCellModel(self):
        return self._structViewCellModel

    @Property('QVariant', notify=structViewAxesModelChanged)
    def structViewAxesModel(self):
        return self._structViewAxesModel

    # QML accessible methods

    @Slot(str, str, result=str)
    def atomData(self, typeSymbol, key):
        if typeSymbol == '':
            return ''
        typeSymbol = re.sub(r'[0-9]', '', typeSymbol)  # '162Dy' -> 'Dy'
        return PERIODIC_TABLE[typeSymbol][key]

    @Slot()
    def addDefaultModel(self):
        console.debug("Adding default model(s)")
        self.loadModelsFromEdCif(_DEFAULT_CIF_BLOCK)

    @Slot('QVariant')
    def loadModelsFromResources(self, fpaths):
        if type(fpaths) == QJSValue:
            fpaths = fpaths.toVariant()
        for fpath in fpaths:
            console.debug(f"Loading model(s) from: {fpath}")
            file = QFile(fpath)
            if not file.open(QIODevice.ReadOnly | QIODevice.Text):
                console.error('Not found in resources')
                return
            stream = QTextStream(file)
            edCif = stream.readAll()
            self.loadModelsFromEdCif(edCif)

    @Slot('QVariant')
    def loadModelsFromFiles(self, fpaths):
        if type(fpaths) == QJSValue:
            fpaths = fpaths.toVariant()
        for fpath in fpaths:
            fpath = fpath.toLocalFile()
            fpath = IO.generalizePath(fpath)
            console.debug(f"Loading model(s) from: {fpath}")
            with open(fpath, 'r') as file:
                edCif = file.read()
            self.loadModelsFromEdCif(edCif)

    @Slot(str)
    def loadModelsFromEdCif(self, edCif):
        cryspyObj = self._proxy.data._cryspyObj
        cryspyCif = CryspyParser.edCifToCryspyCif(edCif)
        cryspyModelsObj = str_to_globaln(cryspyCif)

        modelsCountBefore = len(self.cryspyObjCrystals())
        cryspyObj.add_items(cryspyModelsObj.items)
        modelsCountAfter = len(self.cryspyObjCrystals())
        success = modelsCountAfter - modelsCountBefore

        if success:
            cryspyModelsDict = cryspyModelsObj.get_dictionary()
            edModels = CryspyParser.cryspyObjAndDictToEdModels(cryspyModelsObj, cryspyModelsDict)

            self._proxy.data._cryspyDict.update(cryspyModelsDict)
            self._dataBlocks += edModels

            self._currentIndex = len(self.dataBlocks) - 1
            if not self.defined:
                self.defined = bool(len(self.dataBlocks))

            console.debug(IO.formatMsg('sub', f'{len(edModels)} model(s)', '', 'to intern dataset', 'added'))

            self.dataBlocksChanged.emit()

        else:
            console.debug(IO.formatMsg('sub', 'No model(s)', '', 'to intern dataset', 'added'))

    @Slot(str)
    def replaceModel(self, edCif=''):
        console.debug("Cryspy obj and dict need to be replaced")

        currentDataBlock = self.dataBlocks[self.currentIndex]
        currentModelName = currentDataBlock['name']['value']

        cryspyObjBlockNames = [item.data_name for item in self._proxy.data._cryspyObj.items]
        cryspyObjBlockIdx = cryspyObjBlockNames.index(currentModelName)

        cryspyDictBlockName = f'crystal_{currentModelName}'

        if not edCif:
            edCif = CryspyParser.dataBlockToCif(currentDataBlock)
        cryspyCif = CryspyParser.edCifToCryspyCif(edCif)
        cryspyModelsObj = str_to_globaln(cryspyCif)
        cryspyModelsDict = cryspyModelsObj.get_dictionary()
        edModels = CryspyParser.cryspyObjAndDictToEdModels(cryspyModelsObj, cryspyModelsDict)

        self._proxy.data._cryspyObj.items[cryspyObjBlockIdx] = cryspyModelsObj.items[0]
        self._proxy.data._cryspyDict[cryspyDictBlockName] = cryspyModelsDict[cryspyDictBlockName]
        self._dataBlocks[self.currentIndex] = edModels[0]

        console.debug(f"Model data block '{currentModelName}' (no. {self.currentIndex + 1}) has been replaced")
        self.dataBlocksChanged.emit()

    @Slot(int)
    def removeModel(self, index):
        console.debug(f"Removing model no. {index + 1}")

        currentDataBlock = self.dataBlocks[index]
        currentModelName = currentDataBlock['name']['value']

        cryspyObjBlockNames = [item.data_name for item in self._proxy.data._cryspyObj.items]
        cryspyObjBlockIdx = cryspyObjBlockNames.index(currentModelName)

        cryspyDictBlockName = f'crystal_{currentModelName}'

        del self._proxy.data._cryspyObj.items[cryspyObjBlockIdx]
        del self._proxy.data._cryspyDict[cryspyDictBlockName]
        del self._dataBlocks[index]

        self.defined = bool(len(self.dataBlocks))

        self.dataBlocksChanged.emit()

        console.debug(f"Model no. {index + 1} has been removed")

    @Slot()
    def resetAll(self):
        self.defined = False
        self._currentIndex = -1
        self._dataBlocks = []
        self._dataBlocksCif = []
        #self.dataBlocksChanged.emit()
        console.debug("All models removed")

    @Slot(int, str, str, 'QVariant')
    def setMainParamWithFullUpdate(self, blockIndex, paramName, field, value):
        changedIntern = self.editDataBlockMainParam(blockIndex, paramName, field, value)
        if not changedIntern:
            return
        self.replaceModel()

    @Slot(int, str, str, 'QVariant')
    def setMainParam(self, blockIndex, paramName, field, value):
        changedIntern = self.editDataBlockMainParam(blockIndex, paramName, field, value)
        changedCryspy = self.editCryspyDictByMainParam(blockIndex, paramName, field, value)
        if changedIntern and changedCryspy:
            self.dataBlocksChanged.emit()

    @Slot(int, str, str, int, str, 'QVariant')
    def setLoopParamWithFullUpdate(self, blockIndex, loopName, paramName, rowIndex, field, value):
        changedIntern = self.editDataBlockLoopParam(blockIndex, loopName, paramName, rowIndex, field, value)
        if not changedIntern:
            return
        self.replaceModel()

    @Slot(int, str, str, int, str, 'QVariant')
    def setLoopParam(self, blockIndex, loopName, paramName, rowIndex, field, value):
        changedIntern = self.editDataBlockLoopParam(blockIndex, loopName, paramName, rowIndex, field, value)
        changedCryspy = self.editCryspyDictByLoopParam(blockIndex, loopName, paramName, rowIndex, field, value)
        if changedIntern and changedCryspy:
            self.dataBlocksChanged.emit()

    @Slot(str, int)
    def removeLoopRow(self, loopName, rowIndex):
        self.removeDataBlockLoopRow(loopName, rowIndex)
        self.replaceModel()

    @Slot(str)
    def appendLoopRow(self, loopName):
        self.appendDataBlockLoopRow(loopName)
        self.replaceModel()

    @Slot(str, int)
    def duplicateLoopRow(self, loopName, idx):
        self.duplicateDataBlockLoopRow(loopName, idx)
        self.replaceModel()

    # Private methods

    def cryspyObjCrystals(self):
        cryspyObj = self._proxy.data._cryspyObj
        cryspyModelType = cryspy.E_data_classes.cl_1_crystal.Crystal
        models = [block for block in cryspyObj.items if type(block) == cryspyModelType]
        return models

    def createSpaceGroupNames(self):
        namesShort = ACCESIBLE_NAME_HM_SHORT
        namesFull = tuple((name[1] for name in REFERENCE_TABLE_IT_NUMBER_NAME_HM_FULL))
        namesExtended = tuple((name[2] for name in REFERENCE_TABLE_IT_COORDINATE_SYSTEM_CODE_NAME_HM_EXTENDED))
        return list(set(namesShort + namesFull + namesExtended))

    def createIsotopesNames(self):
        return [isotope[1] for isotope in list(DATABASE['Isotopes'].keys())]

    def removeDataBlockLoopRow(self, loopName, rowIndex):
        block = 'model'
        blockIndex = self._currentIndex
        del self._dataBlocks[blockIndex]['loops'][loopName][rowIndex]

        console.debug(IO.formatMsg('sub', 'Intern dict', 'removed', f'{block}[{blockIndex}].{loopName}[{rowIndex}]'))

    def appendDataBlockLoopRow(self, loopName):
        block = 'model'
        blockIndex = self._currentIndex

        lastAtom = self._dataBlocks[blockIndex]['loops'][loopName][-1]

        newAtom = copy.deepcopy(lastAtom)
        newAtom['_label']['value'] = random.choice(self.isotopesNames)
        newAtom['_type_symbol']['value'] = newAtom['_label']['value']
        newAtom['_fract_x']['value'] = random.uniform(0, 1)
        newAtom['_fract_y']['value'] = random.uniform(0, 1)
        newAtom['_fract_z']['value'] = random.uniform(0, 1)
        newAtom['_occupancy']['value'] = 1
        newAtom['_B_iso_or_equiv']['value'] = 0

        self._dataBlocks[blockIndex]['loops'][loopName].append(newAtom)
        atomsCount = len(self._dataBlocks[blockIndex]['loops'][loopName])

        console.debug(IO.formatMsg('sub', 'Intern dict', 'added', f'{block}[{blockIndex}].{loopName}[{atomsCount}]'))

    def duplicateDataBlockLoopRow(self, loopName, idx):
        block = 'model'
        blockIndex = self._currentIndex

        lastAtom = self._dataBlocks[blockIndex]['loops'][loopName][idx]

        self._dataBlocks[blockIndex]['loops'][loopName].append(lastAtom)
        atomsCount = len(self._dataBlocks[blockIndex]['loops'][loopName])

        console.debug(IO.formatMsg('sub', 'Intern dict', 'added', f'{block}[{blockIndex}].{loopName}[{atomsCount}]'))

    def editDataBlockMainParam(self, blockIndex, paramName, field, value):
        blockType = 'model'
        oldValue = self._dataBlocks[blockIndex]['params'][paramName][field]
        if oldValue == value:
            return False
        self._dataBlocks[blockIndex]['params'][paramName][field] = value
        if type(value) == float:
            console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value:.6f}', f'{blockType}[{blockIndex}].{paramName}.{field}'))
        else:
            console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value}', f'{blockType}[{blockIndex}].{paramName}.{field}'))
        return True

    def editDataBlockLoopParam(self, blockIndex, loopName, paramName, rowIndex, field, value):
        block = 'model'
        oldValue = self._dataBlocks[blockIndex]['loops'][loopName][rowIndex][paramName][field]
        if oldValue == value:
            return False
        self._dataBlocks[blockIndex]['loops'][loopName][rowIndex][paramName][field] = value
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
        blockName = self._dataBlocks[blockIndex]['name']['value']
        path = ['','','']
        path[0] = f"crystal_{blockName}"

        # _cell
        if paramName == '_cell_length_a':
            path[1] = 'unit_cell_parameters'
            path[2] = 0
        elif paramName == '_cell_length_b':
            path[1] = 'unit_cell_parameters'
            path[2] = 1
        elif paramName == '_cell_length_c':
            path[1] = 'unit_cell_parameters'
            path[2] = 2
        elif paramName == '_cell_angle_alpha':
            path[1] = 'unit_cell_parameters'
            path[2] = 3
            value = np.deg2rad(value)
        elif paramName == '_cell_angle_beta':
            path[1] = 'unit_cell_parameters'
            path[2] = 4
            value = np.deg2rad(value)
        elif paramName == '_cell_angle_gamma':
            path[1] = 'unit_cell_parameters'
            path[2] = 5
            value = np.deg2rad(value)

        # undefined
        else:
            console.error(f"Undefined parameter name '{paramName}'")

        return path, value

    def cryspyDictPathByLoopParam(self, blockIndex, loopName, paramName, rowIndex, value):
        blockName = self._dataBlocks[blockIndex]['name']['value']
        path = ['','','']
        path[0] = f"crystal_{blockName}"

        # _atom_site
        if loopName == '_atom_site':
            if paramName == '_fract_x':
                path[1] = 'atom_fract_xyz'
                path[2] = (0, rowIndex)
            elif paramName == '_fract_y':
                path[1] = 'atom_fract_xyz'
                path[2] = (1, rowIndex)
            elif paramName == '_fract_z':
                path[1] = 'atom_fract_xyz'
                path[2] = (2, rowIndex)
            elif paramName == '_occupancy':
                path[1] = 'atom_occupancy'
                path[2] = rowIndex
            elif paramName == '_B_iso_or_equiv':
                path[1] = 'atom_b_iso'
                path[2] = rowIndex

        return path, value

    def paramValueByFieldAndCrypyParamPath(self, field, path):  # NEED FIX: code duplicate of editDataBlockByLmfitParams
        block, group, idx = path

        # crystal block
        if block.startswith('crystal_'):
            blockName = block[8:]
            loopName = None
            paramName = None
            rowIndex = None

            # unit_cell_parameters
            if group == 'unit_cell_parameters':
                if idx[0] == 0:
                    paramName = '_cell_length_a'
                elif idx[0] == 1:
                    paramName = '_cell_length_b'
                elif idx[0] == 2:
                    paramName = '_cell_length_c'
                elif idx[0] == 3:
                    paramName = '_cell_angle_alpha'
                elif idx[0] == 4:
                    paramName = '_cell_angle_beta'
                elif idx[0] == 5:
                    paramName = '_cell_angle_gamma'

            # atom_fract_xyz
            elif group == 'atom_fract_xyz':
                loopName = '_atom_site'
                rowIndex = idx[1]
                if idx[0] == 0:
                    paramName = '_fract_x'
                elif idx[0] == 1:
                    paramName = '_fract_y'
                elif idx[0] == 2:
                    paramName = '_fract_z'

            # atom_occupancy
            elif group == 'atom_occupancy':
                loopName = '_atom_site'
                rowIndex = idx[0]
                paramName = '_occupancy'

            # b_iso_or_equiv
            elif group == 'atom_b_iso':
                loopName = '_atom_site'
                rowIndex = idx[0]
                paramName = '_B_iso_or_equiv'

            blockIndex = [block['name']['value'] for block in self._dataBlocks].index(blockName)

            if loopName is None:
                return self.dataBlocks[blockIndex]['params'][paramName][field]
            else:
                return self.dataBlocks[blockIndex]['loops'][loopName][rowIndex][paramName][field]

        return None

    def editDataBlockByLmfitParams(self, params):
        for param in params.values():
            block, group, idx = Data.strToCryspyDictParamPath(param.name)

            # crystal block
            if block.startswith('crystal_'):
                blockName = block[8:]
                loopName = None
                paramName = None
                rowIndex = None
                value = param.value
                error = 0
                if param.stderr is not None:
                    error = param.stderr

                # unit_cell_parameters
                if group == 'unit_cell_parameters':
                    if idx[0] == 0:
                        paramName = '_cell_length_a'
                    elif idx[0] == 1:
                        paramName = '_cell_length_b'
                    elif idx[0] == 2:
                        paramName = '_cell_length_c'
                    elif idx[0] == 3:
                        paramName = '_cell_angle_alpha'
                        value = np.rad2deg(value)
                    elif idx[0] == 4:
                        paramName = '_cell_angle_beta'
                        value = np.rad2deg(value)
                    elif idx[0] == 5:
                        paramName = '_cell_angle_gamma'
                        value = np.rad2deg(value)

                # atom_fract_xyz
                elif group == 'atom_fract_xyz':
                    loopName = '_atom_site'
                    rowIndex = idx[1]
                    if idx[0] == 0:
                        paramName = '_fract_x'
                    elif idx[0] == 1:
                        paramName = '_fract_y'
                    elif idx[0] == 2:
                        paramName = '_fract_z'

                # atom_occupancy
                elif group == 'atom_occupancy':
                    loopName = '_atom_site'
                    rowIndex = idx[0]
                    paramName = '_occupancy'

                # b_iso_or_equiv
                elif group == 'atom_b_iso':
                    loopName = '_atom_site'
                    rowIndex = idx[0]
                    paramName = '_B_iso_or_equiv'

                value = float(value)  # convert float64 to float (needed for QML access)
                error = float(error)  # convert float64 to float (needed for QML access)
                blockIndex = [block['name']['value'] for block in self._dataBlocks].index(blockName)

                if loopName is None:
                    self.editDataBlockMainParam(blockIndex, paramName, 'value', value)
                    self.editDataBlockMainParam(blockIndex, paramName, 'error', error)
                else:
                    self.editDataBlockLoopParam(blockIndex, loopName, paramName, rowIndex, 'value', value)
                    self.editDataBlockLoopParam(blockIndex, loopName, paramName, rowIndex, 'error', error)

    def editDataBlockByCryspyDictParams(self, params):
        for param in params:
            block, group, idx = Data.strToCryspyDictParamPath(param)

            # crystal block
            if block.startswith('crystal_'):
                blockName = block[8:]
                loopName = None
                paramName = None
                rowIndex = None
                value = self._proxy.data._cryspyDict[block][group][idx]

                # unit_cell_parameters
                if group == 'unit_cell_parameters':
                    if idx[0] == 0:
                        paramName = '_cell_length_a'
                    elif idx[0] == 1:
                        paramName = '_cell_length_b'
                    elif idx[0] == 2:
                        paramName = '_cell_length_c'
                    elif idx[0] == 3:
                        paramName = '_cell_angle_alpha'
                        value = np.rad2deg(value)
                    elif idx[0] == 4:
                        paramName = '_cell_angle_beta'
                        value = np.rad2deg(value)
                    elif idx[0] == 5:
                        paramName = '_cell_angle_gamma'
                        value = np.rad2deg(value)

                # atom_fract_xyz
                elif group == 'atom_fract_xyz':
                    loopName = '_atom_site'
                    rowIndex = idx[1]
                    if idx[0] == 0:
                        paramName = '_fract_x'
                    elif idx[0] == 1:
                        paramName = '_fract_y'
                    elif idx[0] == 2:
                        paramName = '_fract_z'

                # atom_occupancy
                elif group == 'atom_occupancy':
                    loopName = '_atom_site'
                    rowIndex = idx[0]
                    paramName = '_occupancy'

                # b_iso_or_equiv
                elif group == 'atom_b_iso':
                    loopName = '_atom_site'
                    rowIndex = idx[0]
                    paramName = '_B_iso_or_equiv'

                value = float(value)  # convert float64 to float (needed for QML access)
                blockIndex = [block['name']['value'] for block in self._dataBlocks].index(blockName)

                if loopName is None:
                    self.editDataBlockMainParam(blockIndex, paramName, 'value', value)
                else:
                    self.editDataBlockLoopParam(blockIndex, loopName, paramName, rowIndex, 'value', value)

    def setDataBlocksCif(self):
        self._dataBlocksCif = [[CryspyParser.dataBlockToCif(block)] for block in self._dataBlocks]
        console.debug(IO.formatMsg('sub', f'{len(self._dataBlocksCif)} model(s)', '', 'to CIF string', 'converted'))
        self.dataBlocksCifChanged.emit()

    def updateCurrentModelStructView(self):
        self.setCurrentModelStructViewAtomsModel()
        #self.setCurrentModelStructViewCellModel()
        #self.setCurrentModelStructViewAxesModel()

    def setCurrentModelStructViewCellModel(self):
        params = self._dataBlocks[self._currentIndex]['params']
        a = params['_cell_length_a']['value']
        b = params['_cell_length_b']['value']
        c = params['_cell_length_c']['value']
        self._structViewCellModel = [
            # x
            { "x": 0,     "y":-0.5*b, "z":-0.5*c, "rotx": 0, "roty": 0,  "rotz":-90, "len": a },
            { "x": 0,     "y": 0.5*b, "z":-0.5*c, "rotx": 0, "roty": 0,  "rotz":-90, "len": a },
            { "x": 0,     "y":-0.5*b, "z": 0.5*c, "rotx": 0, "roty": 0,  "rotz":-90, "len": a },
            { "x": 0,     "y": 0.5*b, "z": 0.5*c, "rotx": 0, "roty": 0,  "rotz":-90, "len": a },
            # y
            { "x":-0.5*a, "y": 0,     "z":-0.5*c, "rotx": 0, "roty": 0,  "rotz": 0,  "len": b },
            { "x": 0.5*a, "y": 0,     "z":-0.5*c, "rotx": 0, "roty": 0,  "rotz": 0,  "len": b },
            { "x":-0.5*a, "y": 0,     "z": 0.5*c, "rotx": 0, "roty": 0,  "rotz": 0,  "len": b },
            { "x": 0.5*a, "y": 0,     "z": 0.5*c, "rotx": 0, "roty": 0,  "rotz": 0,  "len": b },
            # z
            { "x":-0.5*a, "y":-0.5*b, "z": 0,     "rotx": 0, "roty": 90, "rotz": 90, "len": c },
            { "x": 0.5*a, "y":-0.5*b, "z": 0,     "rotx": 0, "roty": 90, "rotz": 90, "len": c },
            { "x":-0.5*a, "y": 0.5*b, "z": 0,     "rotx": 0, "roty": 90, "rotz": 90, "len": c },
            { "x": 0.5*a, "y": 0.5*b, "z": 0,     "rotx": 0, "roty": 90, "rotz": 90, "len": c },
        ]
        console.debug(f"Structure view cell  for model no. {self._currentIndex + 1} has been set. Cell lengths: ({a}, {b}, {c})")
        self.structViewCellModelChanged.emit()

    def setCurrentModelStructViewAxesModel(self):
        params = self._dataBlocks[self._currentIndex]['params']
        a = params['_cell_length_a']['value']
        b = params['_cell_length_b']['value']
        c = params['_cell_length_c']['value']
        self._structViewAxesModel = [
            {"x": 0.5, "y": 0,   "z": 0,   "rotx": 0, "roty":  0, "rotz": -90, "len": a},
            {"x": 0,   "y": 0.5, "z": 0,   "rotx": 0, "roty":  0, "rotz":   0, "len": b},
            {"x": 0,   "y": 0,   "z": 0.5, "rotx": 0, "roty": 90, "rotz":  90, "len": c}
        ]
        console.debug(f"Structure view axes  for model no. {self._currentIndex + 1} has been set. Cell lengths: ({a}, {b}, {c})")
        self.structViewAxesModelChanged.emit()

    def setCurrentModelStructViewAtomsModel(self):
        structViewModel = set()
        currentModelIndex = self._proxy.model.currentIndex
        models = self.cryspyObjCrystals()
        spaceGroup = [sg for sg in models[currentModelIndex].items if type(sg) == cryspy.C_item_loop_classes.cl_2_space_group.SpaceGroup][0]
        atoms = self._dataBlocks[self._currentIndex]['loops']['_atom_site']
        # Add all atoms in the cell, including those in equivalent positions
        for atom in atoms:
            symbol = atom['_type_symbol']['value']
            xUnique = atom['_fract_x']['value']
            yUnique = atom['_fract_y']['value']
            zUnique = atom['_fract_z']['value']
            xArray, yArray, zArray, _ = spaceGroup.calc_xyz_mult(xUnique, yUnique, zUnique)
            for x, y, z in zip(xArray, yArray, zArray):
                structViewModel.add((
                    float(x),
                    float(y),
                    float(z),
                    self.atomData(symbol, 'covalentRadius'),
                    self.atomData(symbol, 'color')
                ))
        # Add those atoms, which have 0 in xyz to be translated into 1
        structViewModelCopy = copy.copy(structViewModel)
        for item in structViewModelCopy:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                structViewModel.add((1, 0, 0, item[3], item[4]))
                structViewModel.add((0, 1, 0, item[3], item[4]))
                structViewModel.add((0, 0, 1, item[3], item[4]))
                structViewModel.add((1, 1, 0, item[3], item[4]))
                structViewModel.add((1, 0, 1, item[3], item[4]))
                structViewModel.add((0, 1, 1, item[3], item[4]))
                structViewModel.add((1, 1, 1, item[3], item[4]))
            elif item[0] == 0 and item[1] == 0:
                structViewModel.add((1, 0, item[2], item[3], item[4]))
                structViewModel.add((0, 1, item[2], item[3], item[4]))
                structViewModel.add((1, 1, item[2], item[3], item[4]))
            elif item[0] == 0 and item[2] == 0:
                structViewModel.add((1, item[1], 0, item[3], item[4]))
                structViewModel.add((0, item[1], 1, item[3], item[4]))
                structViewModel.add((1, item[1], 1, item[3], item[4]))
            elif item[1] == 0 and item[2] == 0:
                structViewModel.add((item[0], 1, 0, item[3], item[4]))
                structViewModel.add((item[0], 0, 1, item[3], item[4]))
                structViewModel.add((item[0], 1, 1, item[3], item[4]))
            elif item[0] == 0:
                structViewModel.add((1, item[1], item[2], item[3], item[4]))
            elif item[1] == 0:
                structViewModel.add((item[0], 1, item[2], item[3], item[4]))
            elif item[2] == 0:
                structViewModel.add((item[0], item[1], 1, item[3], item[4]))
        # Create dict from set for GUI
        self._structViewAtomsModel = [{'x':x, 'y':y, 'z':z, 'diameter':diameter, 'color':color}
                                      for x, y, z, diameter, color in structViewModel]
        console.debug(IO.formatMsg('sub', f'{len(atoms)} atom(s)', f'model no. {self._currentIndex + 1}', 'for structure view', 'defined'))
        self.structViewAtomsModelChanged.emit()


class StructureViewWorker(QObject):
    finished = Signal()

    def __init__(self, proxy):
        super().__init__()
        self._proxy = proxy

    def run(self):
        self._proxy.model.updateCurrentModelStructView()
        self.finished.emit()


class StructureViewUpdater(QObject):
    finished = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._threadpool = QThreadPool.globalInstance()
        self._worker = StructureViewWorker(self._proxy)

        self._worker.finished.connect(self.finished)

    def update(self):
        self._threadpool.start(self._worker.run)
        console.debug(IO.formatMsg('main', '---------------'))
