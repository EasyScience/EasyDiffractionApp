# SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
# SPDX-License-Identifier: BSD-3-Clause
# © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

import os
import time
from pycifstar.data import Data as PycifstarData
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl
from PySide6.QtCore import QFile, QTextStream, QIODevice

from EasyApp.Logic.Logging import console
from Logic.Helpers import IO
from Logic.Calculators import Parameter, CryspyParser


_EMPTY_DATA = {
    'name': '',
    'params': {},
    'loops': {}
}

_EMPTY_DESCRIPTION = dict(Parameter(
                        '.',
                        name='_description',
                        prettyName='Description',
                        url='https://easydiffraction.org'
                    ))
_EXAMPLES = [
    {
        'name': 'La0.5Ba0.5CoO3',
        'description': 'neutrons, powder, constant wavelength, HRPT@PSI',
        'path': ':/Examples/La0.5Ba0.5CoO3/project.cif'

     },
     {
         'name': 'La0.5Ba0.5CoO3-Raw',
         'description': 'neutrons, powder, constant wavelength, HRPT@PSI',
         'path': ':/Examples/La0.5Ba0.5CoO3-Raw/project.cif'

      },
    {
        'name': 'Co2SiO4',
        'description': 'neutrons, powder, constant wavelength, D20@ILL',
        'path': ':/Examples/Co2SiO4/project.cif'

     },
    {
        'name': 'Dy3Al5O12',
        'description': 'neutrons, powder, constant wavelength, G41@LLB',
        'path': ':/Examples/Dy3Al5O12/project.cif'

     },
     {
        'name': 'PbSO4',
        'description': 'neutrons, powder, constant wavelength, D1A@ILL',
        'path': ':/Examples/PbSO4/project.cif'

     },
     {
         'name': 'Co2SiO4-Mult-Phases',
         'description': 'neutrons, powder, constant wavelength, D20@ILL, 2 phases',
         'path': ':/Examples/Co2SiO4-Mult-Phases/project.cif'
     },
     #{
     #    'name': 'Si3N4',
     #    'description': 'neutrons, powder, constant wavelength, multi-phase, 3T2@LLB',
     #    'path': ':/Examples/Si3N4/project.cif'
     #}
]

_DEFAULT_CIF = """data_DefaultProject
_description 'Default project description'
"""


class Project(QObject):
    createdChanged = Signal()
    needSaveChanged = Signal()
    dataBlockChanged = Signal()
    dataBlockCifChanged = Signal()
    recentChanged = Signal()
    locationChanged = Signal()
    dateCreatedChanged = Signal()
    dateLastModifiedChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proxy = parent

        self.resetAll()

    @Slot()
    def resetAll(self):
        self._dataBlock = self.createDataBlockFromCif(_DEFAULT_CIF)
        self._dataBlockCif = _DEFAULT_CIF
        self._examples = _EXAMPLES
        self._created = False
        self._needSave = False
        self._recent = []
        self._isExample = False

        self._location = ''
        self._dateCreated = ''
        self._dateLastModified = ''
        self._dirNames = {
            'models': 'models',
            'experiments': 'experiments',
            'analysis': 'analysis',
            'summary': 'summary'
        }

    @Property('QVariant', notify=dataBlockChanged)
    def dataBlock(self):
        return self._dataBlock

    @Property(str, notify=dataBlockCifChanged)
    def dataBlockCif(self):
        return self._dataBlockCif

    @Property('QVariant', constant=True)
    def examples(self):
        return self._examples

    @Property(bool, notify=createdChanged)
    def created(self):
        return self._created

    @created.setter
    def created(self, newValue):
        if self._created == newValue:
            return
        self._created = newValue
        self.createdChanged.emit()

    @Property(bool, notify=needSaveChanged)
    def needSave(self):
        return self._needSave and self._isExample == False

    @needSave.setter
    def needSave(self, newValue):
        if self._needSave == newValue:
            return
        self._needSave = newValue
        self.needSaveChanged.emit()

    @Slot()
    def setNeedSaveToTrue(self):
        self.needSave = True

    @Property('QVariant', notify=recentChanged)
    def recent(self):
        return self._recent

    @recent.setter
    def recent(self, newValue):
        newValue = newValue.toVariant()
        if self._recent == newValue:
            return
        self._recent = newValue
        self.recentChanged.emit()

    @Property(str, notify=locationChanged)
    def location(self):
        return self._location

    @location.setter
    def location(self, newValue):
        if self._location == newValue:
            return
        self._location = newValue
        self.locationChanged.emit()

    @Property(str, notify=dateCreatedChanged)
    def dateCreated(self):
        return self._dateCreated

    @dateCreated.setter
    def dateCreated(self, newValue):
        if self._dateCreated == newValue:
            return
        self._dateCreated = newValue
        self.dateCreatedChanged.emit()

    @Property(str, notify=dateLastModifiedChanged)
    def dateLastModified(self):
        return self._dateLastModified

    @dateLastModified.setter
    def dateLastModified(self, newValue):
        if self._dateLastModified == newValue:
            return
        self._dateLastModified = newValue
        self.dateLastModifiedChanged.emit()

    @Property('QVariant', constant=True)
    def dirNames(self):
        return self._dirNames

    def createDataBlockFromCif(self, edCif):
        starObj = PycifstarData()
        starObj.take_from_string(edCif)
        dataBlock = CryspyParser.starObjToEdProject(starObj)
        return dataBlock

    @Slot('QVariant')
    def loadRecentFromFile(self, fpath):
        #fpath = fpath.toLocalFile()
        #fpath = IO.generalizePath(fpath)
        self.loadProjectFromFile(fpath)

    @Slot(str)
    def loadExampleFromSoure(self, fpath):
        self._isExample = True
        self.loadProjectFromSource(fpath)

    @Slot('QVariant')
    def loadProject(self, fpath):
        fpath = fpath.toLocalFile()
        fpath = IO.generalizePath(fpath)

        if fpath in self._recent:
            self._recent.remove(fpath)
        self._recent.insert(0, fpath)
        self._recent = self._recent[:10]
        self.recentChanged.emit()

        self.loadProjectFromFile(fpath)

    def loadProjectFromSource(self, fpath):
        console.debug(f"Loading project from: {fpath}")
        file = QFile(fpath)
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            console.error('Not found in resources')
            return

        stream = QTextStream(file)
        edCif = stream.readAll()

        starObj = PycifstarData()
        starObj.take_from_string(edCif)
        self._dataBlock = CryspyParser.starObjToEdProject(starObj)

        self.location = os.path.dirname(fpath)

        modelFileNames = [item['_name']['value'] for item in self._dataBlock['loops']['_model_cif_file']]
        modelFilePaths = [os.path.join(self._location, self._dirNames['models'], fileName) for fileName in modelFileNames]
        self._proxy.model.loadModelsFromResources(modelFilePaths)

        if '_experiment_cif_file' in self._dataBlock['loops']:
            experimentFileNames = [item['_name']['value'] for item in self._dataBlock['loops']['_experiment_cif_file']]
            experimentFilePaths = [os.path.join(self._location, self._dirNames['experiments'], fileName) for fileName in experimentFileNames]
            self._proxy.experiment.loadExperimentsFromResources(experimentFilePaths)

        reportFileName = 'report.cif'
        reportFilePath = os.path.join(self._location, self._dirNames['summary'], reportFileName)
        self._proxy.summary.loadReportFromResources(reportFilePath)

        if '_description' not in self._dataBlock['params']:
            self._dataBlock['params']['_description'] = _EMPTY_DESCRIPTION

        self.dataBlockChanged.emit()
        self.created = True
        self.needSave = False

    def loadProjectFromFile(self, fpath):
        console.debug(f"Loading project from: {fpath}")
        with open(fpath, 'r') as file:
            edCif = file.read()

        starObj = PycifstarData()
        starObj.take_from_string(edCif)
        self._dataBlock = CryspyParser.starObjToEdProject(starObj)

        st = os.stat(fpath)
        fmt = "%d %b %Y %H:%M"
        #self.dateCreated = time.strftime(fmt, time.localtime(st.st_birthtime))
        self.dateLastModified = time.strftime(fmt, time.localtime(st.st_mtime))

        self.location = os.path.dirname(fpath)

        modelFileNames = [item['_name']['value'] for item in self._dataBlock['loops']['_model_cif_file']]
        modelFilePaths = [os.path.join(self._location, self._dirNames['models'], fileName) for fileName in modelFileNames]
        modelFilePaths = [QUrl.fromLocalFile(path) for path in modelFilePaths]
        self._proxy.model.loadModelsFromFiles(modelFilePaths)

        if '_experiment_cif_file' in self._dataBlock['loops']:
            experimentFileNames = [item['_name']['value'] for item in self._dataBlock['loops']['_experiment_cif_file']]
            experimentFilePaths = [os.path.join(self._location, self._dirNames['experiments'], fileName) for fileName in experimentFileNames]
            experimentFilePaths = [QUrl.fromLocalFile(path) for path in experimentFilePaths]
            self._proxy.experiment.loadExperimentsFromFiles(experimentFilePaths)

        reportFileName = 'report.cif'
        reportFilePath = os.path.join(self._location, self._dirNames['summary'], reportFileName)
        reportFilePath = QUrl.fromLocalFile(reportFilePath)
        self._proxy.summary.loadReportFromFile(reportFilePath)

        if '_description' not in self._dataBlock['params']:
            self._dataBlock['params']['_description'] = _EMPTY_DESCRIPTION

        self.dataBlockChanged.emit()
        self.created = True
        self.needSave = True

    @Slot(str)
    def setName(self, value):
        oldValue = self._dataBlock['name']['value']
        if oldValue == value:
            return
        self._dataBlock['name']['value'] = value
        console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value}', 'project.name'))
        self.dataBlockChanged.emit()

    def setModels(self):
        names = [f"{block['name']['value']}" for block in self._proxy.model.dataBlocks]
        oldNames = []
        if '_model_cif_file' in self._dataBlock['loops']:
            oldNames = [os.path.splitext(item['_name']['value'])[0] for item in self._dataBlock['loops']['_model_cif_file']]
        if oldNames == names:
            return

        self._dataBlock['loops']['_model_cif_file'] = []
        for name in names:
            edModel = {}
            edModel['_name'] = dict(Parameter(
                f'{name}.cif',
                name='_name',
                prettyName='Model file(s)',
                url='https://easydiffraction.org'
            ))
            self._dataBlock['loops']['_model_cif_file'].append(edModel)

        console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldNames} → {names}'))
        self.dataBlockChanged.emit()

    def setExperiments(self):
        names = [f"{block['name']['value']}" for block in self._proxy.experiment.dataBlocksNoMeas]
        oldNames = []
        if '_experiment_cif_file' in self._dataBlock['loops']:
            oldNames = [os.path.splitext(item['_name']['value'])[0] for item in self._dataBlock['loops']['_experiment_cif_file']]
        if oldNames == names:
            return

        self._dataBlock['loops']['_experiment_cif_file'] = []
        for name in names:
            edExperiment = {}
            edExperiment['_name'] = dict(Parameter(
                f'{name}.cif',
                name='_name',
                prettyName='Experiment file(s)',
                url='https://easydiffraction.org'
            ))
            self._dataBlock['loops']['_experiment_cif_file'].append(edExperiment)

        console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldNames} → {names}'))
        self.dataBlockChanged.emit()

    @Slot(str, str, 'QVariant')
    def setMainParam(self, paramName, field, value):
        changedIntern = self.editDataBlockMainParam(paramName, field, value)
        if changedIntern:
            self.dataBlockChanged.emit()

    def editDataBlockMainParam(self, paramName, field, value):
        blockType = 'project'
        oldValue = self._dataBlock['params'][paramName][field]
        if oldValue == value:
            return False
        self._dataBlock['params'][paramName][field] = value
        if type(value) == float:
            console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value:.6f}', f'{blockType}.{paramName}.{field}'))
        else:
            console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value}', f'{blockType}.{paramName}.{field}'))
        return True

    @Slot()
    def create(self):
        self.save()

        fpath = os.path.join(self.location, 'project.cif')
        st = os.stat(fpath)
        fmt = "%d %b %Y %H:%M"
        #self.dateCreated = time.strftime(fmt, time.localtime(st.st_birthtime))
        self.dateLastModified = time.strftime(fmt, time.localtime(st.st_mtime))

        self.created = True

    @Slot()
    def save(self):
        console.debug(IO.formatMsg('main', 'Saving project...'))

        projectDirPath = self.location
        projectFileName = 'project.cif'
        projectFilePath = os.path.join(projectDirPath, projectFileName)
        os.makedirs(projectDirPath, exist_ok=True)
        with open(projectFilePath, 'w') as file:
            file.write(self.dataBlockCif)
            console.debug(IO.formatMsg('sub', f'saved to: {projectFilePath}'))

        if self._proxy.model.defined:
            modelFileNames = [item['_name']['value'] for item in self._dataBlock['loops']['_model_cif_file']]
            modelFilePaths = [os.path.join(projectDirPath, self._dirNames['models'], fileName) for fileName in modelFileNames]
            for (modelFilePath, dataBlockCif) in zip(modelFilePaths, self._proxy.model.dataBlocksCif):
                dataBlockCif = dataBlockCif[0]
                os.makedirs(os.path.dirname(modelFilePath), exist_ok=True)
                with open(modelFilePath, 'w') as file:
                    file.write(dataBlockCif)
                    console.debug(IO.formatMsg('sub', f'saved to: {modelFilePath}'))

        if self._proxy.experiment.defined:
            experimentFileNames = [item['_name']['value'] for item in self._dataBlock['loops']['_experiment_cif_file']]
            experimentFilePaths = [os.path.join(projectDirPath, self._dirNames['experiments'], fileName) for fileName in experimentFileNames]
            for (experimentFilePath, dataBlockCifNoMeas, dataBlockCifMeasOnly) in zip(experimentFilePaths, self._proxy.experiment.dataBlocksCifNoMeas, self._proxy.experiment.dataBlocksCifMeasOnly):
                os.makedirs(os.path.dirname(experimentFilePath), exist_ok=True)
                dataBlockCif = dataBlockCifNoMeas + '\n\n' + dataBlockCifMeasOnly
                with open(experimentFilePath, 'w') as file:
                    file.write(dataBlockCif)
                    console.debug(IO.formatMsg('sub', f'saved to: {experimentFilePath}'))

        if self._proxy.summary.isCreated:
            fileName = 'report.cif'
            reportFilePath = os.path.join(projectDirPath, self._dirNames['summary'], fileName)
            os.makedirs(os.path.dirname(reportFilePath), exist_ok=True)
            with open(reportFilePath, 'w') as file:
                dataBlockCif = self._proxy.summary.dataBlocksCif
                file.write(dataBlockCif)
                console.debug(IO.formatMsg('sub', f'saved to: {reportFilePath}'))

        self.needSave = False

    def setDataBlockCif(self):
        self._dataBlockCif = CryspyParser.dataBlockToCif(self._dataBlock)
        console.debug(IO.formatMsg('sub', 'Project', '', 'to CIF string', 'converted'))
        self.dataBlockCifChanged.emit()
