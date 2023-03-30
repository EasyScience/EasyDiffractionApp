# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

# noqa: E501

from gemmi import cif
import numpy as np
import pathlib
import json

from PySide2.QtCore import Signal, QObject

from easyCore import np
from easyCore.Utils.io.xml import XMLSerializer
from easyApp.Logic.Utils.Utils import generalizePath
from easyDiffractionLib.Jobs import get_job_from_file


class ExperimentLogic(QObject):
    """
    """
    # signals controlled by LC
    experimentLoadedChanged = Signal()
    experimentSkippedChanged = Signal()
    clearFrontendState = Signal()

    # signals controlled by our proxy
    patternParametersAsObjChanged = Signal()
    structureParametersChanged = Signal()

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        self._experiment_parameters = None
        self._experiment_data_as_xml = ""
        self.experiment_data = None
        self._experiment_data = None
        self._experiment_loaded = False
        self._experiment_skipped = False
        self.experiments = self._defaultExperiments()
        self.clearFrontendState.connect(self.onClearFrontendState)
        self.spin_polarized = False
        self._current_spin_component = 'Sum'
        self._refine_sum = True
        self._refine_diff = True
        self._refine_up = False
        self._refine_down = False
        self.fn_aggregate = self.pol_sum

    def _defaultExperiment(self):
        return {
            "label": "D1A@ILL",
            "color": "#00a3e3"
        }

    def _loadExperimentCif(self, file_url):
        print("+ _loadExperimentCif")
        file_path = generalizePath(file_url)
        block = cif.read(file_path).sole_block()

        data = self.parent.experiments()[0]
        # Polarized case
        data.x = np.fromiter(block.find_loop("_pd_meas_2theta"), float)
        data.y = np.fromiter(block.find_loop("_pd_meas_intensity_up"), float)
        data.e = np.fromiter(block.find_loop("_pd_meas_intensity_up_sigma"), float)
        data.yb = np.fromiter(block.find_loop("_pd_meas_intensity_down"), float)
        data.eb = np.fromiter(block.find_loop("_pd_meas_intensity_down_sigma"), float)
        #self.spin_polarized = True
        spin_polarized = True
        # Unpolarized case
        if not np.any(data.y):
            data.x = np.fromiter(block.find_loop("_pd_meas_2theta"), float)
            data.y = np.fromiter(block.find_loop("_pd_meas_intensity"), float)
            data.e = np.fromiter(block.find_loop("_pd_meas_intensity_sigma"), float)
            data.yb = np.zeros(len(data.y))
            data.eb = np.zeros(len(data.e))
            #self.spin_polarized = False
            spin_polarized = False
        # setting spin polarization needs to be done first, before experiment is loaded
        self.setPolarized(spin_polarized)

        # job name from file name
        job_name = pathlib.Path(file_path).stem
        _, job = get_job_from_file(file_path, job_name, phases=self.parent.phases(), interface=self._interface)
        job.from_cif_file(file_path, experiment_name=job_name)

        # Update job on sample
        self.parent.l_sample._sample = job

        # Get phase parameters
        sample_phase_labels = self.parent.getPhaseNames()
        experiment_phase_labels = list(block.find_loop("_phase_label"))
        experiment_phase_scales = np.fromiter(block.find_loop("_phase_scale"), float)
        for (phase_label, phase_scale) in zip(experiment_phase_labels, experiment_phase_scales):
            if phase_label in sample_phase_labels:
                self.parent.setPhaseScale(phase_label, phase_scale)

        return data

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        file_path = generalizePath(file_url)
        job_name = pathlib.Path(file_path).stem

        data = self.parent.experiments()[0]
        # TODO: figure out how to tell ToF from CW
        try:
            data.x, data.y, data.e, data.yb, data.eb = np.loadtxt(file_path, unpack=True)
            self.setPolarized(True)
            job = self.parent.l_sample._defaultCWPolJob(name=job_name)
        except Exception as e:
            data.x, data.y, data.e = np.loadtxt(file_path, unpack=True)
            data.yb = np.zeros(len(data.y))
            data.eb = np.zeros(len(data.e))
            self.setPolarized(False)
            # check if set to ToF
            current_type = self.parent.experimentType()
            if 'TOF' in current_type:
                job = self.parent.l_sample._defaultTOFJob(name=job_name)
            else:
                job = self.parent.l_sample._defaultCWJob(name=job_name)

        # Update job on sample
        self.parent.l_sample._sample = job
        return data

    def _experimentDataParameters(self, data):
        x_min = data.x[0]
        x_max = data.x[-1]
        x_step = (x_max - x_min) / (len(data.x) - 1)
        parameters = {
            "x_min":  x_min,
            "x_max":  x_max,
            "x_step": x_step
        }
        return parameters

    def _defaultExperiments(self):
        return []

    def refinement(self):
        return {"sum": self._refine_sum, "diff": self._refine_diff, "up": self._refine_up, "down": self._refine_down}

    def refinement_methods(self):
        return {self.pol_sum: self._refine_sum, self.pol_diff: self._refine_diff, self.pol_up: self._refine_up, self.pol_down: self._refine_down}

    def setPolarized(self, polarized: bool):
        if self.spin_polarized == polarized:
            return False
        current_type = self.parent.experimentType()
        if 'TOF' in current_type:
            return False # no polarized for TOF

        self.spin_polarized = polarized
        if polarized:
            if 'unp' in current_type:
                current_type = current_type.replace('unp', 'pol')
            elif 'pol' in current_type:
                return False # no change
            else:
                # old style unpolarized
                current_type = current_type + "pol"
        else:
            if 'pol' in current_type:
                current_type = current_type.replace('pol', 'unp')

        self.parent.setExperimentType(current_type)
        # need to recalculate the profile
        self.parent.updateCalculatedData()
        return True

    def updateExperimentData(self, name=None):
        self._experiment_data = self.parent.experiments()[0]
        self.experiments = [{'name': name}]
        self.setCurrentExperimentDatasetName(name)
        self.setPolarized(self.spin_polarized)
        self._onExperimentDataAdded()

    def experimentLoaded(self, loaded: bool):
        if self._experiment_loaded == loaded:
            return
        self._experiment_loaded = loaded
        self.experimentLoadedChanged.emit()

    def experimentSkipped(self, skipped: bool):
        if self._experiment_skipped == skipped:
            return
        self._experiment_skipped = skipped
        self.experimentSkippedChanged.emit()

    def experimentDataAsObj(self):
        return [{'name': experiment.name} for experiment in self.parent.experiments()]

    def _setExperimentDataAsXml(self):
        self._experiment_data_as_xml = XMLSerializer().encode({"item":self.experiments}, skip=['interface'])

    def addExperimentDataFromCif(self, file_url):
        self.parent.shouldProfileBeCalculated = False # don't run update until we're done with setting parameters
        self._experiment_data = self._loadExperimentCif(file_url)
        self.newExperimentUpdate(file_url)

    def addExperimentDataFromXye(self, file_url):
        self._experiment_data = self._loadExperimentData(file_url)
        self.newExperimentUpdate(file_url)

    def newExperimentUpdate(self, file_url):
        self.parent.setExperimentName(pathlib.Path(file_url).stem)
        self.experiments = [{'name': experiment.name} for experiment in self.parent.experiments()]
        self.experimentLoaded(True)
        self.experimentSkipped(False)
        # slot in Exp proxy -> notify parameter proxy
        self.structureParametersChanged.emit()

    def addBackgroundDataFromCif(self, file_url):
        file_path = generalizePath(file_url)
        block = cif.read(file_path).sole_block()
        # Get background
        background_2thetas = np.fromiter(block.find_loop("_pd_background_2theta"), float)
        background_intensities = np.fromiter(block.find_loop("_pd_background_intensity"), float)
        self.parent.setBackgroundPoints(background_2thetas, background_intensities)

    def removeExperiment(self):
        self.parent.removeBackgroundPoints()
        self.parent.l_sample.reset()
        self.parent.removeAllConstraints()
        self._current_spin_component = 'Sum'
        self.experiments.clear()
        self._experiment_data = None
        self.experimentLoaded(False)
        self.experimentSkipped(False)
        self.setPolarized(False)
        self.parent.clearFrontendState()

    def _onExperimentSkippedChanged(self):
        self.parent.updateCalculatedData()

    def _onExperimentLoadedChanged(self):
        self.parent.onPatternParametersChanged()

    def setCurrentExperimentDatasetName(self, name):
        self.parent.setCurrentExperimentDatasetName(name)

    def initializeBackground(self):
        self.parent.setMeasuredData(
                                    self._experiment_data.x,
                                    self._experiment_data.y + self._experiment_data.yb,
                                    self._experiment_data.e + self._experiment_data.eb)

        self.parent.setSimulationParameters(json.dumps(self._experiment_parameters))
        self.parent.initializeContainer()

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        # default settings are up+down
        self.parent.setMeasuredData(
                                    self._experiment_data.x,
                                    self._experiment_data.y + self._experiment_data.yb,
                                    self._experiment_data.e + self._experiment_data.eb)
        self._experiment_parameters = \
            self._experimentDataParameters(self._experiment_data)

        # notify parameter proxy
        params_json = json.dumps(self._experiment_parameters)
        self.parent.shouldProfileBeCalculated = True # now we can run update
        self.parent.setSimulationParameters(params_json)

        if len(self.parent.sampleBackgrounds()) == 0:
            self.parent.initializeContainer()

        self.parent.setExperimentNameFromParameters()
        self.parent.notifyProjectChanged()

    def _onPatternParametersChanged(self):
        self.parent.setPatternParametersAsObj()
        # slot in Exp proxy -> notify Param proxy
        self.patternParametersAsObjChanged.emit()

    def onClearFrontendState(self):
        self.parent.clearFrontendState()

    def spinComponent(self):
        return self._current_spin_component

    @staticmethod
    def pol_sum(a, b):
        return a + b

    @staticmethod
    def pol_diff(a, b):
        return a - b

    @staticmethod
    def pol_up(a, b):
        return a

    @staticmethod
    def pol_down(a, b):
        return b

    def setSpinComponent(self, component=None):
        if self._current_spin_component == component:
            return False
        if component is not None:
            self._current_spin_component = component

        phase_label = self.parent.getPhaseNames()[0]
        components = self._interface.get_phase_components(phase_label)
        calc_y = components['components']['up']
        calc_yb = components['components']['down']
        bg = self._interface.get_component('f_background') * 2.0

        self.fn_aggregate = self.pol_sum
        has_experiment = self._experiment_data is not None
        if self._current_spin_component == 'Sum':
            if has_experiment:
                y = self._experiment_data.y + self._experiment_data.yb
                e = self._experiment_data.e + self._experiment_data.eb
            sim_y = calc_y + calc_yb + bg
            self.fn_aggregate = self.pol_sum
        elif self._current_spin_component == 'Difference':
            if has_experiment:
                y = self._experiment_data.y - self._experiment_data.yb
                e = self._experiment_data.e + self._experiment_data.eb
            bg = np.zeros_like(bg)
            sim_y = calc_y - calc_yb
            self.fn_aggregate = self.pol_diff
        elif self._current_spin_component == 'Up':
            if has_experiment:
                y = self._experiment_data.y
                e = self._experiment_data.e
            bg = bg / 2
            sim_y = calc_y + bg
            self.fn_aggregate = self.pol_up
        elif self._current_spin_component == 'Down':
            if has_experiment:
                y = self._experiment_data.yb
                e = self._experiment_data.eb
            bg = bg / 2
            sim_y = calc_yb + bg
            self.fn_aggregate = self.pol_down
        else:
            return False

        if has_experiment:
            sim_x = self._experiment_data.x
        else:
            sim_x = self.parent.sim_x()
        self.parent.setBackgroundData(sim_x, bg)
        if has_experiment:
            self.parent.setMeasuredData(self._experiment_data.x, y, e)

        self.parent.setCalculatedData(sim_x, sim_y)

        return has_experiment

    def refineSum(self):
        return self._refine_sum

    def setRefineSum(self, value):
        self._refine_sum = value

    def refineDiff(self):
        return self._refine_diff

    def setRefineDiff(self, value):
        self._refine_diff = value

    def refineUp(self):
        return self._refine_up

    def setRefineUp(self, value):
        self._refine_up = value

    def refineDown(self):
        return self._refine_down

    def setRefineDown(self, value):
        self._refine_down = value
