# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Slot

from EasyApp.Logic.Logging import console
from Logic.Helpers import IO


class Connections(QObject):

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._silent = False
        self._modelNeedUpdate = False
        self._experimentNeedUpdate = False

        # Project
        self._proxy.project.dataBlockChanged.connect(self.onProjectDataBlockChanged)
        self._proxy.project.createdChanged.connect(self.onProjectCreatedChanged)

        # Model
        self._proxy.model.currentIndexChanged.connect(self.onModelCurrentIndexChanged)
        self._proxy.model.dataBlocksChanged.connect(self.onModelDataBlocksChanged)

        # Experiment
        self._proxy.experiment.currentIndexChanged.connect(self.onExperimentCurrentIndexChanged)
        self._proxy.experiment.dataBlocksNoMeasChanged.connect(self.onExperimentDataBlocksNoMeasChanged)
        self._proxy.experiment.dataBlocksChanged.connect(self.onExperimentDataBlocksChanged)

        # Analysis
        self._proxy.analysis.definedChanged.connect(self.onAnalysisDefined)

        # Fittables
        self._proxy.fittables.nameFilterCriteriaChanged.connect(self.onFittablesFilterCriteriaChanged)
        self._proxy.fittables.variabilityFilterCriteriaChanged.connect(self.onFittablesFilterCriteriaChanged)
        self._proxy.fittables.paramsCountChanged.connect(self.onFittablesParamsCountChanged)
        self._proxy.fittables.modelChangedSilently.connect(self.onModelChangedSilently)
        self._proxy.fittables.experimentChangedSilently.connect(self.onExperimentChangedSilently)

        # Fitting
        self._proxy.fitting.fitFinished.connect(self.onFittingFitFinished)
        self._proxy.fitting.chiSqSignificantlyChanged.connect(self.onFittingChiSqSignificantlyChanged)
        self._proxy.fitting.minimizerMethodChanged.connect(self.onFittingMinimizerMethodChanged)

    #########
    # Project
    #########

    def onProjectCreatedChanged(self):
        self._proxy.project.setModels()
        self._proxy.project.setExperiments()

    def onProjectDataBlockChanged(self):
        self._proxy.status.project = self._proxy.project.dataBlock['name']['value']
        console.debug(IO.formatMsg('main', '(Re)converting project data block to CIF...'))
        self._proxy.project.setDataBlockCif()
        self._proxy.project.setNeedSaveToTrue()

    #######
    # Model
    #######

    def onModelCurrentIndexChanged(self):
        # Model page
        console.debug(IO.formatMsg('main', 'Updating structure view for the current model...'))
        self._proxy.model.updateCurrentModelStructView()

    def onModelDataBlocksChanged(self):        
        if self._silent:
            return

        # Project page
        if self._proxy.project.created:
            self._proxy.project.setNeedSaveToTrue()
            self._proxy.project.setModels()

        # Model page
        console.debug(IO.formatMsg('main', 'Updating structure view for the current model...'))
        self._proxy.model.updateCurrentModelStructView()
        console.debug(IO.formatMsg('main', '(Re)converting model data blocks to CIF...'))
        self._proxy.model.setDataBlocksCif()

        # Experiment page
        if self._proxy.experiment.defined:
            console.debug(IO.formatMsg('main', 'Recalculating data...'))
            self._proxy.experiment.runCryspyCalculations()
            console.debug(IO.formatMsg('main', 'Replacing arrays...'))
            self._proxy.experiment.replaceArrays()
            console.debug(IO.formatMsg('main', f'Redrawing curves on experiment page using {self._proxy.plotting.currentLib1d}...'))
            self._proxy.plotting.drawBackgroundOnExperimentChart()

        # Analysis page
        if self._proxy.analysis.defined:
            console.debug(IO.formatMsg('main', f'Redrawing curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
            self._proxy.plotting.drawCalculatedOnAnalysisChart()
            self._proxy.plotting.drawResidualOnAnalysisChart()
            self._proxy.plotting.drawBraggOnAnalysisChart()
            console.debug(IO.formatMsg('main', 'Updating fittables on the analysis page...'))
            self._proxy.fittables.set()

        # Status bar
        if self._proxy.model.defined:
            self._proxy.status.phaseCount = f'{len(self._proxy.model.dataBlocks)}'
        else:
            self._proxy.status.phaseCount = ''

        console.debug('')

    ############
    # Experiment
    ############

    def onExperimentCurrentIndexChanged(self):
        # Experiment page
        console.debug(IO.formatMsg('main', f'Redrawing curves on experiment page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawMeasuredOnExperimentChart()
        self._proxy.plotting.drawBackgroundOnExperimentChart()

        # Analysis page
        if self._proxy.analysis.defined:
            console.debug(IO.formatMsg('main', f'Redrawing curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
            self._proxy.plotting.drawMeasuredOnAnalysisChart()
            self._proxy.plotting.drawBackgroundOnAnalysisChart()
            self._proxy.plotting.drawCalculatedOnAnalysisChart()
            self._proxy.plotting.drawResidualOnAnalysisChart()
            self._proxy.plotting.drawBraggOnAnalysisChart()

    def onExperimentDataBlocksChanged(self):
        # Project page
        if self._proxy.project.created:
            self._proxy.project.setNeedSaveToTrue()
            self._proxy.project.setExperiments()

        # Experiment page
        console.debug(IO.formatMsg('main', 'Calculating data...'))
        self._proxy.experiment.runCryspyCalculations()
        console.debug(IO.formatMsg('main', 'Adding arrays and ranges...'))
        self._proxy.experiment.addArraysAndChartRanges()
        console.debug(IO.formatMsg('main', f'Drawing curves on experiment page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawMeasuredOnExperimentChart()
        self._proxy.plotting.drawBackgroundOnExperimentChart()
        console.debug(IO.formatMsg('main', 'Converting experiment data blocks to CIF...'))
        self._proxy.experiment.setDataBlocksCif()

        # Analysis page
        if self._proxy.analysis.defined:
            console.debug(IO.formatMsg('main', f'Drawing curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
            self._proxy.plotting.drawMeasuredOnAnalysisChart()
            self._proxy.plotting.drawBackgroundOnExperimentChart()
            self._proxy.plotting.drawCalculatedOnAnalysisChart()
            self._proxy.plotting.drawResidualOnAnalysisChart()
            self._proxy.plotting.drawBraggOnAnalysisChart()
            console.debug(IO.formatMsg('main', 'Setting fittables on the analysis page...'))
            self._proxy.fittables.set()

        # Status bar
        if self._proxy.experiment.defined:
            self._proxy.status.experimentsCount = f'{len(self._proxy.experiment.dataBlocksNoMeas)}'
        else:
            self._proxy.status.experimentsCount = ''

        # GUI upadte silently (without calling self.onExperimentDataBlocksNoMeasChanged)
        self._silent = True
        self._proxy.experiment.dataBlocksNoMeasChanged.emit()
        self._silent = False

        console.debug('')

    def onExperimentDataBlocksNoMeasChanged(self):
        if self._silent:
            return

        # Project page
        if self._proxy.project.created:
            self._proxy.project.setNeedSaveToTrue()
            self._proxy.project.setExperiments()

        # Experiment page
        console.debug(IO.formatMsg('main', 'Recalculating data...'))
        self._proxy.experiment.runCryspyCalculations()
        console.debug(IO.formatMsg('main', 'Replacing arrays...'))
        self._proxy.experiment.replaceArrays()
        console.debug(IO.formatMsg('main', f'Redrawing curves on experiment page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawBackgroundOnExperimentChart()
        console.debug(IO.formatMsg('main', 'Reconverting experiment data blocks to CIF...'))
        self._proxy.experiment.setDataBlocksCif()

        # Analysis page
        if self._proxy.analysis.defined:
            console.debug(IO.formatMsg('main', 'Redrawing curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
            self._proxy.plotting.drawBackgroundOnExperimentChart()
            self._proxy.plotting.drawCalculatedOnAnalysisChart()
            self._proxy.plotting.drawResidualOnAnalysisChart()
            self._proxy.plotting.drawBraggOnAnalysisChart()
            console.debug(IO.formatMsg('main', 'Updating fittables on the analysis page...'))
            self._proxy.fittables.set()

        # Status bar
        if self._proxy.experiment.defined:
            self._proxy.status.experimentsCount = f'{len(self._proxy.experiment.dataBlocksNoMeas)}'
        else:
            self._proxy.status.experimentsCount = ''

        self._proxy.project.setNeedSaveToTrue()
        console.debug('')

    ##########
    # Analysis
    ##########

    def onAnalysisDefined(self):
        self._proxy.status.calculator = 'CrysPy'
        self._proxy.status.minimizer = f'Lmfit ({self._proxy.fitting.minimizerMethod})'
        console.debug(IO.formatMsg('main', f'Drawing curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawMeasuredOnAnalysisChart()
        self._proxy.plotting.drawBackgroundOnExperimentChart()
        self._proxy.plotting.drawCalculatedOnAnalysisChart()
        self._proxy.plotting.drawResidualOnAnalysisChart()
        self._proxy.plotting.drawBraggOnAnalysisChart()
        console.debug(IO.formatMsg('main', 'Setting fittables on the analysis page...'))
        self._proxy.fittables.set()

    ###########
    # Fittables
    ###########

    def onFittablesFilterCriteriaChanged(self):
        self._proxy.fittables.set()

    def onFittablesParamsCountChanged(self):
        free = self._proxy.fittables.freeParamsCount
        fixed = self._proxy.fittables.fixedParamsCount
        total = free + fixed
        self._proxy.status.variables = f'{total} ({free} free, {fixed} fixed)'

    def onModelChangedSilently(self):
        self.recalcAndUpdateAnalysisPageOnly()
        self._modelNeedUpdate = True

    def onExperimentChangedSilently(self):
        self.recalcAndUpdateAnalysisPageOnly()
        self._experimentNeedUpdate = True

    def recalcAndUpdateAnalysisPageOnly(self):
        console.debug(IO.formatMsg('main', 'Recalculating data...'))
        self._proxy.experiment.runCryspyCalculations()
        console.debug(IO.formatMsg('main', 'Replacing arrays...'))
        self._proxy.experiment.replaceArrays()
        console.debug(IO.formatMsg('main', f'Redrawing curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawCalculatedOnAnalysisChart()
        self._proxy.plotting.drawResidualOnAnalysisChart()
        self._proxy.plotting.drawBraggOnAnalysisChart()
        console.debug(IO.formatMsg('main', 'Updating fittables on the analysis page...'))
        self._proxy.fittables.set()

    @Slot()
    def updateModelPageOnly(self):
        if not self._modelNeedUpdate:
            return
        console.debug(IO.formatMsg('main', 'Updating structure view for the current model...'))
        self._proxy.model.updateCurrentModelStructView()
        console.debug(IO.formatMsg('main', '(Re)converting model data blocks to CIF...'))
        self._proxy.model.setDataBlocksCif()
        self._modelNeedUpdate = False
        # GUI upadte silently (without calling self.onExperimentDataBlocksNoMeasChanged)
        self._silent = True
        self._proxy.model.dataBlocksChanged.emit()
        self._silent = False

    @Slot()
    def updateExperimentPageOnly(self):
        if not self._experimentNeedUpdate:
            return
        console.debug(IO.formatMsg('main', f'Redrawing curves on experiment page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawBackgroundOnExperimentChart()
        console.debug(IO.formatMsg('main', 'Converting experiment data blocks to CIF...'))
        self._proxy.experiment.setDataBlocksCif()
        self._experimentNeedUpdate = False
        # GUI upadte silently (without calling self.onExperimentDataBlocksNoMeasChanged)
        self._silent = True
        self._proxy.experiment.dataBlocksNoMeasChanged.emit()
        self._silent = False

    #########
    # Fitting
    #########

    def onFittingFitFinished(self):
        # Model page
        console.debug(IO.formatMsg('main', 'Updating structure view for the current model...'))
        self._proxy.model.updateCurrentModelStructView()
        console.debug(IO.formatMsg('main', '(Re)converting model data blocks to CIF...'))
        self._proxy.model.setDataBlocksCif()

        # Experiment page
        console.debug(IO.formatMsg('main', 'Replacing arrays...'))
        self._proxy.experiment.replaceArrays()
        console.debug(IO.formatMsg('main', f'Redrawing curves on experiment page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawBackgroundOnExperimentChart()
        console.debug(IO.formatMsg('main', 'Reconverting experiment data blocks to CIF...'))
        self._proxy.experiment.setDataBlocksCif()

        # Analysis page
        console.debug(IO.formatMsg('main', f'Redrawing curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawBackgroundOnExperimentChart()
        self._proxy.plotting.drawCalculatedOnAnalysisChart()
        self._proxy.plotting.drawResidualOnAnalysisChart()
        self._proxy.plotting.drawBraggOnAnalysisChart()
        console.debug(IO.formatMsg('main', 'Updating fittables on the analysis page...'))
        self._proxy.fittables.set()

        # Summary page
        console.debug(IO.formatMsg('main', 'Updating summary report...'))
        if not self._proxy.summary.isCreated:
            self._proxy.summary.isCreated = True
        self._proxy.summary.setDataBlocksCif()  # NEED FIX: Update summary on any change, not only after fitting

        # GUI upadte silently (without calling self.onExperimentDataBlocksNoMeasChanged)
        self._silent = True
        self._proxy.model.dataBlocksChanged.emit()
        self._proxy.experiment.dataBlocksNoMeasChanged.emit()
        self._silent = False

        # Need save after fitting
        self._proxy.project.setNeedSaveToTrue()

        console.debug('')

    def onFittingChiSqSignificantlyChanged(self):
        # Experiment page
        console.debug(IO.formatMsg('main', 'Replacing arrays...'))
        self._proxy.experiment.replaceArrays()
        # self._proxy.plotting.drawBackgroundOnExperimentChart() # Not needed!!!! as it is updated on Experiment page clicked???

        # Analysis page
        console.debug(IO.formatMsg('main', f'Redrawing curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawBackgroundOnAnalysisChart()
        self._proxy.plotting.drawCalculatedOnAnalysisChart()
        self._proxy.plotting.drawResidualOnAnalysisChart()
        self._proxy.plotting.drawBraggOnAnalysisChart()

    def onFittingMinimizerMethodChanged(self):
        self._proxy.status.minimizer = f'Lmfit ({self._proxy.fitting.minimizerMethod})'
