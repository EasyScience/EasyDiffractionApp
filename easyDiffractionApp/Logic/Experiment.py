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

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.state = parent.l_parameters

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

        # Get pattern parameters
        pattern_parameters = self.parent.l_sample._sample.pattern
        if (value := block.find_value("_setup_offset_2theta")) is not None:
            pattern_parameters.zero_shift = float(value)

        # Get instrumental parameters
        instrument_parameters = self.parent.l_sample._sample.parameters
        if (value := block.find_value("_setup_wavelength")) is not None:
            instrument_parameters.wavelength = float(value)
        if (value := block.find_value("_pd_instr_resolution_u")) is not None:
            instrument_parameters.resolution_u = float(value)
        if (value := block.find_value("_pd_instr_resolution_v")) is not None:
            instrument_parameters.resolution_v = float(value)
        if (value := block.find_value("_pd_instr_resolution_w")) is not None:
            instrument_parameters.resolution_w = float(value)
        if (value := block.find_value("_pd_instr_resolution_x")) is not None:
            instrument_parameters.resolution_x = float(value)
        if (value := block.find_value("_pd_instr_resolution_y")) is not None:
            instrument_parameters.resolution_y = float(value)

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
        self._onPatternParametersChanged()
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

    def addExperimentDataFromXye(self, file_url):
        self._experiment_data = self._loadExperimentData(file_url)
        self.state._data.experiments[0].name = pathlib.Path(file_url).stem
        self.experiments = [{'name': experiment.name} for experiment in self.state._data.experiments]
        self.experimentLoaded(True)
        self.experimentSkipped(False)

    def removeExperiment(self):
        if len(self.parent.l_sample._sample.pattern.backgrounds) > 0:
            self.parent.l_background.removeAllPoints()
        self.parent.l_fitting.removeAllConstraints()
        self.setPolarized(False)
        self.experiments.clear()
        self.experimentLoaded(False)
        self.experimentSkipped(False)

    def _onExperimentSkippedChanged(self):
        self.state._updateCalculatedData()

    def _onExperimentLoadedChanged(self):
        self.state._onPatternParametersChanged()

    def setCurrentExperimentDatasetName(self, name):
        self.parent.l_phase.setCurrentExperimentDatasetName(name)

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        self.parent.l_plotting1d.setMeasuredData(
                                          self._experiment_data.x,
                                          self._experiment_data.y,
                                          self._experiment_data.e)
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

    def pol_sum(self, a, b):
        return a + b
    def pol_diff(self, a, b):
        return a - b
    def pol_up(self, a, b):
        return a
    def pol_down(self, a, b):
        return b

    def setSpinComponent(self, component=None):
        if self._current_spin_component == component:
            return False
        if component is not None:
            self._current_spin_component = component

        self.fn_aggregate = self.pol_sum
        if self._current_spin_component == 'Sum':
            if self._experiment_data is not None:
                y = 0.5*(self._experiment_data.y + self._experiment_data.yb)
                e = 0.5*(self._experiment_data.e + self._experiment_data.eb)
            self.fn_aggregate = self.pol_sum
        elif self._current_spin_component == 'Difference':
            if self._experiment_data is not None:
                y = self._experiment_data.y - self._experiment_data.yb
                e = self._experiment_data.e - self._experiment_data.eb
            self.fn_aggregate = self.pol_diff
        elif self._current_spin_component == 'Up':
            if self._experiment_data is not None:
                y = self._experiment_data.y
                e = self._experiment_data.e
            self.fn_aggregate = self.pol_up
        elif self._current_spin_component == 'Down':
            if self._experiment_data is not None:
                y = self._experiment_data.yb
                e = self._experiment_data.eb
            self.fn_aggregate = self.pol_down
        else:
            return False
        if self._experiment_data is not None:
            self.parent.l_plotting1d.setMeasuredData(self._experiment_data.x, y, e)
        # recalculate the profile for the new spin case
        self.parent.l_parameters._updateCalculatedData()
        if self._experiment_data is not None:
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
