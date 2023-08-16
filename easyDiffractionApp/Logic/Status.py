# SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
# SPDX-License-Identifier: BSD-3-Clause
# © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

from PySide6.QtCore import QObject, Signal, Slot, Property

from EasyApp.Logic.Logging import console


class Status(QObject):
    projectChanged = Signal()
    phaseCountChanged = Signal()
    experimentsCountChanged = Signal()
    calculatorChanged = Signal()
    minimizerChanged = Signal()
    variablesChanged = Signal()
    fitIterationChanged = Signal()
    goodnessOfFitChanged = Signal()
    fitStatusChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._project = 'Undefined'
        self._phaseCount = ''
        self._experimentsCount = ''
        self._calculator = ''
        self._minimizer = ''
        self._variables = ''
        self._fitIteration = ''
        self._goodnessOfFit = ''
        self._fitStatus = ''

    @Property(str, notify=projectChanged)
    def project(self):
        return self._project

    @project.setter
    def project(self, newValue):
        if self._project == newValue:
            return
        self._project = newValue
        self.projectChanged.emit()

    @Property(str, notify=phaseCountChanged)
    def phaseCount(self):
        return self._phaseCount

    @phaseCount.setter
    def phaseCount(self, newValue):
        if self._phaseCount == newValue:
            return
        self._phaseCount = newValue
        self.phaseCountChanged.emit()

    @Property(str, notify=experimentsCountChanged)
    def experimentsCount(self):
        return self._experimentsCount

    @experimentsCount.setter
    def experimentsCount(self, newValue):
        if self._experimentsCount == newValue:
            return
        self._experimentsCount = newValue
        self.experimentsCountChanged.emit()

    @Property(str, notify=calculatorChanged)
    def calculator(self):
        return self._calculator

    @calculator.setter
    def calculator(self, newValue):
        if self._calculator == newValue:
            return
        self._calculator = newValue
        self.calculatorChanged.emit()

    @Property(str, notify=minimizerChanged)
    def minimizer(self):
        return self._minimizer

    @minimizer.setter
    def minimizer(self, newValue):
        if self._minimizer == newValue:
            return
        self._minimizer = newValue
        self.minimizerChanged.emit()

    @Property(str, notify=variablesChanged)
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, newValue):
        if self._variables == newValue:
            return
        self._variables = newValue
        self.variablesChanged.emit()

    @Property(str, notify=fitIterationChanged)
    def fitIteration(self):
        return self._fitIteration

    @fitIteration.setter
    def fitIteration(self, newValue):
        if self._fitIteration == newValue:
            return
        self._fitIteration = newValue
        self.fitIterationChanged.emit()

    @Property(str, notify=goodnessOfFitChanged)
    def goodnessOfFit(self):
        return self._goodnessOfFit

    @goodnessOfFit.setter
    def goodnessOfFit(self, newValue):
        if self._goodnessOfFit == newValue:
            return
        self._goodnessOfFit = newValue
        self.goodnessOfFitChanged.emit()

    @Property(str, notify=fitStatusChanged)
    def fitStatus(self):
        return self._fitStatus

    @fitStatus.setter
    def fitStatus(self, newValue):
        if self._fitStatus == newValue:
            return
        self._fitStatus = newValue
        self.fitStatusChanged.emit()

    @Slot()
    def resetAll(self):
        self.project = 'Undefined'
        self.phaseCount = ''
        self.experimentsCount = ''
        self.calculator = ''
        self.minimizer = ''
        self.variables = ''
        self.fitIteration = ''
        self.goodnessOfFit = ''
        self.fitStatus = ''
        console.debug("All status info removed")
