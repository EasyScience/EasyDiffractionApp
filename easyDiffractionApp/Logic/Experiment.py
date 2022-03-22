# SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

# noqa: E501

from dicttoxml import dicttoxml
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
        # Spin components to display
        self._spin_components = ['Sum', 'Difference', 'Up', 'Down']
        self._current_spin_component = 'Sum'
        self._refine_sum = True
        self._refine_diff = True

    def _defaultExperiment(self):
        return {
            "label": "D1A@ILL",
            "color": "#00a3e3"
        }

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        file_path = generalizePath(file_url)
        data = self.state._data.experiments[0]
        try:
            data.x, data.y, data.e, data.yb, data.eb = np.loadtxt(file_path, unpack=True)
            self.spin_polarized = True
        except Exception as e:
            data.x, data.y, data.e = np.loadtxt(file_path, unpack=True)
            data.yb = np.zeros(len(data.y))
            data.eb = np.zeros(len(data.e))
            self.spin_polarized = False
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

    def setSpinComponent(self, component):
        if self._current_spin_component == component:
            return False
        if component not in self._spin_components:
            return False
        self._current_spin_component = component

        if self._current_spin_component == 'Sum':
            y = self._experiment_data.y + self._experiment_data.yb
            e = self._experiment_data.e + self._experiment_data.eb
        elif self._current_spin_component == 'Difference':
            y = self._experiment_data.y - self._experiment_data.yb
            e = self._experiment_data.e - self._experiment_data.eb
        elif self._current_spin_component == 'Up':
            y = self._experiment_data.y
            e = self._experiment_data.e
        elif self._current_spin_component == 'Down':
            y = self._experiment_data.yb
            e = self._experiment_data.eb
        else:
            return False
        self.parent.l_plotting1d.setMeasuredData(self._experiment_data.x, y, e)
        return True

    def refineSum(self):
        return self._refine_sum

    def setRefineSum(self, value):
        self._refine_sum = value

    def refineDiff(self):
        return self._refine_diff

    def setRefineDiff(self, value):
        self._refine_diff = value
