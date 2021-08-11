# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from dicttoxml import dicttoxml

from PySide2.QtCore import Signal, QObject

from easyDiffractionLib.sample import Sample
from easyDiffractionLib.Profiles.P1D import Instrument1DCWParameters, Instrument1DTOFParameters
from easyDiffractionLib.Profiles.P1D import Powder1DParameters


class SampleLogic(QObject):
    """
    """
    SampleChanged = Signal()

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        self._phases = parent.l_phase
        self._sample = self._defaultSample()

    ####################################################################################################################
    ####################################################################################################################
    # SAMPLE
    ####################################################################################################################
    ####################################################################################################################

    def _defaultSample(self):
        sample = Sample(
            phases=self._phases.phases,
            parameters=Instrument1DCWParameters.default(),
            pattern=Powder1DParameters.default(),
            interface=self._interface)
        sample.pattern.zero_shift = 0.0
        sample.pattern.scale = 100.0
        sample.parameters.wavelength = 1.912
        sample.parameters.resolution_u = 0.1447
        sample.parameters.resolution_v = -0.4252
        sample.parameters.resolution_w = 0.3864
        sample.parameters.resolution_x = 0.0
        sample.parameters.resolution_y = 0.0  # 0.0961
        return sample

    @property
    def experimentType(self):
        exp_type = None
        if issubclass(type(self._sample.parameters), Instrument1DCWParameters):
            exp_type = 'powder1DCW'
        elif issubclass(type(self._sample.parameters), Instrument1DTOFParameters):
            exp_type = 'Powder1DTOF'
        else:
            raise AttributeError('Unknown EXP type')
        return exp_type

    @experimentType.setter
    def experimentType(self, new_exp_type: str):
        phases = self._phases.phases
        pattern = self._sample.pattern

        if new_exp_type == 'powder1DCW':
            params = Instrument1DCWParameters.default()
        elif new_exp_type == 'powder1DTOF':
            params = Instrument1DTOFParameters.default()
        else:
            raise AttributeError('Unknown Experiment type')

        self._sample = Sample(
            phases=phases,
            parameters=params,
            pattern=pattern,
            interface=self._interface)
        self.parent.l_phase.phasesAsObjChanged.emit()
