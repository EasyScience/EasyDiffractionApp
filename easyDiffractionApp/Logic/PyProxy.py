# SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
# SPDX-License-Identifier: BSD-3-Clause
# © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

from PySide6.QtCore import QObject, Property

from EasyApp.Logic.Logging import LoggerLevelHandler
from Logic.Connections import Connections
from Logic.Project import Project
from Logic.Experiment import Experiment
from Logic.Model import Model
from Logic.Data import Data
from Logic.Analysis import Analysis
from Logic.Fitting import Fitting
from Logic.Fittables import Fittables
from Logic.Summary import Summary
from Logic.Status import Status
from Logic.Plotting import Plotting
from Logic.Helpers import BackendHelpers


class PyProxy(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._logger = LoggerLevelHandler(self)
        self._project = Project(self)
        self._experiment = Experiment(self)
        self._model = Model(self)
        self._data = Data(self)
        self._analysis = Analysis(self)
        self._fittables = Fittables(self)
        self._fitting = Fitting(self)
        self._summary = Summary(self)
        self._status = Status(self)
        self._plotting = Plotting(self)
        self._connections = Connections(self)
        self._backendHelpers = BackendHelpers(self)

    @Property('QVariant', constant=True)
    def logger(self):
        return self._logger

    @Property('QVariant', constant=True)
    def connections(self):
        return self._connections

    @Property('QVariant', constant=True)
    def project(self):
        return self._project

    @Property('QVariant', constant=True)
    def experiment(self):
        return self._experiment

    @Property('QVariant', constant=True)
    def model(self):
        return self._model

    @Property('QVariant', constant=True)
    def data(self):
        return self._data

    @Property('QVariant', constant=True)
    def analysis(self):
        return self._analysis

    @Property('QVariant', constant=True)
    def fitting(self):
        return self._fitting

    @Property('QVariant', constant=True)
    def fittables(self):
        return self._fittables

    @Property('QVariant', constant=True)
    def summary(self):
        return self._summary

    @Property('QVariant', constant=True)
    def status(self):
        return self._status

    @Property('QVariant', constant=True)
    def plotting(self):
        return self._plotting

    @Property('QVariant', constant=True)
    def backendHelpers(self):
        return self._backendHelpers
