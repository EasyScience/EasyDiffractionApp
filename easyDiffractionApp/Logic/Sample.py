# SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from PySide2.QtCore import Signal, QObject

from easyCore.Datasets.xarray import xr
from easyDiffractionLib.Profiles.P1D import Instrument1DCWParameters, Instrument1DTOFParameters, Instrument1DCWPolParameters
from easyDiffractionLib.Jobs import Powder1DCW, Powder1DTOF, PolPowder1DCW


class SampleLogic(QObject):
    """
    """
    SampleChanged = Signal()

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._phases = parent.l_phase
        self._interface = interface
        self._sample = self._defaultCWJob()

    def _defaultCWJob(self, name=None):
        if name is None:
            name = 'default_job_9999'
        job = Powder1DCW(name, phases=self._phases.phases, interface=self._interface)
        job.pattern.zero_shift = 0.9999
        job.pattern.scale = 9999.0
        job.parameters.wavelength = 1.912
        job.parameters.resolution_u = 0.1447
        job.parameters.resolution_v = -0.4252
        job.parameters.resolution_w = 0.3864
        job.parameters.resolution_x = 0.0
        job.parameters.resolution_y = 0.0  # 0.0961
        job.parameters.reflex_asymmetry_p1 = 0.0
        job.parameters.reflex_asymmetry_p2 = 0.0
        job.parameters.reflex_asymmetry_p3 = 0.0
        job.parameters.reflex_asymmetry_p4 = 0.0
        return job

    def _defaultCWPolJob(self):
        job = PolPowder1DCW('default_job_8888', phases=self._phases.phases, interface=self._interface)
        # unpolarized parameters
        job.pattern.zero_shift = 0.8888
        job.pattern.scale = 8888.0
        job.parameters.wavelength = 1.912
        job.parameters.resolution_u = 0.1447
        job.parameters.resolution_v = -0.4252
        job.parameters.resolution_w = 0.3864
        job.parameters.resolution_x = 0.0
        job.parameters.resolution_y = 0.0  # 0.0961
        job.parameters.reflex_asymmetry_p1 = 0.0
        job.parameters.reflex_asymmetry_p2 = 0.0
        job.parameters.reflex_asymmetry_p3 = 0.0
        job.parameters.reflex_asymmetry_p4 = 0.0
        # polarized parameters
        job.pattern.beam.polarization = 0.0
        job.pattern.beam.efficiency = 100.0
        return job

    def _defaultTOFJob(self):
        job = Powder1DTOF('default_job_7777', phases=self._phases.phases, interface=self._interface)
        job.pattern.zero_shift = 0.7777
        job.pattern.scale = 7777.0
        job.parameters.dtt1 = 6167.24700
        job.parameters.dtt2 = -2.28000
        job.parameters.ttheta_bank = 145.00
        job.parameters.resolution_sigma0 = 0
        job.parameters.resolution_sigma1 = 0
        job.parameters.resolution_sigma2 = 0
        job.parameters.resolution_gamma0 = 0
        job.parameters.resolution_gamma1 = 0
        job.parameters.resolution_gamma2 = 0
        job.parameters.resolution_alpha0 = 0
        job.parameters.resolution_alpha1 = 0
        job.parameters.resolution_beta0 = 0
        job.parameters.resolution_beta1 = 0
        return job

    @property
    def experimentType(self):
        exp_type = None
        if issubclass(type(self._sample.parameters), Instrument1DCWPolParameters):
            exp_type = 'powder1DCWpol'
        elif issubclass(type(self._sample.parameters), Instrument1DCWParameters):
            exp_type = 'powder1DCW'
        elif issubclass(type(self._sample.parameters), Instrument1DTOFParameters):
            exp_type = 'powder1DTOF'
        else:
            raise AttributeError('Unknown EXP type')
        return exp_type

    @experimentType.setter
    def experimentType(self, new_exp_type: str):
        if new_exp_type == 'powder1DCWpol':
            self._sample = self._defaultCWPolJob()
        elif new_exp_type == 'powder1DCWunp' or new_exp_type == 'powder1DCW':
            self._sample = self._defaultCWJob()
            if new_exp_type == 'powder1DCW':
                new_exp_type = 'powder1DCWunp'
        elif new_exp_type == 'powder1DTOFunp' or new_exp_type == 'powder1DTOF':
            self._sample = self._defaultTOFJob()
            if new_exp_type == 'powder1DTOF':
                new_exp_type = 'powder1DTOFunp'
        else:
            raise AttributeError('Unknown Experiment type')

        interface = self._interface
        test_str = 'N' + new_exp_type
        if not self._interface.current_interface.feature_checker(test_str=test_str):
            interfaces = self._interface.interface_compatability(test_str)
            interface.switch(interfaces[0])

        self._sample.interface = interface
        self.parent.phasesAsObjChanged()
        self.parent.calculatorListChanged()

