# SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

# noqa: E501

from dicttoxml import dicttoxml
from gemmi import cif
import numpy as np
import pathlib
import json

from PySide2.QtCore import Signal, QObject

from easyCore import np

from easyApp.Logic.Utils.Utils import generalizePath


class ExperimentLogic(QObject):
    """
    """
    experimentLoadedChanged = Signal()
    experimentSkippedChanged = Signal()
    experimentDataChanged = Signal()
    patternParametersAsObjChanged = Signal()
    clearFrontendState = Signal()

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self.state = parent.l_parameters
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

        # Get experiment type
        # Set default experiment type: powder1DCWunp
        self.parent.l_sample.experimentType = 'powder1DCWunp'
        # Check if powder1DCWpol
        value = block.find_value("_diffrn_radiation_polarization")
        if value is not None:
            self.parent.l_sample.experimentType = 'powder1DCWpol'
        # Check if powder1DTOFunp
        # ...
        # Check if powder1DTOFpol
        # ...

        # Get diffraction radiation parameters
        pattern_parameters = self.parent.l_sample._sample.pattern
        value = block.find_value("_diffrn_radiation_polarization")
        if value is not None:
            pattern_parameters.polarization = float(value)
        value = block.find_value("_diffrn_radiation_efficiency")
        if value is not None:
            pattern_parameters.efficiency = float(value)

        # Get pattern parameters
        pattern_parameters = self.parent.l_sample._sample.pattern
        value = block.find_value("_setup_offset_2theta")
        if value is not None:
            pattern_parameters.zero_shift = float(value)

        # Get instrumental parameters
        instrument_parameters = self.parent.l_sample._sample.parameters
        value = block.find_value("_setup_wavelength")
        if value is not None:
            instrument_parameters.wavelength = float(value)
        value = block.find_value("_pd_instr_resolution_u")
        if value is not None:
            instrument_parameters.resolution_u = float(value)
        value = block.find_value("_pd_instr_resolution_v")
        if value is not None:
            instrument_parameters.resolution_v = float(value)
        value = block.find_value("_pd_instr_resolution_w")
        if value is not None:
            instrument_parameters.resolution_w = float(value)
        value = block.find_value("_pd_instr_resolution_x")
        if value is not None:
            instrument_parameters.resolution_x = float(value)
        value = block.find_value("_pd_instr_resolution_y")
        if value is not None:
            instrument_parameters.resolution_y = float(value)

        # Get phase parameters
        sample_phase_labels = self.parent.l_phase.phases.phase_names
        experiment_phase_labels = list(block.find_loop("_phase_label"))
        experiment_phase_scales = np.fromiter(block.find_loop("_phase_scale"), float)
        for (phase_label, phase_scale) in zip(experiment_phase_labels, experiment_phase_scales):
            if phase_label in sample_phase_labels:
                self.parent.l_phase.phases[phase_label].scale = phase_scale

        # Get data
        data = self.state._data.experiments[0]
        # Polarized case
        data.x = np.fromiter(block.find_loop("_pd_meas_2theta"), float)
        data.y = np.fromiter(block.find_loop("_pd_meas_intensity_up"), float)
        data.e = np.fromiter(block.find_loop("_pd_meas_intensity_up_sigma"), float)
        data.yb = np.fromiter(block.find_loop("_pd_meas_intensity_down"), float)
        data.eb = np.fromiter(block.find_loop("_pd_meas_intensity_down_sigma"), float)
        self.spin_polarized = True
        # Unpolarized case
        if not np.any(data.y):
            data.x = np.fromiter(block.find_loop("_pd_meas_2theta"), float)
            data.y = np.fromiter(block.find_loop("_pd_meas_intensity"), float)
            data.e = np.fromiter(block.find_loop("_pd_meas_intensity_sigma"), float)
            data.yb = np.zeros(len(data.y))
            data.eb = np.zeros(len(data.e))
            self.spin_polarized = False
        self.setPolarized(self.spin_polarized)
        return data

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        file_path = generalizePath(file_url)
        data = self.state._data.experiments[0]
        try:
            data.x, data.y, data.e, data.yb, data.eb = np.loadtxt(file_path, unpack=True)
            self.setPolarized(True)
        except Exception as e:
            data.x, data.y, data.e = np.loadtxt(file_path, unpack=True)
            data.yb = np.zeros(len(data.y))
            data.eb = np.zeros(len(data.e))
            self.setPolarized(False)
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

    def setPolarized(self, polarized: bool):
        if self.spin_polarized == polarized:
            return False
        current_type = self.parent.l_sample.experimentType
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

        self.parent.l_sample.experimentType = current_type
        # need to recalculate the profile
        self.state._updateCalculatedData()
        return True

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
        return [{'name': experiment.name} for experiment in self.state._data.experiments]

    def _setExperimentDataAsXml(self):
        self._experiment_data_as_xml = dicttoxml(self.experiments, attr_type=True).decode()  # noqa: E501

    def addExperimentDataFromCif(self, file_url):
        self._experiment_data = self._loadExperimentCif(file_url)
        self.state._data.experiments[0].name = pathlib.Path(file_url).stem
        self.experiments = [{'name': experiment.name} for experiment in self.state._data.experiments]
        self.experimentLoaded(True)
        self.experimentSkipped(False)
        # need to update parameters in all the places.
        self.parent.l_phase.structureParametersChanged.emit()

    def addExperimentDataFromXye(self, file_url):
        self._experiment_data = self._loadExperimentData(file_url)
        self.state._data.experiments[0].name = pathlib.Path(file_url).stem
        self.experiments = [{'name': experiment.name} for experiment in self.state._data.experiments]
        self.experimentLoaded(True)
        self.experimentSkipped(False)

    def addBackgroundDataFromCif(self, file_url):
        file_path = generalizePath(file_url)
        block = cif.read(file_path).sole_block()
        # Get background
        background_2thetas = np.fromiter(block.find_loop("_pd_background_2theta"), float)
        background_intensities = np.fromiter(block.find_loop("_pd_background_intensity"), float)
        self.parent.l_background.addPoints(background_2thetas, background_intensities)
        self.parent.l_background._setAsXml()
        self.parent.l_plotting1d.bokehBackgroundDataObjChanged.emit()

    def removeExperiment(self):
        if len(self.parent.l_sample._sample.pattern.backgrounds) > 0:
            self.parent.l_background.removeAllPoints()
        self.parent.l_fitting.removeAllConstraints()
        self.setPolarized(False)
        self._current_spin_component = 'Sum'
        self.experiments.clear()
        self.experimentLoaded(False)
        self.experimentSkipped(False)

    def _onExperimentSkippedChanged(self):
        self.state._updateCalculatedData()

    def _onExperimentLoadedChanged(self):
        self.state._onPatternParametersChanged()

    def setCurrentExperimentDatasetName(self, name):
        self.parent.l_phase.setCurrentExperimentDatasetName(name)

    def initializeBackground(self):
        self.parent.l_plotting1d.setMeasuredData(
                                          self._experiment_data.x,
                                          self._experiment_data.y + self._experiment_data.yb,
                                          self._experiment_data.e + self._experiment_data.eb)

        self.parent.proxy.parameters.simulationParametersAsObj = \
            json.dumps(self._experiment_parameters)
        self.parent.l_background.initializeContainer()

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        # default settings are up+down
        self.parent.l_plotting1d.setMeasuredData(
                                          self._experiment_data.x,
                                          self._experiment_data.y + self._experiment_data.yb,
                                          self._experiment_data.e + self._experiment_data.eb)
        self._experiment_parameters = \
            self._experimentDataParameters(self._experiment_data)

        # non-kosher connection to foreign proxy. Ewwww :(
        self.parent.proxy.parameters.simulationParametersAsObj = \
            json.dumps(self._experiment_parameters)

        if len(self.parent.l_sample._sample.pattern.backgrounds) == 0:
            self.parent.l_background.initializeContainer()

        self.parent.l_project._project_info['experiments'] = \
            self.parent.l_parameters._data.experiments[0].name

        self.parent.l_project.projectInfoChanged.emit()

    def _onPatternParametersChanged(self):
        self.state._setPatternParametersAsObj()
        self.patternParametersAsObjChanged.emit()

    def onClearFrontendState(self):
        self.parent.l_plotting1d.clearFrontendState()

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

        phase_label = self.parent.l_phase.phases.phase_names[0]
        components = self._interface.get_phase_components(phase_label)
        calc_y = components['components']['up']
        calc_yb = components['components']['down']
        bg = self._interface.get_component('background')

        self.fn_aggregate = self.pol_sum
        if self._current_spin_component == 'Sum':
            if self._experiment_data is not None:
                y = self._experiment_data.y + self._experiment_data.yb
                e = self._experiment_data.e + self._experiment_data.eb
            sim_y = calc_y + calc_yb + bg
            self.fn_aggregate = self.pol_sum
        elif self._current_spin_component == 'Difference':
            if self._experiment_data is not None:
                y = self._experiment_data.y - self._experiment_data.yb
                e = self._experiment_data.e + self._experiment_data.eb
            sim_y = calc_y - calc_yb
            self.fn_aggregate = self.pol_diff
        elif self._current_spin_component == 'Up':
            if self._experiment_data is not None:
                y = self._experiment_data.y
                e = self._experiment_data.e
            sim_y = calc_y + bg
            self.fn_aggregate = self.pol_up
        elif self._current_spin_component == 'Down':
            if self._experiment_data is not None:
                y = self._experiment_data.yb
                e = self._experiment_data.eb
            sim_y = calc_yb + bg
            self.fn_aggregate = self.pol_down
        else:
            return False
        if self._experiment_data is None:
            sim_x = self.state.sim_x()
        else:
            sim_x = self._experiment_data.x
        self.parent.l_plotting1d.setCalculatedData(sim_x, sim_y)

        if self._experiment_data is not None:
            self.parent.l_plotting1d.setMeasuredData(self._experiment_data.x, y, e)
            return True
        return False

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
