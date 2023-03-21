# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import numpy as np

from PySide2.QtCore import QObject, Signal

from easyDiffractionApp.Logic.Background import BackgroundLogic
from easyDiffractionApp.Logic.Experiment import ExperimentLogic
from easyDiffractionApp.Logic.Fitting import FittingLogic
from easyDiffractionApp.Logic.Parameters import ParametersLogic
from easyDiffractionApp.Logic.Phase import PhaseLogic
from easyDiffractionApp.Logic.Sample import SampleLogic
from easyDiffractionApp.Logic.Plotting1d import Plotting1dLogic
from easyDiffractionApp.Logic.Plotting3d import Plotting3dLogic
from easyDiffractionApp.Logic.Project import ProjectLogic
from easyDiffractionApp.Logic.Stack import StackLogic
from easyDiffractionApp.Logic.State import StateLogic
from easyDiffractionLib.interface import InterfaceFactory


class LogicController(QObject):
    """
    Controller class for communication between the logic components.
    """
    parametersChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.proxy = parent
        self.interface = InterfaceFactory()
        self.shouldProfileBeCalculated = True

        # Screen recorder
        self._screen_recorder = self.recorder()

        # instantiate logics
        self.initializeLogics()

        # define signal forwarders
        self.setupSignals()

    def initializeLogics(self):
        self.l_state = StateLogic(self, interface=self.interface)
        self.l_parameters = ParametersLogic(self, interface=self.interface)
        self.l_experiment = ExperimentLogic(self, interface=self.interface)
        self.l_phase = PhaseLogic(self, interface=self.interface)
        self.l_sample = SampleLogic(self, interface=self.interface)
        self.l_fitting = FittingLogic(self, interface=self.interface)
        self.l_plotting1d = Plotting1dLogic(self, interface=self.interface)
        self.l_plotting3d = Plotting3dLogic(self)
        self.l_background = BackgroundLogic(self)
        self.l_project = ProjectLogic(self, interface=self.interface)
        # stack logic
        no_history = [self.parametersChanged]
        with_history = [self.l_phase.phaseAdded, self.parametersChanged]
        self.l_stack = StackLogic(self, self.proxy,
                                  callbacks_no_history=no_history,
                                  callbacks_with_history=with_history)

    def setupSignals(self):
        self.l_fitting.fitFinished.connect(self.parametersChanged)
        self.l_fitting.fitFinished.connect(self.l_parameters.parametersChanged)

        # self.l_project.phasesEnabled.connect(self.l_phase.phasesEnabled)
        self.l_project.phasesAsObjChanged.connect(self.l_phase.phasesAsObjChanged)
        self.l_project.structureParametersChanged.connect(self.l_phase.structureParametersChanged)

        self.l_parameters.parametersValuesChanged.connect(self.parametersChanged)
        self.l_parameters.plotCalculatedDataSignal.connect(self.plotCalculatedData)
        self.l_parameters.plotBraggDataSignal.connect(self.plotBraggData)
        self.l_parameters.undoRedoChanged.connect(self.l_stack.undoRedoChanged)

        self.l_phase.updateProjectInfo.connect(self.l_project.updateProjectInfo)
        self.parametersChanged.connect(self.onParametersChanged)

    def resetFactory(self):
        self.interface = InterfaceFactory()

    def sample(self):
        return self.l_sample._sample

    def refinementMethods(self):
        return self.l_experiment.refinement_methods()

    def isSpinPolarized(self):
        return self.l_experiment.spin_polarized

    def spinComponent(self):
        return self.l_experiment.spinComponent()

    def setSpinComponent(self):
        self.l_experiment.setSpinComponent()

    def pdata(self):
        return self.l_parameters._data

    def experiments(self):
        return self.pdata().experiments

    def setExperimentName(self, name=""):
        self.l_parameters._data.experiments[0].name = name

    def updateCalculatedData(self):
        self.l_parameters._updateCalculatedData()

    def plotCalculatedData(self, data):
        self.l_plotting1d.setCalculatedData(data[0], data[1])

    def calculatorListChanged(self):
        self.proxy.fitting.calculatorListChanged.emit()

    def plotBraggData(self, data):
        self.l_plotting1d.setBraggData(data[0], data[1], data[2], data[3], data[4])  # noqa: E501

    def initializeBorg(self):
        self.l_stack.initializeBorg()

    def assignPhaseIndex(self):
        self.sample().output_index = self.l_phase._current_phase_index

    def resetState(self):
        # TO FIX: after modifying the interface string
        # self.l_fitting.setCurrentCalculatorIndex(0)
        if self.l_phase.samplesPresent():
            self.l_phase.removeAllPhases()
        self.l_plotting1d.clearBackendState()
        self.l_plotting1d.clearFrontendState()
        self.l_stack.resetUndoRedoStack()
        self.l_stack.undoRedoChanged.emit()

    def assignToSample(self, sample_descr):
        self.l_sample._sample = sample_descr
        self.l_phase.phases = self.l_sample._sample._phases
        self.proxy.sample.updateExperimentType()
        # send signal to tell the proxy we changed phases
        self.l_phase.phaseAdded.emit()

    def sendToExperiment(self, data, exp_name):
        self.setExperimentLoaded(True)
        self.shouldProfileBeCalculated = False # don't calculate profile before all the loading took place
        self.setExperimentData(data)
        self.l_experiment.updateExperimentData(exp_name)
        self.shouldProfileBeCalculated = True # now we can calculate profile
        self.updateBackgroundOnLoad()
        self.l_experiment.experimentLoadedChanged.emit()

    def setExperimentData(self, data):
        self.l_parameters._data.experiments[0].x = np.array(data[0])
        self.l_parameters._data.experiments[0].y = np.array(data[1])
        self.l_parameters._data.experiments[0].e = np.array(data[2])

        if(len(data) > 3):
            self.l_parameters._data.experiments[0].yb = np.array(data[3])
            self.l_parameters._data.experiments[0].eb = np.array(data[4])
            self.l_experiment.spin_polarized = True
        else:
            length = len(self.l_parameters._data.experiments[0].y)
            self.l_parameters._data.experiments[0].yb = np.zeros(length)
            self.l_parameters._data.experiments[0].eb = np.zeros(length)
            self.l_experiment.spin_polarized = False

    def fnAggregate(self):
        return self.l_experiment.fn_aggregate

    def sampleBackgrounds(self):
        return self.l_sample._sample.pattern.backgrounds

    def updateBackground(self, background):
        self.l_parameters.parametersChanged.emit()
        self.l_sample._sample.set_background(background)
        self.l_parameters._updateCalculatedData()

    def updateBackgroundOnLoad(self):
        # self.l_background.onAsObjChanged()
        self.l_background.backgroundLoaded()
        if self.l_experiment.spin_polarized:
            self.l_experiment.setSpinComponent()
        self.l_parameters.parametersChanged.emit()
        self.l_sample._sample.set_background(self.l_background._background_as_obj)

    def setExperimentLoaded(self, loaded=True):
        self.l_experiment.experimentLoaded(loaded)
        self.l_experiment.experimentSkipped(not loaded)

    def removeExperiment(self, skipped=False):
        self.l_experiment.experimentLoaded(False)
        self.setExperimentLoaded(False)
        if skipped:
            self.l_experiment.experimentSkipped(True)
            self.l_experiment.experimentSkippedChanged.emit()

    def setExperimentType(self, t=""):
        self.l_sample.experimentType = t

    def experimentType(self):
        return self.l_sample.experimentType

    def experimentLoaded(self):
        return self.l_experiment._experiment_loaded

    def experimentSkipped(self):
        return self.l_experiment._experiment_skipped

    def experimentName(self):
        return self.l_experiment.experimentDataAsObj()[0]["name"]

    def getSampleAsDict(self):
        return self.l_sample._sample.as_dict(skip=['interface', 'calculator', 'datastore'])

    def setPhaseScale(self, phase_label, phase_scale):
        self.l_phase.phases[phase_label].scale = phase_scale

    def setCalculatedDataForPhase(self):
        self.l_plotting1d.setCalculatedDataForPhase()

    def phases(self):
        return self.l_phase.phases

    def phasesAsObjChanged(self):
        self.l_phase.phasesAsObjChanged.emit()

    def setPhasesOnSample(self, phases):
        self.l_sample._sample.phases = phases

    def sim_x(self):
        return self.l_parameters.sim_x()

    def getPhaseNames(self):
        return self.l_phase.phases.phase_names

    def onPatternParametersChanged(self):
        self.l_parameters._onPatternParametersChanged()

    def emitParametersChanged(self):
        self.l_parameters.parametersChanged.emit()

    def setPatternParametersAsObj(self):
        self.l_parameters._setPatternParametersAsObj()

    def getExperiments(self):
        return self.l_parameters.getExperiments()

    def setCurrentExperimentDatasetName(self, name):
        self.l_phase.setCurrentExperimentDatasetName(name)

    def isExperimentSkipped(self):
        return self.l_experiment._experiment_skipped

    def setExperimentNameFromParameters(self):
        self.l_project._project_info['experiments'] = \
            self.l_parameters._data.experiments[0].name

    def fittingNamesDict(self):
        return self.l_fitting.fittingNamesDict()

    def resetStack(self):
        self.l_stack.resetUndoRedoStack()
        self.l_stack.undoRedoChanged.emit()

    def setNewEngine(self, engine=None, method=None):
        self.l_fitting.setNewEngine(engine, method)

    def setSampleOnFitter(self):
        self.l_fitting.fitter.fit_object = self.l_sample._sample

    def statusModelAsObj(self):
        engine_name = self.l_fitting.fitter.current_engine.name
        minimizer_name = self.l_fitting._current_minimizer_method_name
        return self.l_state.statusModelAsObj(engine_name, minimizer_name)

    def statusModelAsXml(self):
        engine_name = self.l_fitting.fitter.current_engine.name
        minimizer_name = self.l_fitting._current_minimizer_method_name
        return self.l_state.statusModelAsXml(engine_name, minimizer_name)

    def initializeContainer(self):
        self.l_background.initializeContainer()

    def setBackgroundData(self, x, y):
        self.l_plotting1d.setBackgroundData(x, y)

    def setMeasuredData(self, x, y, e):
        self.l_plotting1d.setMeasuredData(x, y, e)

    def setCalculatedData(self, x, y):
        self.l_plotting1d.setCalculatedData(x, y)

    def clearFrontendState(self):
        self.l_plotting1d.clearFrontendState()

    def setBackgroundPoints(self, bg_2thetas, bg_intensities):
        self.l_background.addPoints(bg_2thetas, bg_intensities)
        self.l_background._setAsXml()
        self.l_plotting1d.bokehBackgroundDataObjChanged.emit()

    def removeBackgroundPoints(self):
        if len(self.l_sample._sample.pattern.backgrounds) > 0:
            self.l_background.removeAllPoints()

    def removeAllConstraints(self):
        self.l_fitting.removeAllConstraints()

    def setSimulationParameters(self, params):
        self.proxy.parameters.simulationParametersAsObj = params

    def notifyProjectChanged(self):
        self.l_project.projectInfoChanged.emit()

    def onParametersChanged(self):
        self.l_phase.structureParametersChanged.emit()
        self.l_experiment._onPatternParametersChanged()
        self.l_parameters.instrumentParametersChanged.emit()
        self.l_background.onAsObjChanged()  # this invokes _updateCalculatedData()
        self.l_stack.undoRedoChanged.emit()

    def recorder(self):
        rec = None
        try:
            from easyDiffractionApp.Logic.ScreenRecorder import ScreenRecorder
            rec = ScreenRecorder()
        except (ImportError, ModuleNotFoundError):
            print('Screen recording disabled')
        return rec
