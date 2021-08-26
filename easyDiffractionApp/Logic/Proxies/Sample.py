# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from PySide2.QtCore import QObject, Signal, Property

from easyDiffractionApp.Logic.Parameters import defaultSimulationParams


class SampleProxy(QObject):

    experimentTypeChanged = Signal()

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_sample

    @Property(str, notify=experimentTypeChanged)
    def experimentType(self):
        return self.logic.experimentType

    @experimentType.setter
    def experimentType(self, exp_type: str):
        self.logic.experimentType = exp_type
        self.parent.parameters.simulationParametersAsObj = defaultSimulationParams(exp_type)
        self.experimentTypeChanged.emit()
        self.parent.parameters._onParametersChanged()
        self.parent.parameters._onInstrumentParametersChanged()

    def updateExperimentType(self):
        self.experimentTypeChanged.emit()
        self.parent.parameters._onParametersChanged()
        self.parent.parameters._onInstrumentParametersChanged()
